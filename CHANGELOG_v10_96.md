# CHANGELOG v10.96 - Armed Tracking Retention Guard

## Fixed
- 已觸及／穿越中線並進入 `ARMED_L1` 的幣，不再因排行榜輪替跌出前四而刪除追蹤狀態。
- 已武裝幣會保留一個執行槽位；排行榜只補入剩餘槽位，總執行計畫仍不超過四個。
- 保留 `zone_entered`、`zone_entered_at`、上一口 Mark Price 與最新密集區上下沿，繼續等待後續突破開 L1。
- pytest 使用獨立共享狀態路徑，不再寫入真實 `~/.local/state/auto-snowball/.roll_engine_state.json`。
- 載入舊快照時移除既有 `TESTUSDC` 測試事件污染。
- 共享狀態路徑支援 `AUTO_SNOWBALL_ENGINE_STATE_FILE` 與 `XDG_STATE_HOME`。

## Validation
- Armed retention / centerline / persistence / order-cycle targeted tests: `20 passed`.
- Full runtime pytest: `351 passed in 37.99s`.
- Browser/E2E suite: `13 passed in 32.66s`.

## Safety and deployment
- 未修改、重啟或部署目前 `127.0.0.1:5050`；現行 runtime 仍為 v10.94。
- 未切換真實模式、未下真實訂單、未修改密集區參數。
- v10.96 是候選版本，須另行部署後觀察真實「中線武裝 → 後續突破 → L1」事件證據。
