# CHANGELOG v10.91 — Centerline Crossing Touch Consistency

## Fixed
- 修正「現價穿越中線」顯示/判斷一致性。
- 只要上一口價與現價跨過密集區中線，就一律算 `已觸及中線`。
- 即使現價已經由密集區下方跳到上方，或由上方跳到下方，UI/API 也不再顯示 `未到中線 / 先等觸及中線`。
- `dense_centerline_reached=true`、`dense_centerline_crossed=true` 時，會同步：
  - `dense_entry_ready=true`；
  - `dense_centerline_status=已觸及中線`；
  - `dense_centerline_status_label=中線：已觸及`；
  - `dense_zone_arrival_status=已進入中線`。

## Unchanged
- 入場公式不改。
- 密集區公式不改。
- 成交量分不改。
- 波動分不改。
- 回測分不改。
- L1-L10 階梯不改。
- 止損 / 保盈公式不改。
- 排行榜權重不改。
- 真實模式守門、read-only/safe/no-real-orders 防護不改。

## Safety
- 未自動重啟交易。
- 未切換真實模式。
- 未下真實訂單。
