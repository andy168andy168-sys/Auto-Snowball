from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_ARCHIVE_TEST_FILES = {
    "rate-limit backoff": ("rate", "limit", "backoff"),
    "disconnect reconnect": ("disconnect", "reconnect"),
    "order idempotency duplicate guard": ("idempotency", "duplicate"),
    "timeout query-order recovery": ("timeout", "query", "recovery"),
    "circuit breaker": ("circuit", "breaker"),
    "process monitor watchdog": ("watchdog",),
    "one-year 4H backtest": ("one", "year", "4h", "backtest"),
    "formula consistency": ("formula", "consistency"),
    "browser E2E Playwright 5050 auto-select": ("browser", "playwright", "5050", "auto", "select"),
}

# Old string-only proof tests are forbidden. The meta-test that scans for these
# patterns is executable and is intentionally excluded from this text scan.
FORBIDDEN_STUB_MARKERS = (
    "release" + "_evidence",
    "evidence" + " = " + chr(34),
    "assert " + chr(34) + "rate" + chr(34) + " in evidence",
    "assert " + chr(34) + "disconnect" + chr(34) + " in evidence",
)

META_TEST_FILENAMES = {"test_no_safety_string_evidence_stubs.py"}


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Require executable production gate tests to exist inside the extracted "
            "release archive, not only in repository root"
        )
    )
    parser.add_argument("--extract-dir", required=True)
    args = parser.parse_args()

    root = Path(args.extract_dir)
    failures: list[str] = []
    test_paths = [p for p in root.rglob("test_*.py") if p.is_file()]
    normalized = [p.relative_to(root).as_posix().lower() for p in test_paths]

    for label, tokens in REQUIRED_ARCHIVE_TEST_FILES.items():
        if not any(all(token in path for token in tokens) for path in normalized):
            failures.append(
                f"missing release-archive executable test file for {label}; "
                "test must be inside extracted archive, not only repo root"
            )

    for path in test_paths:
        if path.name in META_TEST_FILENAMES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(marker in text for marker in FORBIDDEN_STUB_MARKERS):
            failures.append(
                f"{path.relative_to(root).as_posix()} still uses string-only evidence stubs"
            )

    if failures:
        print("RELEASE_ARCHIVE_TEST_PLACEMENT=FAIL")
        for failure in failures:
            print("-", failure)
        return 1

    print("RELEASE_ARCHIVE_TEST_PLACEMENT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
