from __future__ import annotations

import argparse
import sys
from pathlib import Path

REQUIRED_ARCHIVE_TEST_FILES = {
    "rate-limit backoff": ("rate", "limit", "backoff"),
    "disconnect reconnect": ("disconnect", "reconnect"),
    "order idempotency duplicate guard": ("idempot", "duplicate"),
    "timeout query-order recovery": ("timeout", "query", "recover"),
    "circuit breaker": ("circuit", "breaker"),
    "process monitor watchdog": ("watchdog",),
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Require production safety tests to exist inside the extracted release archive, not only in repository root")
    parser.add_argument("--extract-dir", required=True)
    args = parser.parse_args()

    root = Path(args.extract_dir)
    failures: list[str] = []
    test_paths = [p.relative_to(root).as_posix().lower() for p in root.rglob("test_*.py") if p.is_file()]

    for label, tokens in REQUIRED_ARCHIVE_TEST_FILES.items():
        if not any(all(token in path for token in tokens) for path in test_paths):
            failures.append(f"missing release-archive test file for {label}; test must be inside extracted archive, not only repo root")

    if failures:
        print("RELEASE_ARCHIVE_TEST_PLACEMENT=FAIL")
        for failure in failures:
            print("-", failure)
        return 1

    print("RELEASE_ARCHIVE_TEST_PLACEMENT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
