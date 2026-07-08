# Auto Snowball v10.84 Sandbox Formal Live Gate Audit — 2026-07-08

## Scope
- Input package: `auto_snowball_web_v10_83_volume_percentage_fairness_e2e.zip`.
- Output package: `auto_snowball_web_v10_84_dense_centerline_ui_clarity_e2e.zip`.
- Requested change: clarify `中線入場狀態` so `區內 0.00%` is not mistaken for centerline reached.
- Sandbox cannot access Mac production workdir `/Users/andyna/Documents/自動滾倉系統設計`.
- Safety flags used: `AUTO_SNOWBALL_SAFE_MODE=1`, `AUTO_SNOWBALL_NO_REAL_ORDERS=1`, `AUTO_SNOWBALL_READ_ONLY=1`, `BINANCE_READ_ONLY=1`.
- No real orders were placed. No real trading mode was enabled.

## Change summary
- Version bumped to `10.84` / `D+E/v10.84`.
- UI now displays dense-zone membership and centerline status separately:
  - `密集區：已入區 / 區外上方 / 區外下方`;
  - `中線：未到 / 已觸及｜距中線 x.xx%`.
- Backend/API now expose `dense_zone_membership_status`, `dense_zone_membership_distance_pct`, `dense_zone_membership_label`, `dense_centerline_status`, `dense_centerline_status_label`, and `dense_centerline_distance_label`.
- Static template, WebSocket JS renderer, realtime page and strategy page use the same clarity fields.
- Formula audit explicitly states that `dense_zone_distance_pct` is distance to dense-zone boundary and `區內 0.00%` does not mean centerline reached.

## Tests
- Full pytest: `302 passed, 13 skipped`.
- 13 skipped tests are sandbox/browser/Mac-local evidence checks and cannot be counted as formal production browser E2E pass.

## 5050 runtime smoke
A fresh 5050 runtime was started from the inspected v10.84 package. The following returned HTTP 200 without Traceback/Internal Server Error text:
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
- `/api/system/formula-audit`: `ok=true`, `version=10.84`, `logic_version=D+E/v10.84`.
- Formula audit display labels include:
  - `dense_zone_membership_status = 密集區狀態：已入區 / 區外上方 / 區外下方`;
  - `dense_centerline_status = 中線狀態：未到中線 / 已觸及中線`;
  - `dense_centerline_distance_pct = 現價距離密集區中線`.
- `/api/coins` returned 10 visible candidates sorted by final score descending.
- Sample first row (BTCUSDC): `dense_zone_membership_status=已入密集區`, `dense_centerline_status=未到中線`, `dense_centerline_distance_pct=0.3177048233368634`, and `dense_zone_distance_label=密集區：已入區｜中線：未到｜距中線 0.32%`.

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
v10.84 implements the requested dense/centerline UI clarity update and passes all executable sandbox tests. Auto Snowball still has **not** reached true-fund formal live standard. Do not switch to real trading and do not place real orders until the formal-live blockers are cleared on the production Mac host.
