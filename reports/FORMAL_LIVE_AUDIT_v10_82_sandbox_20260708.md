# Auto Snowball v10.82 Sandbox Formal Live Gate Audit — 2026-07-08

## Scope
- Input package: `auto_snowball_web_v10_81_ranking_centerline_score_sync_e2e.zip`.
- Output package: `auto_snowball_web_v10_82_dense_line_green_e2e.zip`.
- Requested change: in `1日訊號 / 六線` and `4小時訊號 / 六線`, show each EMA/MA numeric value in green when that line has entered the dense zone; otherwise keep the current white styling.
- Sandbox cannot access Mac production workdir `/Users/andyna/Documents/自動滾倉系統設計`.
- Safety flags used: `AUTO_SNOWBALL_SAFE_MODE=1`, `AUTO_SNOWBALL_NO_REAL_ORDERS=1`, `AUTO_SNOWBALL_READ_ONLY=1`, `BINANCE_READ_ONLY=1`.
- No real orders were placed. No real trading mode was enabled.

## Change summary
- Version bumped to `10.82` / `D+E/v10.82`.
- Added backend helper `dense_line_inside_flags()`.
- `timeframe_six_line_payload()` now exposes `line_inside_dense_zone` and `line_inside_dense_zone_count`.
- `attach_timeframe_line_fields()` now exposes `line_inside_trade_dense_zone` and per-timeframe counts for active trading dense-zone highlighting.
- `auto_select.html` and `static/app.js` add `line-in-dense-zone` only to numeric MA/EMA values inside the active dense zone.
- `static/app.css` makes `.ma-line-value.line-in-dense-zone` use the existing green accent.
- Labels remain the original EMA/MA colors; only the numeric values change color.

## Tests
- Full pytest: `293 passed, 13 skipped`.
- 13 skipped tests are sandbox/browser/Mac-local evidence checks and cannot be counted as formal production browser E2E pass.

## 5050 runtime smoke
A fresh 5050 runtime was started from the inspected v10.82 package. The following returned HTTP 200 without Traceback/Internal Server Error text:
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

## A/B sync verification
- `/api/system/formula-audit`: `ok=true`, `version=10.82`, `logic_version=D+E/v10.82`.
- Formula audit display label includes `line_inside_dense_zone = 六線數字進入密集區時顯示綠色`.
- Template, JS and CSS all reference the same `line-in-dense-zone` contract.
- New regression tests verify backend flags, active trade dense-zone flags, template/JS/CSS sync, and formula audit contract.

## Formal live readiness
`/api/system/formal-live-readiness` still returned:
- `formal_live_ready=false`
- `ok=false`
- `must_not_claim_live_ready=true`
- blocking items: 9

Blocking items remain external/production evidence blockers, including Mac-local 5050 Playwright/browser E2E, production workdir evidence, fresh realtime sync evidence, 365-day/2190-bar 4H backtest evidence for all visible candidates, signed Binance reconciliation, complete safety evidence, and user-approved small-canary evidence.

## Conclusion
v10.82 implements the requested dense-line green highlight and passes all executable sandbox tests. Auto Snowball still has **not** reached true-fund formal live standard. Do not switch to real trading and do not place real orders until the formal-live blockers are cleared on the production Mac host.
