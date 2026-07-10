# CHANGELOG v10.98 — Centerline Trigger Highest Entry Score

## Changed
- 只改「中線入場分 / 中場入場分」評分定義與 A/B 顯示同步。
- 明確鎖死：已觸發 / 已觸及 / 已穿越 / 已武裝中線 = 原始 100 分，排行榜貢獻 25 分，最高分。
- 區內未到中線仍按距中線遠近給分，但不可達 100。
- 區外只給低分。
- 新增 `CENTERLINE_ENTRY_SCORE_CONFIG`：`basis = triggered_centerline_highest_score`。
- 新增 `centerline_entry_triggered_for_score()`，讓 `dense_entry_ready`、`dense_centerline_reached`、`dense_centerline_crossed`、`engine_entry_state=ARMED_L1`、中線已觸及/已武裝文字狀態都得到 100 分。
- `/api/system/formula-audit` 新增 `ranking_score.centerline_entry_score.config.basis = triggered_centerline_highest_score`。
- A/B checks 新增：
  - `centerline_entry_score_basis`；
  - `centerline_entry_score_triggered_highest`。

## Unchanged
- 中線觸碰條件不改。
- 密集區公式不改。
- 成交量分不改。
- 波動分不改。
- 回測分不改。
- L1-L10 階梯不改。
- 止損 / 保盈公式不改。
- 排行榜權重不改；中線入場分仍只佔 25%。
- 真實模式守門、read-only/safe/no-real-orders 防護不改。

## Safety
- 未自動重啟交易。
- 未切換真實模式。
- 未下真實訂單。
