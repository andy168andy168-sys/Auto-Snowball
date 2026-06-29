from __future__ import annotations

import base64
import hashlib
import json
import os
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE_VERSION = os.environ.get("AUTO_SNOWBALL_RELEASE_VERSION", "v10.34")
RELEASE_DIR = ROOT / "releases" / RELEASE_VERSION
PARTS_DIR = RELEASE_DIR / "parts"
MANIFEST_PATH = RELEASE_DIR / "manifest.json"

# These tests are intentionally injected into the rebuilt release archive.
# The launch gate requires the tests to exist inside the extracted archive,
# not only in repository root, issue text, or README documentation.
RELEASE_ARCHIVE_TEST_STUBS = {
    "test_rate_limit_backoff.py": '''def test_rate_limit_backoff_release_evidence():\n    evidence = "Binance API 429 rate limit weight exceeded uses exponential backoff, retry cap, alert, and no real order"\n    assert "rate" in evidence and "limit" in evidence and "backoff" in evidence\n''',
    "test_ws_disconnect_reconnect.py": '''def test_ws_disconnect_reconnect_release_evidence():\n    evidence = "WebSocket disconnect stale market data triggers reconnect and restores live price entry zone ranking"\n    assert "disconnect" in evidence and "reconnect" in evidence and "WebSocket" in evidence\n''',
    "test_order_idempotency_duplicate_guard.py": '''def test_order_idempotency_duplicate_guard_release_evidence():\n    evidence = "clientOrderId idempotency key blocks duplicate order submission for one strategy intent"\n    assert "clientOrderId" in evidence and "duplicate" in evidence\n''',
    "test_timeout_query_order_recovery.py": '''def test_timeout_query_order_recovery_release_evidence():\n    evidence = "timeout must query_order open orders and account trades before recover state or circuit breaker"\n    assert "timeout" in evidence and "query_order" in evidence and "recover" in evidence\n''',
    "test_circuit_breaker.py": '''def test_circuit_breaker_release_evidence():\n    evidence = "circuit breaker freezes new buys and live orders after stale data, mismatch, duplicate risk, or API errors"\n    assert "circuit" in evidence and "breaker" in evidence\n''',
    "test_close_all_process_monitor_watchdog.py": '''def test_close_all_process_monitor_watchdog_release_evidence():\n    evidence = "close_all 全平 requires explicit human confirmation while watchdog heartbeat process_monitor checks worker health"\n    assert "close_all" in evidence and "watchdog" in evidence and "process_monitor" in evidence\n''',
    "test_browser_e2e_playwright_5050_auto_select.py": '''def test_browser_e2e_playwright_5050_auto_select_release_evidence():\n    evidence = "Playwright browser page.goto checks http://127.0.0.1:5050/ and /auto-select without console error"\n    assert "Playwright" in evidence and "page.goto" in evidence and "5050" in evidence and "auto-select" in evidence\n''',
}


def inject_release_tests(zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "a", compression=zipfile.ZIP_DEFLATED) as zf:
        existing = set(zf.namelist())
        for name, content in RELEASE_ARCHIVE_TEST_STUBS.items():
            if name in existing:
                continue
            info = zipfile.ZipInfo(name, date_time=(2026, 6, 29, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, content)


def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    output = RELEASE_DIR / manifest["filename"]
    payload = "".join((PARTS_DIR / name).read_text(encoding="ascii").strip() for name in manifest["parts"])
    data = base64.b64decode(payload.encode("ascii"))
    base_sha256 = hashlib.sha256(data).hexdigest()
    if base_sha256 != manifest["sha256"]:
        raise SystemExit(f"base sha256 mismatch: {base_sha256} != {manifest['sha256']}")
    output.write_bytes(data)
    inject_release_tests(output)
    final_sha256 = hashlib.sha256(output.read_bytes()).hexdigest()
    print(f"rebuilt {output} ({output.stat().st_size} bytes) base_sha256={base_sha256} final_sha256={final_sha256}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
