# Auto Snowball v10.80 Formal Live Gate Re-run — 2026-07-08 16:43 TPE

## Scope
- Package inspected: `auto_snowball_web_v10_80_centerline_entry_gate_e2e.zip`.
- SHA256 verified: `bd84a73dc5b5b3fb539cf9f1984fd2a45f6c4859fa5801f99725722a7bbf660d`.
- Runtime tested from sandbox directory: `/mnt/data/audit_v10_80_run/auto_snowball_web_v10_80_centerline_entry_gate_e2e`.
- Requested Mac production workdir could not be accessed from this sandbox: `/Users/andyna/Documents/自動滾倉系統設計`.
- Safety flags used: `AUTO_SNOWBALL_SAFE_MODE=1`, `AUTO_SNOWBALL_NO_REAL_ORDERS=1`, `AUTO_SNOWBALL_READ_ONLY=1`, `BINANCE_READ_ONLY=1`.
- No real orders were placed. No real trading mode was enabled.

## Vulnerability check
- No new code vulnerability was found in this re-run.
- No code change was required.
- No v10.81 package was produced.
- The v10.80 centerline-entry rule remains active and did not regress.

## Pytest / E2E status
- Full pytest: `286 passed, 13 skipped`.
- Skipped tests are sandbox/browser/Mac-local evidence checks and cannot be counted as formal production browser E2E pass.

## 5050 runtime smoke
Fresh 5050 runtime was started from the inspected v10.80 package. The following returned HTTP 200 without Traceback/Internal Server Error text:
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

## Ranking and centerline-entry gate
- `/api/coins` returned 10 visible candidates.
- Score order was descending: BTCUSDC, ETHUSDC, SOLUSDC, BNBUSDC, XRPUSDC, ADAUSDC, AVAXUSDC, DOGEUSDC, LINKUSDC, TIAUSDC.
- All visible candidates showed centerline-aware fields: `dense_entry_ready`, `dense_centerline_reached`, and `dense_centerline_distance_pct`.
- Current sample state: all 10 candidates were `區內未到中線`; `dense_entry_ready=false`; `dense_centerline_reached=false`.
- This confirms the v10.80 rule that merely entering the dense zone is not enough to arm L1.

## Formula / A-B sync
- `/api/system/formula-audit`: `ok=true`, `version=10.80`, `logic_version=D+E/v10.80`.
- A/B checks: 16 total, 0 failed.
- Dense zone remains six-line center ±1.5% total 3%.
- Entry gate remains `CENTERLINE`.

## Safety guard checks
Runtime write protections behaved as expected:
- DNS rebinding Host header blocked: HTTP 403.
- Mutating GET `/api/engine/plan` blocked: HTTP 405.
- GET refresh `/api/research/dense-width?refresh=1` blocked: HTTP 405.
- Cross-site POST blocked: HTTP 403.
- No-Origin / no-local POST blocked: HTTP 403.
- Real-mode switch attempt `/api/mode` blocked under safe/read-only/no-real-orders: HTTP 423.
- Start automatic trading `/api/action` blocked under safe/read-only/no-real-orders: HTTP 423.
- One-key close-all with `confirm=CLOSE_ALL` blocked under safe/read-only/no-real-orders: HTTP 423.

## Binance daily performance and dense-width research
- Virtual U-margined daily performance: `不可判定`; no complete closed rounds and no complete signed private Binance coverage in sandbox.
- Real U-margined daily performance: `不可判定`; no complete closed rounds and no complete signed private Binance coverage in sandbox.
- Recent 10-round wins and rolling 10-round 7-win/8-win ratios: `不可判定`; windows = 0.
- Dense-width research: `不可判定`; read-only true; no candidate width because complete one-year 4H histories/private production evidence are not available in sandbox.
- No leaderboard/backtest score was used as real trading win rate.

## Formal live readiness
`/api/system/formal-live-readiness` returned:
- `formal_live_ready=false`
- `ok=false`
- `must_not_claim_live_ready=true`
- blocking items: 9

Blocking items:
1. Need Mac local 5050 Playwright/browser E2E evidence with matching version/workdir/time.
2. Need evidence that audit workdir is `/Users/andyna/Documents/自動滾倉系統設計`.
3. Need fresh realtime prices, entry-zone status/score/ranking sync E2E evidence.
4. Need all visible candidate coins to have 365-day/about 2190 4H K-line backtest evidence.
5. Need signed Binance reconciliation clean evidence.
6. Need complete safety test evidence for rate-limit backoff, disconnect/reconnect, order idempotency, timeout query-order recovery, duplicate order guard, circuit breaker, close-all, and process monitor.
7. Need latest-version full pytest evidence accepted by the formal gate.
8. Need Mac local browser E2E all-pass evidence; sandbox skipped E2E is not sufficient.
9. Need formal preflight plus user-approved small-canary evidence.

## Conclusion
v10.80 passed executable sandbox pytest and 5050/API/safety smoke checks, and no new vulnerability was found. Auto Snowball still has **not** reached true-fund formal live standard. Do not switch to real trading and do not place real orders until the blocking items are cleared on the production Mac host.
