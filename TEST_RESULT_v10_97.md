# TEST_RESULT v10.97

## Full pytest
```bash
AUTO_SNOWBALL_SAFE_MODE=1 \
AUTO_SNOWBALL_NO_REAL_ORDERS=1 \
AUTO_SNOWBALL_READ_ONLY=1 \
BINANCE_READ_ONLY=1 \
python - <<'PY'
import os, pytest
code = pytest.main(['-q'])
print(f'PYTEST_MAIN_EXIT_CODE={code}', flush=True)
os._exit(code)
PY
```

Result:
- `343 passed, 13 skipped`
- Exit code: `0`

## New regression coverage
- `test_v197_runtime_state_isolation.py`
- Updated `test_v194_runtime_state_persistence.py`
- Updated `test_v188_release_secret_hygiene.py`

Verified:
- All mutable runtime paths default outside the release root.
- Release-root state/cache/evidence is ignored by default.
- Legacy release-root import requires `AUTO_SNOWBALL_IMPORT_LEGACY_RUNTIME=1`.
- JSON runtime writes are atomic with file mode 0600 and private parent directory.
- virtual market cache is not reused in real mode.
- virtual and real engine states are stored and loaded separately.
- Running automatic trading cannot switch account mode.
- ARMED_L1 retention and centerline-then-breakout entry tests remain passing.

## Security regression subset
- Rate-limit backoff
- WebSocket disconnect/reconnect
- Book-stream resubscription
- Order idempotency / duplicate guard
- Timeout query-order recovery
- Circuit breaker
- Close-all / process watchdog
- DNS rebinding / CSRF / localhost POST provenance
- WebSocket listen-key redaction
- Release secret hygiene

Result: `68 passed` before the final full-suite rerun.

## 5050 runtime smoke
A clean v10.97 runtime was started with safe/read-only/no-real-orders flags. HTTP 200:
- `/`
- `/auto-select`
- `/calculator`
- `/realtime`
- `/audit-center`
- `/virtual-account`
- `/real-account`
- `/control-panel`
- `/api/status`
- `/api/coins`
- `/api/system/formula-audit`
- `/api/engine/parameters`
- `/api/system/formal-live-readiness`
- `/api/binance/daily-performance`
- `/api/binance/daily-performance?mode=real`
- `/api/research/dense-width`
- `/api/engine/status`

Checks:
- formula audit: `ok=true`, `version=10.97`, `logic_version=D+E/v10.97`
- `/api/coins`: 10 visible rows sorted by final score descending
- formal live: `formal_live_ready=false`, `must_not_claim_live_ready=true`, 9 blockers
- release root remained free of runtime secret/state/cache/evidence files while server was running

## Runtime safety smoke
- DNS rebinding Host: HTTP 403
- mutating GET engine plan: HTTP 405
- GET refresh dense-width: HTTP 405
- cross-origin POST: HTTP 403
- no-origin/no-local-header POST: HTTP 403
- real-mode switch under safe/read-only/no-real-orders: HTTP 423
- start automatic trading under safe/read-only/no-real-orders: HTTP 423
- one-key close-all under safe/read-only/no-real-orders: HTTP 423

## Browser E2E limitation
- Playwright Python and system Chromium were present.
- Chromium localhost navigation was blocked by the sandbox administrator policy with `net::ERR_BLOCKED_BY_ADMINISTRATOR`.
- Therefore this run does **not** claim Mac-local/browser E2E pass; the 13 browser/Mac-local evidence tests remain skipped.
