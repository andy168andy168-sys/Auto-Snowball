# CHANGELOG v10.86 — Volatility Monotonic Score

## Changed
- 只改「波動分」評分方向；其他公式不改：
  - 入場公式不改；
  - 密集區公式不改；
  - 成交量分不改；
  - 回測分不改；
  - L1-L10 階梯不改；
  - 止損 / 保盈公式不改；
  - 最終排行榜權重仍是成交量20% + 波動15% + 密集區30% + 回測10% + 中線入場25% - 風險扣分。
- 波動分由舊「中等波動最高、過高扣分」改為使用者指定的單調遞增：
  - `abs(24h漲跌幅) = 0%` → 0 分；
  - `abs(24h漲跌幅) = 10%` → 50 分；
  - `abs(24h漲跌幅) >= 20%` → 100 分；
  - 中間按線性比例計算；20% 以上封頂 100 分。
- 新波動分100公式：`clamp(abs_24h_change_pct / 20.0 * 100, 0, 100)`。
- 風險仍由 `risk_penalty` 獨立扣分；本次只改波動分，不把高波動風險混入波動分。

## A/B sync
- A 端新增 `VOLATILITY_SCORE_CONFIG`，明確標示 `basis = monotonic_abs_24h_change`。
- B 端 `volatility_score_100_value()` 同步使用同一公式。
- `/api/system/formula-audit` 新增 `ranking_score.volatility_score.config.basis = monotonic_abs_24h_change`。
- A/B checks 新增：
  - `volatility_score_basis`；
  - `volatility_score_monotonic_low_high`。

## Safety
- 未修改下單 endpoint、真實模式守門、read-only/safe/no-real-orders 防護。
- 未自動重啟交易、未切換真實模式、未下真實訂單。

## Tests
- Full pytest: `310 passed, 13 skipped`.
- New regression: `test_v186_volatility_monotonic_score.py`.
- 5050 smoke: `/`, `/auto-select`, `/calculator`, `/realtime`, `/audit-center`, `/virtual-account`, `/real-account`, `/control-panel`, `/api/status`, `/api/coins`, `/api/system/formula-audit`, `/api/engine/parameters`, `/api/system/formal-live-readiness`, `/api/binance/daily-performance`, `/api/research/dense-width` all returned HTTP 200 in sandbox.
