# Auto Snowball v10.92 Sandbox Formal Live Gate Audit — 2026-07-09

## Scope
- Input package: `auto_snowball_web_v10_91_centerline_crossing_touch_e2e.zip`.
- Output package: `auto_snowball_web_v10_92_centerline_then_breakout_e2e.zip`.
- Requested change: current price crossing the dense-zone centerline only counts as centerline touched/armed; L1 entry must wait for a later breakout above/below the dense zone.
- Requested automation scope: sync GitHub, inspect for vulnerabilities, fix if found, run E2E, and check formal live readiness.
- Safety flags used during sandbox execution: `AUTO_SNOWBALL_SAFE_MODE=1`, `AUTO_SNOWBALL_NO_REAL_ORDERS=1`, `AUTO_SNOWBALL_READ_ONLY=1`, `BINANCE_READ_ONLY=1`.
- No real orders were placed. No real trading mode was enabled.

## Change summary
- Version bumped to `10.92` / `D+E/v10.92`.
- Only centerline-to-L1 entry sequencing was changed.
- Rule now enforced: centerline touch/crossing arms L1 only; it must not open L1 on the same tick.
- After armed, LONG L1 requires a later upward cross through the latest dense-zone upper edge.
- After armed, SHORT L1 requires a later downward cross through the latest dense-zone lower edge.
- A one-tick jump from below the dense zone to above it is treated as `armed_centerline_wait_breakout`, not a buy/open event.
- A one-tick jump from above the dense zone to below it is treated as `armed_centerline_wait_breakout`, not a sell/open event.

## Unchanged formulas
- Dense-zone formula unchanged.
- Volume score unchanged.
- Volatility score unchanged.
- Backtest score unchanged.
- L1-L10 stages unchanged.
- Stop-loss and profit-floor formulas unchanged.
- Final ranking weights unchanged.
- Real-mode and read-only/safe/no-real-orders guards unchanged.

## Tests
- Full pytest: `327 passed, 13 skipped`.
- New regression: `test_v192_centerline_then_breakout_entry.py`.
- The 13 skipped tests are browser/Playwright or Mac-local formal-gate evidence checks and cannot be counted as formal production browser E2E pass.

## 5050 runtime smoke
A fresh 5050 runtime was checked after the v10.92 change.
- Main pages and system APIs returned HTTP 200.
- `/api/system/formula-audit` reported v10.92 / D+E/v10.92.
- `/api/coins` returned 10 visible candidates sorted by final score descending.
- `/api/system/formal-live-readiness` returned `formal_live_ready=false` and `must_not_claim_live_ready=true`.
- `/api/binance/daily-performance` returned `不可判定` in sandbox.
- `/api/research/dense-width` returned `不可判定` in sandbox.

## Safety guard checks
Runtime write protections behaved as expected:
- DNS rebinding Host header blocked: HTTP 403.
- Mutating GET `/api/engine/plan` blocked: HTTP 405.
- GET refresh `/api/research/dense-width?refresh=1` blocked: HTTP 405.
- Cross-site POST blocked: HTTP 403.
- No-Origin / no-local POST blocked: HTTP 403.
- Real-mode switch attempt `/api/mode` blocked under safe/read-only/no-real-orders with local JSON POST: HTTP 423.
- Start automatic trading `/api/action` blocked under safe/read-only/no-real-orders with local JSON POST: HTTP 423.
- One-key close-all `/api/engine/close-all` with `confirm=CLOSE_ALL` blocked under safe/read-only/no-real-orders with local JSON POST: HTTP 423.

## Binance daily performance and dense-width research
- Virtual U-margined daily performance: `不可判定`; no complete closed rounds and no complete signed private Binance coverage in sandbox.
- Real U-margined daily performance: `不可判定`; no complete closed rounds and no complete signed private Binance coverage in sandbox.
- Recent 10-round wins and rolling 10-round 7-win/8-win ratios: `不可判定`; closed windows are not available in sandbox.
- Dense-width research: `不可判定`; no production one-year 4H histories/private evidence are available in sandbox.
- No leaderboard/backtest score was used as real trading win rate.

## Formal live readiness
v10.92 still does **not** meet true-fund formal-live standard. Required production evidence remains unavailable from this sandbox, including:
1. Mac local 5050 Playwright/browser E2E evidence with matching version/workdir/time.
2. Evidence that audit workdir is `/Users/andyna/Documents/自動滾倉系統設計`.
3. Fresh realtime prices, entry-zone status/score/ranking sync E2E evidence.
4. All visible candidate coins with 365-day/about 2190 4H K-line backtest evidence.
5. Signed Binance reconciliation clean evidence.
6. Complete safety evidence for rate-limit backoff, disconnect/reconnect, order idempotency, timeout query-order recovery, duplicate order guard, circuit breaker, close-all, and process monitor.
7. Latest-version full pytest evidence accepted by the formal gate.
8. Mac local browser E2E all-pass evidence; sandbox skipped E2E is not sufficient.
9. Formal preflight plus user-approved small-canary evidence.

## Conclusion
v10.92 implements the requested rule: centerline crossing only arms L1, and actual L1 entry waits for a later dense-zone upper/lower breakout. Auto Snowball still has **not** reached true-fund formal live standard. Do not switch to real trading and do not place real orders until the formal-live blockers are cleared on the production Mac host.
