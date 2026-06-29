from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

TEXT_SUFFIXES = {
    ".py", ".md", ".txt", ".html", ".htm", ".js", ".ts", ".json", ".yml", ".yaml", ".css"
}

REQUIRED_STATIC_EVIDENCE = [
    (
        "5050 runtime / smoke target is represented",
        [r"127\.0\.0\.1:5050", r"localhost:5050", r"port\s*=\s*5050", r"PORT[^\n]{0,40}5050", r"app\.run\([^\n]*5050"],
    ),
    (
        "leaderboard uses final score ordering",
        [r"final[_-]?score", r"最終分數", r"sort(?:ed)?\([^\n]{0,240}score", r"reverse\s*=\s*True", r"order_by[^\n]{0,120}score"],
    ),
    (
        "live price / entry status / ranking refresh source exists",
        [r"/api/market/live", r"入區", r"entry[_-]?zone", r"setInterval", r"WebSocket", r"EventSource"],
    ),
    (
        "one-year 4H backtest target is represented",
        [r"365", r"2190", r"4H|4h", r"one[-_ ]year|一年"],
    ),
    (
        "six-line dense-zone formula is represented",
        [r"六線", r"six[-_ ]?line", r"dense[_-]?zone", r"密集區", r"0\.015|1\.5%"],
    ),
    (
        "L1 stop-loss and profit-guard formulas are represented",
        [r"L1", r"stop[-_ ]?loss|止損", r"profit[-_ ]?guard|保盈", r"0\.8|80%", r"capital|本金"],
    ),
    (
        "Binance reconciliation / account truth is represented",
        [r"Binance", r"account", r"signed", r"balance", r"對帳|reconcil", r"exchange[_-]?truth"],
    ),
    (
        "formal preflight / canary gate is represented",
        [r"preflight|前置檢查", r"canary|灰度|小額", r"production|正式", r"live", r"go[-_ ]?live|上線"],
    ),
    (
        "real-order safety guard is represented",
        [r"NO_REAL_ORDERS", r"DRY[_-]?RUN", r"simulation[_-]?only", r"read[-_ ]?only", r"SAFE[_-]?MODE", r"禁止.*真實訂單"],
    ),
]

REQUIRED_TEST_EVIDENCE = [
    ("rate-limit backoff test", [r"rate[-_ ]?limit|429", r"backoff|退避"]),
    ("disconnect reconnect test", [r"disconnect|斷線", r"reconnect|重連|WebSocket"]),
    ("order idempotency / duplicate-order protection test", [r"idempot|clientOrderId|冪等", r"duplicate|重複下單"]),
    ("timeout query-order recovery test", [r"timeout|逾時", r"query[_-]?order|查單", r"recover|復原"]),
    ("circuit breaker test", [r"circuit|breaker|熔斷"]),
    ("one-click close-all test", [r"close[_-]?all|全平|flatten"]),
    ("process monitor / watchdog test", [r"watchdog|heartbeat|process[_-]?monitor|程序監控"]),
    ("browser E2E / Playwright test", [r"playwright", r"page\.goto|browser", r"5050|auto-select"]),
]


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and not path.name.startswith("test_"):
            continue
        parts = {part.lower() for part in path.parts}
        if ".git" in parts or "__pycache__" in parts:
            continue
        yield path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return ""
    except Exception:
        return ""


def build_corpus(root: Path) -> tuple[str, str, list[Path]]:
    all_chunks: list[str] = []
    test_chunks: list[str] = []
    test_files: list[Path] = []
    for path in iter_text_files(root):
        rel = str(path.relative_to(root))
        text = read_text(path)
        chunk = f"\n--- FILE: {rel} ---\n{text}\n"
        all_chunks.append(chunk)
        is_test = path.name.startswith("test_") or "/test" in rel.replace("\\", "/").lower() or "e2e" in rel.lower()
        if is_test:
            test_files.append(path)
            test_chunks.append(chunk)
    return "\n".join(all_chunks), "\n".join(test_chunks), test_files


def has_all_patterns(text: str, patterns: list[str]) -> bool:
    return all(re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL) for pattern in patterns)


def has_any_pattern(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL) for pattern in patterns)


def main() -> int:
    parser = argparse.ArgumentParser(description="Static production-gate evidence audit for Auto Snowball release archive")
    parser.add_argument("--zip", dest="zip_path", required=True)
    parser.add_argument("--extract-dir", required=True)
    args = parser.parse_args()

    zip_path = Path(args.zip_path)
    extract_dir = Path(args.extract_dir)
    failures: list[str] = []

    if not zip_path.exists():
        failures.append(f"missing release zip: {zip_path}")
    else:
        try:
            with zipfile.ZipFile(zip_path) as zf:
                bad = zf.testzip()
                if bad:
                    failures.append(f"zip integrity failed at member: {bad}")
                names = zf.namelist()
                if not any(name.endswith(".py") for name in names):
                    failures.append("zip contains no Python source files")
                if not any(Path(name).name.startswith("test_") for name in names):
                    failures.append("zip contains no pytest-style test files")
        except zipfile.BadZipFile as exc:
            failures.append(f"bad release zip: {exc}")

    if not extract_dir.exists():
        failures.append(f"missing extracted directory: {extract_dir}")
    else:
        corpus, test_corpus, test_files = build_corpus(extract_dir)
        if not test_files:
            failures.append("no test files discovered after extraction")

        for label, patterns in REQUIRED_STATIC_EVIDENCE:
            if not has_any_pattern(corpus, patterns):
                failures.append(f"missing static evidence: {label}")

        for label, patterns in REQUIRED_TEST_EVIDENCE:
            if not has_all_patterns(test_corpus, patterns):
                failures.append(f"missing test evidence: {label}")

    if failures:
        print("PRODUCTION_GATE_AUDIT=FAIL")
        for item in failures:
            print(f"- {item}")
        return 1

    print("PRODUCTION_GATE_AUDIT=PASS")
    print("Static evidence exists for all required launch-gate categories. Dynamic pytest/E2E results are evaluated by later CI steps.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
