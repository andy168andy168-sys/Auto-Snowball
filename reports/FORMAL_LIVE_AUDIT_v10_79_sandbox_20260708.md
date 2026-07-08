# Auto Snowball v10.79 Sandbox Formal Live Gate Audit — 2026-07-08

## Scope
- Input package inspected: `auto_snowball_web_v10_78_l1_stop_100_e2e.zip`.
- Patched output package: `auto_snowball_web_v10_79_release_provenance_hardening_e2e.zip`.
- Runtime tested from sandbox directory: `/mnt/data/work_v10_79/auto_snowball_web_v10_79_release_provenance_hardening_e2e`.
- Requested Mac production workdir could not be accessed from this sandbox: `/Users/andyna/Documents/自動滾倉系統設計`.
- Safety flags used: `AUTO_SNOWBALL_SAFE_MODE=1`, `AUTO_SNOWBALL_NO_REAL_ORDERS=1`, `AUTO_SNOWBALL_READ_ONLY=1`, `BINANCE_READ_ONLY=1`.
- No real orders were placed. No real mode switch was allowed.

## Vulnerability / failure found and fixed
- Found CI/provenance reliability bug in the v10.78 package workflow: `.github/workflows/auto-snowball-release-provenance.yml` still depended on finding `auto_snowball_web_v*.zip` in the checkout workspace, then tried `scripts/rebuild_release.py` as fallback.
- The release package does not include `scripts/rebuild_release.py`, so the fallback could not work inside the release snapshot.
- Fixed in v10.79 by changing the release provenance workflow fallback order to:
  1. download current workflow artifact named `release-zip`,
  2. download GitHub Release asset matching `auto_snowball_web_v*.zip`,
  3. search the workspace and print explicit diagnostics if no zip is found.
- Added/updated regression coverage so the workflow must keep artifact/release download support and must not depend on `scripts/rebuild_release.py` inside the release package.

## Test results
- Full pytest: `286 passed, 13 skipped`.
- Skips were browser/Playwright tests blocked by sandbox Chromium localhost policy or tests explicitly requiring Mac-local 5050 Playwright evidence.
- Package hygiene before repackaging: runtime/cache/state/key files removed/excluded (`__pycache__`, `.pytest_cache`, `.binance_api_keys.json`, runtime truth/market/engine state, logs, pid files).

## 5050 HTTP/API runtime check
Server started on `127.0.0.1:5050` with version `10.79`.

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
- `/api/coins`
- `/api/system/formula-audit`
- `/api/engine/parameters`
- `/api/system/formal-live-readiness`
- `/api/binance/daily-performance`
- `/api/binance/daily-performance?mode=real`
- `/api/research/dense-width`

## Ranking and formula checks
- `/api/coins` score order is descending: BTCUSDC 73.98, ETHUSDC 72.44, SOLUSDC 64.62, BNBUSDC 59.10, XRPUSDC 58.81, ADAUSDC 58.67, AVAXUSDC 57.45, DOGEUSDC 49.08, LINKUSDC 42.22, TIAUSDC 38.83.
- `/api/system/formula-audit`: `ok=true`, `version=10.79`, `logic_version=D+E/v10.79`.
- A→B sync passed with 15 checks.
- L1 max floating loss remains `100%` / `100 USDC` for 100 USDC capital.
- Staged profit floors remain synchronized; first three floor percentages are `25.0`, `55.0`, `180.0`.

## Safety guard checks
Runtime write protections behaved as expected:
- DNS rebinding Host header request blocked: HTTP 403.
- Mutating GET `/api/engine/plan` blocked: HTTP 405.
- GET refresh `/api/research/dense-width?refresh=1` blocked: HTTP 405.
- Cross-site POST blocked: HTTP 403.
- No-Origin POST blocked: HTTP 403.
- Real-mode switch attempt blocked under safe/read-only guard.
- Start automatic trading attempt blocked under safe/read-only guard.

## Binance daily performance and dense-width status
- Virtual daily performance: `不可判定`; no complete closed rounds; missing/incomplete signed private Binance `userTrades`, `allOrders`, and `income` coverage.
- Real daily performance: `不可判定`; no complete closed rounds; endpoint failures for private/signed account data in sandbox.
- Recent 10 rounds: `不可判定`; wins = 0 only because there are no complete closed rounds, not because strategy lost.
- Rolling 10-round 7-win/8-win ratios: `不可判定`; windows = 0.
- Dense-width research: `不可判定`; read-only true; no candidate width because one-year 4H K-line histories were absent/incomplete in sandbox.
- No leaderboard/backtest score was used as real trading win rate.

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
v10.79 fixes the release provenance workflow fallback bug and passes all executable sandbox tests. Auto Snowball still has **not** reached true-fund formal live standard because formal-live readiness remains blocked by missing Mac-local browser E2E, production workdir evidence, private Binance reconciliation, one-year 4H K-line evidence, and user-approved small-canary evidence. Do not switch to real trading and do not place real orders until all blocking items are cleared on the production Mac host.
