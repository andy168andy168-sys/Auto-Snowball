# CHANGELOG v10.85 — Backtest L1 Profit-Floor Priority

## Changed
- 只改「一年回測分」評分方向；其他公式不改：
  - 入場公式不改；
  - 密集區公式不改；
  - 成交量分不改；
  - 波動分不改；
  - L1-L10 階梯不改；
  - 止損 / 保盈公式不改；
  - 最終排行榜權重仍是成交量20% + 波動15% + 密集區30% + 回測10% + 中線入場25% - 風險扣分。
- 回測分由舊「推到越高 L 層越高分」改為「L1 保盈優先」。
- 新回測單次訊號分：
  - L1 保盈 = 100 分；
  - L2 = 90 分；
  - L3 = 80 分；
  - L4 = 70 分；
  - L5 = 60 分；
  - L6 = 50 分；
  - L7 = 40 分；
  - L8 = 30 分；
  - L9 = 20 分；
  - L10 = 10 分；
  - 未完成保盈 / unresolved = 0 分；
  - 止損 = -10，正規化後歸零並按止損率額外扣分。
- `backtest_level_score` 現在代表「一年 4H L1 保盈優先回測分」。
- UI label 由「一年回測層級」同步改為「一年L1保盈分」。

## A/B sync
- A 端新增 `BACKTEST_SCORE_CONFIG`，明確標示 `basis = l1_profit_floor_priority`。
- B 端新增/同步 `backtest_l1_priority_signal_score()`。
- `/api/system/formula-audit` 新增 `ranking_score.backtest_score.config.basis = l1_profit_floor_priority`。
- A/B checks 新增：
  - `backtest_score_basis`；
  - `backtest_score_l1_highest_l10_lowest`。

## Safety
- 未修改下單 endpoint、真實模式守門、read-only/safe/no-real-orders 防護。
- 未自動重啟交易、未切換真實模式、未下真實訂單。

## Tests
- Full pytest via force-exit wrapper after pytest returned: `307 passed, 13 skipped`.
- New regression: `test_v185_backtest_l1_priority_score.py`.
- 5050 smoke: `/`, `/auto-select`, `/calculator`, `/realtime`, `/audit-center`, `/virtual-account`, `/real-account`, `/control-panel`, `/api/status`, `/api/coins`, `/api/system/formula-audit`, `/api/engine/parameters`, `/api/system/formal-live-readiness`, `/api/binance/daily-performance`, `/api/research/dense-width` all returned HTTP 200 in sandbox.
