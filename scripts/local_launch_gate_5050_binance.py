from __future__ import annotations

import argparse
import math
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any

import requests

BINANCE_SPOT_KLINES = "https://api.binance.com/api/v3/klines"
FOUR_HOURS_MS = 4 * 60 * 60 * 1000
ONE_YEAR_4H_EXPECTED = 365 * 6
ONE_YEAR_4H_MINIMUM = 2184  # allow a small edge-window tolerance around current partial candles

SAFE_ENV_NAMES = [
    "AUTO_SNOWBALL_SAFE_MODE",
    "AUTO_SNOWBALL_NO_REAL_ORDERS",
    "AUTO_SNOWBALL_READ_ONLY",
    "BINANCE_READ_ONLY",
]


def fail(message: str, failures: list[str]) -> None:
    print(f"FAIL: {message}")
    failures.append(message)


def get_json(url: str, timeout: float = 8.0) -> Any:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    ctype = response.headers.get("content-type", "")
    if "json" in ctype or response.text.strip().startswith(("{", "[")):
        return response.json()
    return response.text


def flatten_values(obj: Any):
    if isinstance(obj, dict):
        for value in obj.values():
            yield from flatten_values(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from flatten_values(value)
    else:
        yield obj


def find_symbols(obj: Any) -> list[str]:
    symbols: set[str] = set()
    pattern = re.compile(r"\b[A-Z0-9]{2,20}/?USDC\b")
    for value in flatten_values(obj):
        if isinstance(value, str):
            for match in pattern.findall(value.upper()):
                symbols.add(match.replace("/", ""))
    return sorted(symbols)


def find_row_lists(obj: Any) -> list[list[dict[str, Any]]]:
    found: list[list[dict[str, Any]]] = []
    if isinstance(obj, list) and obj and all(isinstance(x, dict) for x in obj):
        if any(any(key in row for key in ("symbol", "pair", "final_score", "score", "rank")) for row in obj):
            found.append(obj)  # type: ignore[arg-type]
    elif isinstance(obj, dict):
        for value in obj.values():
            found.extend(find_row_lists(value))
    return found


def number(value: Any) -> float | None:
    try:
        if value in (None, "", "--"):
            return None
        return float(str(value).replace("%", ""))
    except Exception:
        return None


def first_number(row: dict[str, Any], keys: tuple[str, ...]) -> float | None:
    for key in keys:
        if key in row:
            got = number(row[key])
            if got is not None:
                return got
    return None


def check_sorted_by_final_score(rows: list[dict[str, Any]], failures: list[str]) -> None:
    scored = []
    for idx, row in enumerate(rows):
        score = first_number(row, ("final_score", "finalScore", "final", "最終分數", "score"))
        if score is not None:
            scored.append((idx, score, row.get("symbol") or row.get("pair")))
    if len(scored) < 2:
        fail("leaderboard final-score fields were not found or insufficient for sorting verification", failures)
        return
    scores = [score for _, score, _ in scored]
    if scores != sorted(scores, reverse=True):
        fail(f"leaderboard is not sorted by descending final score: {scored[:10]}", failures)


def check_live_fields(rows: list[dict[str, Any]], failures: list[str]) -> None:
    required_groups = {
        "live price": ("price", "last_price", "current_price", "現價"),
        "entry status": ("entry_status", "in_zone", "入區", "入區狀態"),
        "entry score": ("entry_score", "入區分數"),
        "rank": ("rank", "排名"),
    }
    for row in rows:
        symbol = row.get("symbol") or row.get("pair") or "UNKNOWN"
        for label, keys in required_groups.items():
            if not any(key in row for key in keys):
                fail(f"{symbol}: missing {label} field in /api/market/live row", failures)


def check_formula_fields(rows: list[dict[str, Any]], failures: list[str]) -> None:
    for row in rows:
        symbol = row.get("symbol") or row.get("pair") or "UNKNOWN"
        center = first_number(row, ("six_line_center", "sixLineCenter", "六線中心"))
        dense_low = first_number(row, ("dense_low", "denseZoneLow", "密集區下限"))
        dense_high = first_number(row, ("dense_high", "denseZoneHigh", "密集區上限"))
        if center and dense_low and dense_high:
            if not math.isclose(dense_low, center * 0.985, rel_tol=1e-4, abs_tol=1e-8):
                fail(f"{symbol}: dense low formula mismatch, got {dense_low}, expected {center * 0.985}", failures)
            if not math.isclose(dense_high, center * 1.015, rel_tol=1e-4, abs_tol=1e-8):
                fail(f"{symbol}: dense high formula mismatch, got {dense_high}, expected {center * 1.015}", failures)
        else:
            fail(f"{symbol}: missing six-line dense-zone fields for formula verification", failures)

        capital = first_number(row, ("capital", "本金"))
        stop_pct = first_number(row, ("stop_loss_pct", "stopLossPct", "止損百分比"))
        stop_loss = first_number(row, ("stop_loss", "stopLoss", "止損"))
        if capital is not None and stop_pct is not None and stop_loss is not None:
            pct = stop_pct / 100 if stop_pct > 1 else stop_pct
            if not math.isclose(stop_loss, capital * pct, rel_tol=1e-4, abs_tol=1e-8):
                fail(f"{symbol}: stop-loss formula mismatch, got {stop_loss}, expected {capital * pct}", failures)
        else:
            fail(f"{symbol}: missing capital / stop-loss percent / stop-loss fields", failures)

        target = first_number(row, ("triggered_target", "triggerTarget", "激發目標"))
        guard = first_number(row, ("profit_guard", "profitGuard", "保盈"))
        if target is not None and guard is not None:
            if not math.isclose(guard, target * 0.8, rel_tol=1e-4, abs_tol=1e-8):
                fail(f"{symbol}: profit-guard formula mismatch, got {guard}, expected {target * 0.8}", failures)
        else:
            fail(f"{symbol}: missing triggered target / profit guard fields", failures)


def count_binance_4h_klines(symbol: str, start_ms: int, end_ms: int) -> int:
    count = 0
    cursor = start_ms
    while cursor < end_ms:
        params = {
            "symbol": symbol,
            "interval": "4h",
            "startTime": cursor,
            "endTime": end_ms,
            "limit": 1000,
        }
        response = requests.get(BINANCE_SPOT_KLINES, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data:
            break
        count += len(data)
        last_open = int(data[-1][0])
        next_cursor = last_open + FOUR_HOURS_MS
        if next_cursor <= cursor:
            break
        cursor = next_cursor
        time.sleep(0.05)
    return count


def check_public_backtests(symbols: list[str], failures: list[str]) -> None:
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=365)
    start_ms = int(start.timestamp() * 1000)
    end_ms = int(end.timestamp() * 1000)
    for symbol in symbols:
        try:
            count = count_binance_4h_klines(symbol, start_ms, end_ms)
        except Exception as exc:
            fail(f"{symbol}: Binance 4H kline fetch failed: {exc}", failures)
            continue
        print(f"{symbol}: one-year Binance 4H kline count={count}, expected≈{ONE_YEAR_4H_EXPECTED}")
        if count < ONE_YEAR_4H_MINIMUM:
            fail(f"{symbol}: insufficient one-year 4H klines: {count} < {ONE_YEAR_4H_MINIMUM}", failures)


def check_reconciliation(base_url: str, failures: list[str]) -> None:
    candidate_paths = [
        "/api/reconciliation/status",
        "/api/account/reconciliation",
        "/api/binance/reconciliation",
        "/api/account/truth",
    ]
    for path in candidate_paths:
        url = base_url.rstrip("/") + path
        try:
            data = get_json(url, timeout=5)
        except Exception:
            continue
        text = str(data).lower()
        if any(word in text for word in ("mismatch", "error", "異常", "fail")):
            fail(f"Binance reconciliation endpoint reports an issue: {path}: {data}", failures)
        else:
            print(f"Binance reconciliation endpoint checked: {path}")
        return
    fail("no Binance reconciliation endpoint was reachable from localhost; account balance/order/fee reconciliation is unverified", failures)


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only local launch gate for 127.0.0.1:5050 plus Binance public kline coverage")
    parser.add_argument("--base-url", default="http://127.0.0.1:5050")
    parser.add_argument("--skip-binance", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []

    for name in SAFE_ENV_NAMES:
        if os.environ.get(name) != "1":
            fail(f"safe env {name}=1 is not set", failures)

    base_url = args.base_url.rstrip("/")
    for path in ("/", "/auto-select", "/api/market/live"):
        url = base_url + path
        try:
            result = get_json(url)
            print(f"OK {url}")
        except Exception as exc:
            fail(f"{url} is not reachable or has an error: {exc}", failures)

    try:
        live = get_json(base_url + "/api/market/live")
    except Exception as exc:
        print("LOCAL_LAUNCH_GATE=FAIL")
        print(f"cannot continue without /api/market/live: {exc}")
        return 1

    row_lists = find_row_lists(live)
    if not row_lists:
        fail("/api/market/live did not expose a recognizable leaderboard row list", failures)
        rows: list[dict[str, Any]] = []
    else:
        rows = max(row_lists, key=len)
        print(f"leaderboard rows discovered={len(rows)}")
        check_sorted_by_final_score(rows, failures)
        check_live_fields(rows, failures)
        check_formula_fields(rows, failures)

    symbols = find_symbols(live)
    if not symbols:
        fail("no visible USDC candidate symbols discovered from /api/market/live", failures)
    else:
        print("visible USDC symbols:", ", ".join(symbols))
        if not args.skip_binance:
            check_public_backtests(symbols, failures)

    check_reconciliation(base_url, failures)

    if failures:
        print("LOCAL_LAUNCH_GATE=FAIL")
        for item in failures:
            print("-", item)
        return 1

    print("LOCAL_LAUNCH_GATE=PASS")
    print("All local 5050, visible candidate, Binance public kline, formula, and reconciliation checks passed in read-only mode.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
