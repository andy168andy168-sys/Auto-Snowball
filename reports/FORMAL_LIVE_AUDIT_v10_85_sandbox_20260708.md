# Auto Snowball v10.85 Sandbox Formal Live Gate Audit — 2026-07-08

## Scope
- Input package: `auto_snowball_web_v10_84_dense_centerline_ui_clarity_e2e.zip`.
- Output package: `auto_snowball_web_v10_85_backtest_l1_priority_e2e.zip`.
- Requested change: do not change any formula except the backtest score; make L1 profit-floor score highest and L10 lowest.
- Sandbox cannot access Mac production workdir `/Users/andyna/Documents/自動滾倉系統設計`.
- Safety flags used: `AUTO_SNOWBALL_SAFE_MODE=1`, `AUTO_SNOWBALL_NO_REAL_ORDERS=1`, `AUTO_SNOWBALL_READ_ONLY=1`, `BINANCE_READ_ONLY=1`.
- No real orders were placed. No real trading mode was enabled.

## Change summary
- Version bumped to `10.85` / `D+E/v10.85`.
- Only the one-year 4H backtest scoring formula was changed.
- Unchanged formulas: dense-zone, centerline gate, L1 entry boundaries, volume score, volatility score, L1-L10 stages, stop-loss, profit-floor protection, final ranking weights, safety gates.
- New backtest basis: `l1_profit_floor_priority`.
- New signal scoring table:
  - L1 profit-floor win = 100;
  - L2 = 90;
  - L3 = 80;
  - L4 = 70;
  - L5 = 60;
  - L6 = 50;
  - L7 = 40;
  - L8 = 30;
  - L9 = 20;
  - L10 = 10;
  - unprotected/unresolved = 0;
  - stop-loss = -10, then normalized/clamped to 0 and additionally penalized by stop-loss rate.
- `backtest_level_score` now means one-year 4H L1-profit-floor-priority score.
- UI labels now show `一年L1保盈分`.

## Tests
- Full pytest via wrapper after pytest returned: `307 passed, 13 skipped`.
- 13 skipped tests are sandbox/browser/Mac-local evidence checks and cannot be counted as formal production browser E2E pass.

## 5050 runtime smoke
A fresh 5050 runtime was started from the inspected v10.85 package. The following returned HTTP 200 without Traceback/Internal Server Error text:
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
- `/api/system/formula-audit`: `ok=true`, `version=10.85`, `logic_version=D+E/v10.85`.
- Formula audit exposes `ranking_score.backtest_score.config.basis = l1_profit_floor_priority`.
- A/B checks include `backtest_score_basis` and `backtest_score_l1_highest_l10_lowest`; both passed.
- `/api/coins` returned 10 visible candidates sorted by final score descending.

## Safety guard checks
Runtime write protections behaved as expected:
- DNS rebinding Host header blocked: HTTP 403.
- Mutating GET `/api/engine/plan` blocked: HTTP 405.
- GET refresh `/api/research/dense-width?refresh=1` blocked: HTTP 405.
- Cross-site POST blocked: HTTP 403.
- No-Origin / no-local POST blocked: HTTP 403.
- Real-mode switch attempt `/api/mode` blocked under safe/read-only/no-real-orders: HTTP 423.
- Start automatic trading `/api/action` blocked under safe/read-only/no-real-orders: HTTP 423.
- One-key close-all `/api/engine/close-all` with `confirm=CLOSE_ALL` blocked under safe/read-only/no-real-orders: HTTP 423.

## Formal live readiness
`/api/system/formal-live-readiness` still returned:
- `formal_live_ready=false`
- `ok=false`
- `must_not_claim_live_ready=true`
- blocking items: 9

Blocking items remain external/production evidence blockers, including Mac-local 5050 Playwright/browser E2E, production workdir evidence, fresh realtime sync evidence, 365-day/2190-bar 4H backtest evidence for all visible candidates, signed Binance reconciliation, complete safety evidence, and user-approved small-canary evidence.

## Conclusion
v10.85 implements the requested backtest-score-only update and passes all executable sandbox tests. Auto Snowball still has **not** reached true-fund formal live standard. Do not switch to real trading and do not place real orders until the formal-live blockers are cleared on the production Mac host.
