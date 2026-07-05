# Auto Snowball v10.72 Test Result

## Targeted safety/formula/process tests

Result: `20 passed`.

Covered formal-live gate, daily performance/dense-width gate, unopened stage guard display, process-monitor stuck detection, order idempotency, timeout order-query recovery, circuit breaker, and process watchdog tests.

## Full pytest

Result: `279 passed, 13 skipped in 14.45s`.

## Browser subset

Result: `12 skipped in 9.97s`.

Sandbox browser skip is not valid Mac-local `127.0.0.1:5050` browser E2E evidence.

## 5050 smoke

Safe/read-only smoke returned 200 for:

- `/`
- `/auto-select`
- `/audit-center`
- `/api/status`
- `/api/system/formula-audit`
- `/api/system/runtime`
- `/api/system/formal-live-readiness`
- `/api/binance/daily-performance`
- `/api/research/dense-width`
- `/api/engine/status`

`/api/system/formal-live-readiness` returned `formal_live_ready=false`.
