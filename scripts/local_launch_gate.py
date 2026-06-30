from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def get(url: str, timeout: float = 8.0) -> tuple[int, str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "AutoSnowballLocalLaunchGate/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.headers.get("content-type", ""), resp.read().decode("utf-8", "replace")


def add(report: dict[str, Any], label: str, ok: bool, details: str) -> None:
    item = {"label": label, "status": "PASS" if ok else "FAIL", "details": details}
    report["checks"].append(item)
    if not ok:
        report["failures"].append(item)


def source_text(root: Path) -> str:
    chunks: list[str] = []
    for p in root.rglob("*"):
        rel = p.relative_to(root).as_posix() if root in p.parents or p == root else p.as_posix()
        if not p.is_file() or p.suffix.lower() not in {".py", ".js", ".ts", ".html", ".json", ".md"}:
            continue
        if any(skip in rel for skip in (".git/", "__pycache__/", ".pytest_cache/", "node_modules/", "venv/", ".venv/")):
            continue
        if p.name.startswith("test_"):
            continue
        chunks.append(p.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(chunks).lower()


def has_groups(text: str, groups: list[tuple[str, ...]]) -> tuple[bool, str]:
    missing = []
    for group in groups:
        if not any(token.lower() in text for token in group):
            missing.append(" or ".join(group))
    return not missing, "missing: " + ", ".join(missing) if missing else "present"


def candidates(x: Any) -> list[list[dict[str, Any]]]:
    found: list[list[dict[str, Any]]] = []
    if isinstance(x, list) and x and all(isinstance(i, dict) for i in x):
        keys = {str(k).lower() for row in x for k in row.keys()}
        if {"symbol", "pair", "s"} & keys and any("score" in k for k in keys):
            found.append(x)  # type: ignore[arg-type]
    if isinstance(x, dict):
        for v in x.values():
            found += candidates(v)
    elif isinstance(x, list):
        for v in x:
            found += candidates(v)
    return found


def num(row: dict[str, Any], names: tuple[str, ...]) -> float | None:
    low = {str(k).lower(): v for k, v in row.items()}
    for name in names:
        try:
            return float(low[name.lower()])
        except Exception:
            pass
    return None


def validate_market(payload: Any) -> tuple[bool, str]:
    lists = candidates(payload)
    if not lists:
        return False, "no candidate list with symbol + score found"
    rows = max(lists, key=len)
    scores: list[float] = []
    symbols: list[str] = []
    for row in rows:
        symbol = str(row.get("symbol") or row.get("pair") or row.get("s") or "")
        if not symbol:
            return False, f"row missing symbol: {row}"
        symbols.append(symbol)
        price = num(row, ("price", "last", "last_price", "current_price"))
        if price is None or price <= 0:
            return False, f"{symbol} missing positive price"
        score = num(row, ("final_score", "finalScore", "score", "entry_score", "入區分數"))
        if score is None:
            return False, f"{symbol} missing final/entry score"
        scores.append(score)
    if scores != sorted(scores, reverse=True):
        return False, f"not sorted by final score descending: {scores[:10]}"
    return True, f"validated {len(rows)} candidates: {symbols[:10]}"


def run_playwright(urls: list[str]) -> tuple[bool, str]:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        return False, f"Playwright unavailable: {exc}"
    errors: list[str] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.on("console", lambda m: errors.append(f"console:{m.type}:{m.text}") if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror:{e}"))
        for url in urls:
            resp = page.goto(url, wait_until="networkidle", timeout=20000)
            if not resp or resp.status >= 500:
                errors.append(f"{url} status={resp.status if resp else 'NO_RESPONSE'}")
        browser.close()
    return not errors, "\n".join(errors) if errors else "no browser console/page errors"


def main() -> int:
    parser = argparse.ArgumentParser(description="Auto Snowball local formal launch gate")
    parser.add_argument("--workdir", default="/Users/andyna/Documents/自動滾倉系統設計")
    parser.add_argument("--url", default="http://127.0.0.1:5050")
    parser.add_argument("--output", default="evidence/LOCAL_LAUNCH_GATE.json")
    parser.add_argument("--ci", action="store_true")
    parser.add_argument("--require-backtest-artifacts", action="store_true")
    parser.add_argument("--require-account-recon", action="store_true")
    args = parser.parse_args()

    root = Path(args.workdir).expanduser().resolve()
    report: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "workdir": str(root),
        "url": args.url,
        "checks": [],
        "failures": [],
    }

    safe_env = {k: os.environ.get(k) for k in ("AUTO_SNOWBALL_SAFE_MODE", "AUTO_SNOWBALL_NO_REAL_ORDERS", "AUTO_SNOWBALL_READ_ONLY", "BINANCE_READ_ONLY")}
    report["safe_env"] = safe_env
    add(report, "workdir exists", root.exists(), str(root))
    add(report, "read-only/no-real-orders env", all(v == "1" for v in safe_env.values()), json.dumps(safe_env, ensure_ascii=False))

    if not args.ci:
        out = subprocess.getoutput("lsof -nP -iTCP:5050 -sTCP:LISTEN || true")
        report["lsof_5050"] = out
        add(report, "127.0.0.1:5050 listening process", bool(out.strip()), out[-2000:])

    urls = [args.url.rstrip("/") + p for p in ("/", "/auto-select", "/api/market/live")]
    ok = True
    details = []
    payload = None
    for url in urls:
        try:
            status, _, body = get(url)
            details.append(f"{url} status={status}")
            ok = ok and status < 500 and "Traceback" not in body and "Internal Server Error" not in body
            if url.endswith("/api/market/live"):
                payload = json.loads(body)
        except Exception as exc:
            ok = False
            details.append(f"{url} ERROR {exc}")
    add(report, "5050 endpoints reachable without server errors", ok, "\n".join(details))

    add(report, "market/live price score ranking sync", *(validate_market(payload) if payload is not None else (False, "market payload unavailable")))
    add(report, "browser E2E no console/page errors", *run_playwright(urls))

    if root.exists():
        text = source_text(root)
        checks = {
            "rate-limit backoff": [("429", "rate limit", "x-mbx-used-weight"), ("backoff", "retry", "sleep")],
            "WebSocket reconnect": [("websocket", "socket", "ws"), ("disconnect", "closed", "stale"), ("reconnect", "restart")],
            "order idempotency duplicate guard": [("clientorderid", "client_order_id", "idempot"), ("duplicate", "dedupe", "重複")],
            "timeout query-order recovery": [("timeout", "readtimeout"), ("query_order", "get_order", "fetch_order", "查單"), ("recover", "restore", "復原")],
            "circuit breaker": [("circuit", "breaker", "熔斷"), ("freeze", "halt", "pause", "stop_new_buys")],
            "close_all watchdog": [("close_all", "flatten", "全平"), ("confirm", "manual", "確認"), ("watchdog", "heartbeat", "process_monitor")],
            "formula consistency": [("six_line", "六線", "dense_zone", "密集區"), ("distance", "距離"), ("l1",), ("stop_loss", "止損"), ("profit_guard", "保盈"), ("final_score", "最終分數")],
            "Binance signed reconciliation source": [("binance",), ("signed", "signature", "timestamp"), ("account", "balance"), ("reconciliation", "對帳", "exchange_truth")],
            "formal preflight canary": [("preflight", "前置檢查"), ("canary", "灰度", "小額"), ("production", "正式", "go_live", "上線")],
        }
        for label, groups in checks.items():
            passed, why = has_groups(text, groups)
            add(report, f"source feature: {label}", passed, why)

        backtest_files = [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in {".json", ".jsonl", ".csv"} and any(x in p.name.lower() for x in ("backtest", "kline", "4h"))]
        if args.require_backtest_artifacts:
            add(report, "365d/4H backtest artifacts exist", bool(backtest_files), str([p.as_posix() for p in backtest_files]))
        else:
            report["checks"].append({"label": "365d/4H backtest artifacts exist", "status": "INFO", "details": str([p.as_posix() for p in backtest_files])})

        recon_files = [p for p in root.rglob("*") if p.is_file() and any(x in p.name.lower() for x in ("recon", "account", "balance", "trade", "對帳"))]
        if args.require_account_recon:
            add(report, "Binance signed account reconciliation artifact", bool(recon_files), str([p.as_posix() for p in recon_files]))
        else:
            report["checks"].append({"label": "Binance signed account reconciliation artifact", "status": "INFO", "details": str([p.as_posix() for p in recon_files])})

    report["overall_status"] = "PASS" if not report["failures"] else "FAIL"
    output = Path(args.output)
    if not output.is_absolute():
        output = root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not report["failures"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
