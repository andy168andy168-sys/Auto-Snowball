# Auto Snowball v10.98 Sandbox Formal Live Gate Audit — 2026-07-10

## Scope
- Input package: `auto_snowball_web_v10_97_armed_snapshot_breakout_e2e.zip`.
- Output package: `auto_snowball_web_v10_98_centerline_trigger_score_e2e.zip`.
- Requested change: `中場入場分 / 中線入場分` should give the highest score after centerline has been triggered/touched/armed.
- Safety flags used during sandbox execution: `AUTO_SNOWBALL_SAFE_MODE=1`, `AUTO_SNOWBALL_NO_REAL_ORDERS=1`, `AUTO_SNOWBALL_READ_ONLY=1`, `BINANCE_READ_ONLY=1`.
- No real orders were placed. No real trading mode was enabled.

## Change summary
- Version bumped to `10.98` / `D+E/v10.98`.
- Only centerline-entry ranking score definition and A/B audit exposure were changed.
- New rule: centerline triggered/touched/crossed/armed gets raw 100 score and weighted 25 points.
- `ARMED_L1` gets the same highest centerline-entry score even if a display row lacks the older `dense_entry_ready` flag.
- Inside-zone-but-not-centerline distance score remains below 100.
- Outside-zone score remains low.

## A/B sync verification
- Added `CENTERLINE_ENTRY_SCORE_CONFIG` with `basis = triggered_centerline_highest_score`.
- `/api/system/formula-audit` exposes `ranking_score.centerline_entry_score.config.basis = triggered_centerline_highest_score`.
- A/B checks include `centerline_entry_score_basis` and `centerline_entry_score_triggered_highest`; both passed.

## Unchanged formulas
- Centerline touch/crossing condition unchanged.
- Dense-zone formula unchanged.
- Volume score unchanged.
- Volatility score unchanged.
- Backtest score unchanged.
- L1-L10 stages unchanged.
- Stop-loss and profit-floor formulas unchanged.
- Final ranking weights unchanged.
- Real-mode and read-only/safe/no-real-orders guards unchanged.

## Tests
- Full pytest: `344 passed, 13 skipped`.
- New regression: `test_v198_centerline_entry_score_triggered_highest.py`.
- The 13 skipped tests are browser/Playwright or Mac-local formal-gate evidence checks and cannot be counted as formal production browser E2E pass.

## 5050 runtime smoke
A fresh 5050 runtime was checked after the v10.98 change.
- Main pages and system APIs returned HTTP 200.
- `/api/system/formula-audit` reported `ok=true`, `version=10.98`, `logic_version=D+E/v10.98`.
- Formula audit reported `centerline_entry_score.config.basis=triggered_centerline_highest_score`.
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
v10.98 still does **not** meet true-fund formal-live standard. Required production evidence remains unavailable from this sandbox, including Mac-local browser E2E, production workdir evidence, realtime sync evidence, 365-day/about 2190 4H K-line backtest evidence for all visible candidates, signed Binance reconciliation, complete safety evidence, and user-approved small-canary evidence.

## Conclusion
v10.98 implements the requested rule: centerline triggered/touched/armed receives the highest centerline-entry ranking score. Auto Snowball still has **not** reached true-fund formal live standard. Do not switch to real trading and do not place real orders until the blockers are cleared on the production Mac host.
