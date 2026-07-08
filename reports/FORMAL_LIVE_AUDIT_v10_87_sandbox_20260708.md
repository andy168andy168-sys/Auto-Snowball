# Auto Snowball v10.87 Sandbox Formal Live Gate Audit — 2026-07-08

## Scope
- Input package: `auto_snowball_web_v10_86_volatility_monotonic_e2e.zip`.
- Output package: `auto_snowball_web_v10_87_backtest_profit_floor_stage_e2e.zip`.
- Requested change: update backtest score to explicit L1-L10 profit-floor stage scoring.
- Sandbox cannot access Mac production workdir `/Users/andyna/Documents/自動滾倉系統設計`.
- Safety flags used: `AUTO_SNOWBALL_SAFE_MODE=1`, `AUTO_SNOWBALL_NO_REAL_ORDERS=1`, `AUTO_SNOWBALL_READ_ONLY=1`, `BINANCE_READ_ONLY=1`.
- No real orders were placed. No real trading mode was enabled.

## Change summary
- Version bumped to `10.87` / `D+E/v10.87`.
- Only the one-year 4H backtest score definition was changed.
- Unchanged formulas: dense-zone, centerline gate, L1 entry boundaries, volume score, volatility score, L1-L10 stages, stop-loss, profit-floor protection, final ranking weights, safety gates.
- New backtest basis: `stage_profit_floor_priority`.
- New signal scoring table:
  - L1 保盈 = 100;
  - L2 保盈 = 90;
  - L3 保盈 = 80;
  - L4 保盈 = 70;
  - L5 保盈 = 60;
  - L6 保盈 = 50;
  - L7 保盈 = 40;
  - L8 保盈 = 30;
  - L9 保盈 = 20;
  - L10 保盈 = 10;
  - unprotected/unresolved = 0;
  - stop-loss = -10, then normalized/clamped to 0 and additionally penalized by stop-loss rate.
- The score is based on the actual protected/profit-floor stage, not the highest opened stage.
- UI labels now show `一年L1-L10保盈分`.

## Tests
- Full pytest: `313 passed, 13 skipped`.
- A focused post-README sync check also passed: `12 passed` for v10.87 regression, launch preflight and package hygiene tests.
- 13 skipped tests are sandbox/browser/Mac-local evidence checks and cannot be counted as formal production browser E2E pass.

## 5050 runtime smoke
A fresh 5050 runtime was started from the inspected v10.87 package. The following returned HTTP 200 without Traceback/Internal Server Error text:
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
- `/api/system/formula-audit`: `ok=true`, `version=10.87`, `logic_version=D+E/v10.87`.
- Formula audit exposes `ranking_score.backtest_score.config.basis = stage_profit_floor_priority`.
- A/B checks include `backtest_score_basis`, `backtest_score_l1_highest_l10_lowest`, and `backtest_score_requires_actual_profit_floor_stage`; all passed.
- `/api/coins` returned 10 visible candidates sorted by final score descending.

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
`/api/system/formal-live-readiness` still returned:
- `formal_live_ready=false`
- `ok=false`
- `must_not_claim_live_ready=true`
- blocking items: 9

Blocking items remain external/production evidence blockers, including Mac-local 5050 Playwright/browser E2E, production workdir evidence, fresh realtime sync evidence, 365-day/2190-bar 4H backtest evidence for all visible candidates, signed Binance reconciliation, complete safety evidence, and user-approved small-canary evidence.

## Conclusion
v10.87 implements the requested backtest-score-only update and passes all executable sandbox tests. Auto Snowball still has **not** reached true-fund formal live standard. Do not switch to real trading and do not place real orders until the formal-live blockers are cleared on the production Mac host.
