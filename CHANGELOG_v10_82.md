# CHANGELOG v10.82 — Dense Line Green Highlight

## Changed
- 「1日訊號 / 六線」與「4小時訊號 / 六線」每條 EMA/MA 數字新增密集區狀態顏色。
- 若該線數值已進入交易密集區上下沿，數字顯示綠色。
- 若該線數值未進入交易密集區，數字維持原本白色。
- 前端靜態渲染、WebSocket/API 動態更新、API payload 與 A/B 稽核同步。

## A/B sync
- A 端：API 新增/保留 `line_inside_dense_zone`、`line_inside_trade_dense_zone`、`line_inside_trade_dense_zone_count`。
- B 端：UI 用同一個 active dense zone 判斷每條 MA/EMA 數字是否加上 `line-in-dense-zone` 綠色 class。
- 兼容：未改買入 gate；v10.80 中線 gate 與 v10.81 中線入場分維持不變。

## Safety
- 未修改下單 endpoint、真實模式守門、read-only/safe/no-real-orders 防護。
- 未自動重啟交易、未切換真實模式、未下真實訂單。

## Tests
- Full pytest: `293 passed, 13 skipped`.
- 5050 smoke: `/`, `/auto-select`, `/calculator`, `/realtime`, `/audit-center`, `/virtual-account`, `/real-account`, `/control-panel`, `/api/status`, `/api/coins`, `/api/system/formula-audit`, `/api/engine/parameters`, `/api/system/formal-live-readiness` all returned HTTP 200 in sandbox.
