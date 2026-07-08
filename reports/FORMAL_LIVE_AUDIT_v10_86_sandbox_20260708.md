# Auto Snowball v10.86 Sandbox Formal Live Gate Audit — 2026-07-08

## Scope
- Input package: `auto_snowball_web_v10_85_backtest_l1_priority_e2e.zip`.
- Output package: `auto_snowball_web_v10_86_volatility_monotonic_e2e.zip`.
- Requested change: update volatility score so higher volatility gives higher score and lower volatility gives lower score.
- Sandbox cannot access Mac production workdir `/Users/andyna/Documents/自動滾倉系統設計`.
- Safety flags used: `AUTO_SNOWBALL_SAFE_MODE=1`, `AUTO_SNOWBALL_NO_REAL_ORDERS=1`, `AUTO_SNOWBALL_READ_ONLY=1`, `BINANCE_READ_ONLY=1`.
- No real orders were placed. No real trading mode was enabled.

## Change summary
- Version bumped to `10.86` / `D+E/v10.86`.
- Only the volatility score formula was changed.
- Unchanged formulas: dense-zone, centerline gate, L1 entry boundaries, volume score, backtest score, L1-L10 stages, stop-loss, profit-floor protection, final ranking weights, safety gates.
- New volatility basis: `monotonic_abs_24h_change`.
- New volatility score100 formula: `clamp(abs_24h_change_pct / 20.0 * 100, 0, 100)`.
- Score examples:
  - 0% absolute 24h change = 0;
  - 1% = 5;
  - 5% = 25;
  - 10% = 50;
  - 20% or more = 100.
- Risk remains a separate `risk_penalty`; high volatility no longer reduces the volatility component.

## Tests
- Full pytest: `310 passed, 13 skipped`.
- 13 skipped tests are sandbox/browser/Mac-local evidence checks and cannot be counted as formal production browser E2E pass.

## 5050 runtime smoke
A fresh 5050 runtime was started from the inspected v10.86 package. The following returned HTTP 200 without Traceback/Internal Server Error text:
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

## A/B sync verification
- `/api/system/formula-audit`: `ok=true`, `version=10.86`, `logic_version=D+E/v10.86`.
- Formula audit exposes `ranking_score.volatility_score.config.basis = monotonic_abs_24h_change`.
- A/B checks include `volatility_score_basis` and `volatility_score_monotonic_low_high`; both passed.
- `/api/coins` returned 10 visible candidates sorted by final score descending.

## Safety guard checks
Runtime write protections behaved as expected:
- DNS rebinding Host header blocked: HTTP 403.
- Mutating GET `/api/engine/plan` blocked: HTTP 405.
- GET refresh `/api/research/dense-width?refresh=1` blocked: HTTP 405.
- Cross-site POST blocked: HTTP 403.
- No-Origin / no-local POST blocked: HTTP 403.
- Real-mode switch attempt `/api/mode` blocked under safe/read-only/no-real-orders with JSON POST: HTTP 423.
- Start automatic trading `/api/action` blocked under safe/read-only/no-real-orders with JSON POST: HTTP 423.
- One-key close-all `/api/engine/close-all` with `confirm=CLOSE_ALL` blocked under safe/read-only/no-real-orders with JSON POST: HTTP 423.

## Binance daily performance and dense-width research
- Virtual U-margined daily performance: `不可判定`; no complete closed rounds and no complete signed private Binance coverage in sandbox.
- Real U-margined daily performance: `不可判定`; no complete closed rounds and no complete signed private Binance coverage in sandbox.
- Recent 10-round wins and rolling 10-round 7-win/8-win ratios: `不可判定`; closed windows are not available in sandbox.
- Dense-width research: `不可判定`; no production one-year 4H histories/private evidence are available in sandbox.
- No leaderboard/backtest score was used as real trading win rate.

## Formal live readiness
`/api/system/formal-live-readiness` still returned:
- `formal_live_ready=false`
- `ok=false`
- `must_not_claim_live_ready=true`
- blocking items: 9

Blocking items remain external/production evidence blockers, including Mac-local 5050 Playwright/browser E2E, production workdir evidence, fresh realtime sync evidence, 365-day/2190-bar 4H backtest evidence for all visible candidates, signed Binance reconciliation, complete safety evidence, and user-approved small-canary evidence.

## Conclusion
v10.86 implements the requested volatility-score-only update and passes all executable sandbox tests. Auto Snowball still has **not** reached true-fund formal live standard. Do not switch to real trading and do not place real orders until the formal-live blockers are cleared on the production Mac host.
