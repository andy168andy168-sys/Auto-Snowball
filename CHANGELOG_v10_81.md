# CHANGELOG v10.81 — Ranking Centerline Score Sync

## Changed
- 自動選幣排行榜「入區分」改名為「中線入場分」。
- 排行榜 25% 入場分與 v10.80 真正買入 gate 同步：
  - 已觸及/穿越密集區中線 = 100 分；
  - 區內未到中線 = 按距中線遠近給分；
  - 區外 = 只給低分。
- 新增 `centerline_entry_score_100` 與 `centerline_entry_score`，保留舊 `zone_entry_score*` 欄位作前端/測試兼容。
- Web 標籤由「入區分 / 現價入區狀態」更新為「中線入場分 / 中線入場狀態」。

## Safety
- 未修改下單 endpoint、真實模式守門、read-only/safe/no-real-orders 防護。
- 未自動重啟交易、未切換真實模式、未下真實訂單。

## Tests
- Full pytest: `289 passed, 13 skipped`.
- 5050 smoke: `/`, `/auto-select`, `/api/status`, `/api/coins`, `/api/system/formula-audit`, `/api/engine/parameters`, `/api/system/formal-live-readiness` all returned HTTP 200 in sandbox.
