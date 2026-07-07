# Auto Snowball v10.77 Sandbox Formal Live Gate Audit — 2026-07-07

## Scope
- Package inspected: `auto_snowball_web_v10_77_staged_profit_guard_e2e.zip`
- Runtime tested from sandbox directory: `/mnt/data/work_v10_77/auto_snowball_web_v10_77_staged_profit_guard_e2e`
- Requested Mac production workdir could not be accessed from this sandbox: `/Users/andyna/Documents/自動滾倉系統設計`
- Safety flags used: `AUTO_SNOWBALL_SAFE_MODE=1`, `AUTO_SNOWBALL_NO_REAL_ORDERS=1`, `AUTO_SNOWBALL_READ_ONLY=1`, `BINANCE_READ_ONLY=1`
- No real orders were placed. No real mode switch was allowed.

## Test results
- Dependency install: requirements installed successfully in sandbox.
- Full pytest: `285 passed, 13 skipped`.
- Skips were browser/Playwright tests blocked by sandbox Chromium localhost policy; formal live gate correctly treats sandbox skips as insufficient for approval.
- Non-browser safety/regression group: `283 passed, 15 deselected`.
- Browser/E2E selected group: `2 passed, 13 skipped`.
- Package hygiene: 257 archive entries checked; no forbidden runtime/key/cache files found.
- Bandit static scan: no high/critical findings; observed items are false positives/low severity (`UNSAFE_BIND_HOSTS` constant, env var names, try/except pass).

## 5050 HTTP/API runtime check
Server started on `127.0.0.1:5050` with v10.77.

Pages/API returning HTTP 200 without Traceback/Internal Server Error text:
- `/`
- `/auto-select`
- `/calculator`
- `/realtime`
- `/audit-center`
- `/virtual-account`
- `/real-account`
- `/control-panel`
- `/api/status`
- `/api/system/formula-audit`
- `/api/engine/parameters`
- `/api/system/formal-live-readiness`
- `/api/binance/daily-performance`
- `/api/research/dense-width`

## Ranking and formula checks
- `/api/coins` score order is descending: BTCUSDC 73.98, ETHUSDC 72.44, SOLUSDC 64.62, BNBUSDC 59.10, XRPUSDC 58.81, ADAUSDC 58.67, AVAXUSDC 57.45, DOGEUSDC 49.08, LINKUSDC 42.22, TIAUSDC 38.83.
- `/api/system/formula-audit`: `ok=true`.
- A→B sync passed for dense-zone width, ranking weights, L1 max loss, L1 target total floating profit, L1-L10 staged profit-protection ratios, and computed profit floors.
- v10.77 staged protection ratios verified: L1 50%, L2 55%, L3 60%, L4 65%, L5 70%, L6 75%, L7 80%, L8 85%, L9 90%, L10 95%.

## Safety guard checks
Runtime write protections behaved as expected:
- DNS rebinding Host header request blocked: HTTP 403.
- Mutating GET `/api/engine/plan` blocked: HTTP 405.
- GET refresh `/api/research/dense-width?refresh=1` blocked: HTTP 405.
- Cross-site POST blocked: HTTP 403.
- No-Origin POST without local-control header blocked: HTTP 403.
- Local-control POST attempting real mode blocked by safe/read-only/no-real-orders guard: HTTP 423.
- Start automatic trading blocked by safe/read-only/no-real-orders guard: HTTP 423.

## Binance / real performance / dense-width status
- Binance WebSocket could not connect from sandbox because DNS resolution to Binance failed; mark prices were stale/absent.
- `/api/binance/daily-performance?mode=virtual`: status `不可判定`; no complete closed rounds; coverage incomplete.
- `/api/binance/daily-performance?mode=real`: status `不可判定`; no complete closed rounds; coverage incomplete.
- `/api/research/dense-width`: status `不可判定`; read-only true; no candidate width because one-year 4H histories were absent.
- POST refresh for daily performance remained `不可判定`; POST dense-width refresh timed out in sandbox due unavailable Binance network/DNS and should be rerun on the Mac production host with network access.

## Formal live readiness result
`/api/system/formal-live-readiness` returned:
- `formal_live_ready=false`
- `ok=false`
- `must_not_claim_live_ready=true`
- blocking items: 9

Blocking items:
1. Need Mac local 5050 Playwright/browser E2E evidence with matching version/workdir/time.
2. Need evidence that audit workdir is `/Users/andyna/Documents/自動滾倉系統設計`.
3. Need fresh realtime prices, entry-zone status/score/ranking sync E2E evidence.
4. Need all visible candidate coins to have 365-day / about 2190 4H K-line backtest evidence.
5. Need signed Binance reconciliation clean evidence.
6. Need complete safety test evidence for rate-limit backoff, disconnect/reconnect, order idempotency, timeout query-order recovery, duplicate order guard, circuit breaker, close-all, and process monitor.
7. Need latest-version full pytest pass evidence accepted by formal gate.
8. Need Mac local browser E2E all-pass evidence; sandbox skipped E2E is not sufficient.
9. Need formal preflight plus user-approved small-canary evidence.

## Conclusion
v10.77 package did not show a new code vulnerability in this sandbox audit, and all executable non-browser tests passed. However, Auto Snowball has **not** reached true-fund formal live standard because formal-live readiness is blocked by missing external/Mac/Binance/private-account evidence and unavailable live Binance data in this sandbox. Do not switch to real trading and do not place real orders until the blocking items are cleared on the production Mac host.
