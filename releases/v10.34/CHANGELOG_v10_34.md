# V10.34 — 總覽 / 自動選幣同步守門

- 修正總覽首頁「自動選幣前十名」仍讀舊 `MARKET_SYNC_CACHE / CANDIDATE_COINS`，導致與 `/auto-select` 不同步的問題。
- 首頁與自動選幣頁統一使用 `build_live_market_rows(mode, limit=10)` 作為同一份最終排行榜資料源。
- 首頁新增 `home-top10-tbody`，前端每秒從 `/api/market/live` 更新，與自動選幣頁同步刷新。
- 首頁一年欄位改為「一年回測層級」，顯示 `backtest_level_score`，避免與舊勝率欄混淆。
- 前端/API 再移除舊同步說明備註文字，保留乾淨顯示。
- Binance 檢查：BNBUSDC 現價與 4H K 線接口可回應；私人持倉/成交/費用仍以本機 API key 對帳中心為準。
- 公式維持最新 D/E：密集區 = 六線中心 ±1.5%；止損 = 本金 × 止損百分比；保盈線 = 激發目標 × 80%。
