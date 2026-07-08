# CHANGELOG v10.80 — Dense Centerline Entry Gate

## Changed
- 入場第三門檻由「現價必須先進入密集區」改為「現價必須先觸及/穿越密集區中線」。
- 單純在密集區上半區或下半區，不再武裝 L1。
- 只有當現價等於中線，或由上一筆 markPrice 穿越中線，才會進入 `ARMED_L1`。
- 中線 gate 通過後，仍然不鎖定上下沿；L1 做多/做空價繼續跟隨最新密集區上沿/下沿。

## A/B sync
- A 端公式：密集區 = 六線中心 ±1.5%；入場 gate = `CENTERLINE`。
- B 端引擎：`mark_reached_dense_zone_centerline()` 用上一筆 markPrice 與最新 markPrice 判斷是否觸及/穿越中線。
- Web / API 標籤同步：顯示 `已進入中線`、`區內未到中線`、`尚未進入中線`。

## Safety
- 未修改下單 endpoint、真實模式守門、read-only/safe/no-real-orders 防護。
- 未自動重啟交易、未切換真實模式、未下真實訂單。

## Tests
- Full pytest: `286 passed, 13 skipped`.
- 5050 smoke check: `/`, `/auto-select`, `/api/status`, `/api/coins`, `/api/system/formula-audit`, `/api/engine/parameters`, `/api/system/formal-live-readiness` all returned HTTP 200 in sandbox.
