# Auto Snowball v10.97 Sandbox Formal Live Gate Audit — 2026-07-10

## Scope
- Input package: `auto_snowball_web_v10_96_armed_tracking_retention_guard.zip`.
- Output package: `auto_snowball_web_v10_97_armed_snapshot_breakout_e2e.zip`.
- Requested issue: since changing from immediate dense-zone breakout entry to centerline-triggered tracking entry, no real candidate has successfully completed a buy; investigate and fix.
- Safety flags used during sandbox execution: `AUTO_SNOWBALL_SAFE_MODE=1`, `AUTO_SNOWBALL_NO_REAL_ORDERS=1`, `AUTO_SNOWBALL_READ_ONLY=1`, `BINANCE_READ_ONLY=1`.
- No real orders were placed. No real trading mode was enabled.

## Finding
This was not normal. The risk was not the centerline formula alone; the runtime chain could lose or dilute the armed tracking state before the later breakout arrived.

Observed / user-provided evidence:
- Real candidates had not left a successful `L1 已武裝 → 離區做多/做空 → open_L1` sequence.
- Some runtime state remained in `WAITING_CENTERLINE`.
- Earlier persisted `TESTUSDC` events were synthetic test pollution and must not be treated as real trading evidence.
- Armed plans must survive ranking rotation.
- Moving dense-zone boundaries can make a later breakout chase a moving target.

## Fix summary
- Version bumped to `10.97` / `D+E/v10.97`.
- Centerline touch/crossing still only arms tracking; it does not buy on the same tick.
- When L1 is armed, the system now snapshots the armed dense-zone low/high/centerline:
  - `armed_dense_zone_low`
  - `armed_dense_zone_high`
  - `armed_dense_zone_centerline`
  - `armed_dense_zone_at`
  - `armed_breakout_source=centerline_snapshot`
- Later L1 breakout uses the armed snapshot boundaries, not a constantly moving latest dense-zone edge.
- `set_plan_breakout_direction()` now uses the armed snapshot for L1 entry and stop boundary when available.
- `refresh_plan_dynamic_dense_zone()` no longer wipes `ARMED_L1` if the current market cache temporarily has no dense-zone row; it marks the state as retained tracking instead.
- `prepare_execution_plans()` continues to reserve execution slots for armed symbols even when they rotate out of the current top-four ranking.

## Unchanged formulas
- Centerline touch condition unchanged.
- Dense-zone formula unchanged.
- Volume score unchanged.
- Volatility score unchanged.
- Backtest score unchanged.
- L1-L10 stages unchanged.
- Stop-loss and profit-floor formulas unchanged.
- Final ranking weights unchanged.
- Real-mode and read-only/safe/no-real-orders guards unchanged.

## Tests
- Full pytest: `340 passed, 13 skipped`.
- New regression: `test_v197_armed_snapshot_breakout_real_sequence.py`.
- Focused regression/launch/hygiene checks: `23 passed`.
- The 13 skipped tests are browser/Playwright or Mac-local formal-gate evidence checks and cannot be counted as formal production browser E2E pass.

## 5050 runtime smoke
A fresh 5050 runtime was checked after the v10.97 change.
- Main pages and system APIs returned HTTP 200.
- `/api/system/formula-audit` reported `ok=true`, `version=10.97`, `logic_version=D+E/v10.97`.
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
v10.97 still does **not** meet true-fund formal-live standard. Required production evidence remains unavailable from this sandbox, including Mac-local browser E2E, production workdir evidence, realtime sync evidence, 365-day/about 2190 4H K-line backtest evidence for all visible candidates, signed Binance reconciliation, complete safety evidence, and user-approved small-canary evidence.

## Conclusion
v10.97 fixes the most likely runtime cause of the “centerline armed but never buys” problem: armed tracking now retains the centerline snapshot breakout boundaries across ranking rotation and dense-zone movement. Auto Snowball still has **not** reached true-fund formal live standard. Do not switch to real trading and do not place real orders until the blockers are cleared on the production Mac host.
