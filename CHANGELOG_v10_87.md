# CHANGELOG v10.87 — Backtest Profit-Floor Stage Score

## Changed
- 只改「一年回測分」評分定義；其他公式不改：
  - 入場公式不改；
  - 密集區公式不改；
  - 成交量分不改；
  - 波動分不改；
  - L1-L10 階梯不改；
  - 止損 / 保盈公式不改；
  - 最終排行榜權重仍是成交量20% + 波動15% + 密集區30% + 回測10% + 中線入場25% - 風險扣分。
- 回測分明確改成「L1-L10 保盈層級分」，必須以實際啟動的保盈層級計分，不是單純開到 L 幾。
- 新回測單次訊號分：
  - L1 保盈 = 100 分；
  - L2 保盈 = 90 分；
  - L3 保盈 = 80 分；
  - L4 保盈 = 70 分；
  - L5 保盈 = 60 分；
  - L6 保盈 = 50 分；
  - L7 保盈 = 40 分；
  - L8 保盈 = 30 分；
  - L9 保盈 = 20 分；
  - L10 保盈 = 10 分；
  - 未完成保盈 / unresolved = 0 分；
  - 止損 = -10，正規化後歸零並按止損率額外扣分。
- 例子：如果開到 L2，但實際只啟動 L1 保盈，仍按 L1 保盈 = 100 分；如果未啟動任何保盈，則 0 分。
- UI label 同步為「一年L1-L10保盈分」。

## A/B sync
- A 端 `BACKTEST_SCORE_CONFIG` 明確標示 `basis = stage_profit_floor_priority`。
- B 端 `backtest_stage_profit_floor_signal_score()` 按實際 `protected_stage` 計分。
- `/api/system/formula-audit` 暴露 `ranking_score.backtest_score.config.basis = stage_profit_floor_priority`。
- A/B checks 包括：
  - `backtest_score_basis`；
  - `backtest_score_l1_highest_l10_lowest`；
  - `backtest_score_requires_actual_profit_floor_stage`。

## Safety
- 未修改下單 endpoint、真實模式守門、read-only/safe/no-real-orders 防護。
- 未自動重啟交易、未切換真實模式、未下真實訂單。

## Tests
- Full pytest: `313 passed, 13 skipped`.
- New regression: `test_v187_backtest_profit_floor_stage_score.py`.
- 5050 smoke: `/`, `/auto-select`, `/calculator`, `/realtime`, `/audit-center`, `/virtual-account`, `/real-account`, `/control-panel`, `/api/status`, `/api/coins`, `/api/system/formula-audit`, `/api/engine/parameters`, `/api/system/formal-live-readiness`, `/api/binance/daily-performance`, `/api/research/dense-width` all returned HTTP 200 in sandbox.
