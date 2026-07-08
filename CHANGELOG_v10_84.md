# CHANGELOG v10.84 — Dense / Centerline UI Clarity

## Changed
- 「中線入場狀態」顯示拆成兩層：
  - `密集區：已入區 / 區外上方 / 區外下方`；
  - `中線：未到 / 已觸及｜距中線 x.xx%`。
- 原本 `區內 0.00% / 已進入` 容易被誤會為已到中線，現已改成明確顯示「密集區已入區，但中線未到」。
- `/api/coins` 新增/同步 UI clarity 欄位：
  - `dense_zone_membership_status`
  - `dense_zone_membership_distance_pct`
  - `dense_zone_membership_label`
  - `dense_centerline_status`
  - `dense_centerline_status_label`
  - `dense_centerline_distance_label`
- `auto_select.html`、`static/app.js`、`realtime.html`、`strategy_coin.html` 同步使用新欄位。

## A/B sync
- A 端 formula-audit 新增 display-label contract，明確指出 `dense_zone_distance_pct` 只是距離密集區邊界；區內 0.00% 不代表已到中線。
- B 端 UI 使用 `dense_centerline_distance_pct` 顯示距中線，與 v10.80 中線 gate 保持一致。

## Safety
- 未修改下單 endpoint、真實模式守門、read-only/safe/no-real-orders 防護。
- 未自動重啟交易、未切換真實模式、未下真實訂單。

## Tests
- Full pytest: `302 passed, 13 skipped`.
- 5050 smoke: `/`, `/auto-select`, `/calculator`, `/realtime`, `/audit-center`, `/virtual-account`, `/real-account`, `/control-panel`, `/api/status`, `/api/coins`, `/api/system/formula-audit`, `/api/engine/parameters`, `/api/system/formal-live-readiness` all returned HTTP 200 in sandbox.
