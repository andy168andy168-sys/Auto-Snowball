# CHANGELOG v10.83 — Volume Percentage Fairness

## Changed
- 成交量分由舊的「24h 絕對成交額排名 50% + 7日平均排名 30% + 今日活躍度排名 20%」改為百分比公平化。
- 新成交量分100：
  - `1日/7日活躍度` 40%；
  - `7日/14日短期增長` 25%；
  - `14日/30日中期增長` 20%；
  - `30日基礎流動性` 15%；
  - 再乘 `流動性保護係數 = 0.5 + 0.5 × Base30Score / 100`。
- 1日、7日、14日、30日平均成交額均以 4H quoteVolume 計算：6 / 42 / 84 / 180 根 4H K 線。
- 百分比轉分公式：70% 以下 0 分、100% = 50 分、200% 以上 100 分。
- 30日基礎流動性用 log10 scale，10M USDC/日以下 0 分，100M USDC/日以上 100 分。

## A/B sync
- A 端新增 `VOLUME_SCORE_CONFIG`，明確列出 1/7/14/30 日窗口、權重、百分比門檻、30日流動性門檻及保護係數。
- B 端新增/同步：`volume_percentage_fairness_payload()`、`volume_growth_score()`、`base30_liquidity_score()`、`apply_volume_score_normalization()`。
- `/api/system/formula-audit` 暴露 `ranking_score.volume_score.config.basis = percentage_fairness`。
- 兼容舊欄位：`volume_24h_rank_score_100`、`volume_7d_rank_score_100`、`volume_activity_score_100` 仍保留，但含義改為新百分比分項對應輸出。

## Safety
- 未修改下單 endpoint、真實模式守門、read-only/safe/no-real-orders 防護。
- 未自動重啟交易、未切換真實模式、未下真實訂單。

## Tests
- Full pytest: `297 passed, 13 skipped`.
- 5050 smoke: `/`, `/auto-select`, `/calculator`, `/realtime`, `/audit-center`, `/virtual-account`, `/real-account`, `/control-panel`, `/api/status`, `/api/coins`, `/api/system/formula-audit`, `/api/engine/parameters`, `/api/system/formal-live-readiness` all returned HTTP 200 in sandbox.
