# Auto Snowball v10.51 正式上線 Gate 驗證摘要（2026-07-02）

結論：**未達正式真實資金上線標準**。本次沒有下真實訂單，也沒有切換真實交易模式。

## 已通過 / 有證據
- 5050 HTTP：`200`；`/auto-select`：`200`；`/api/market/live`：`200`。
- Runtime version：`10.51`；port_ok：`True`；cwd：`/mnt/data/asnow_v10_51`。
- 排行榜排序：`True`；可見候選：BTCUSDC, ETHUSDC, SOLUSDC, BNBUSDC, XRPUSDC, ADAUSDC, AVAXUSDC, LINKUSDC, DOGEUSDC, TIAUSDC。
- 即時同步 Top rows：`True`；active_count：`4`。
- 公式審計：`True`；A→B sync：`True`；logic：`D+E/v10.51`。
- pytest：完整 `203 passed, 13 skipped`；安全目標套件 `23 passed`。

## 阻擋項目
- actual cwd is not requested Mac workdir; Mac local 5050 cannot be verified from sandbox
- 365-day / ~2190-bar 4H backtest evidence missing for visible candidates
- Binance reconciliation dataQuality is not clean
- Binance account/balance/orders truth unavailable; API keys not set in this sandbox
- fresh mark price WebSocket evidence missing
- formal launch preflight is not satisfied
- browser E2E did not fully pass in sandbox; Chromium blocked localhost, tests skipped
- small-amount grayscale launch requires manual confirmation and remains false

## Preflight blocking_items
- {'item': '正式 API 金鑰已設定', 'ok': False}
- {'item': '即時 Mark Price 新鮮', 'ok': False}
- {'item': '所有可見候選幣有一年 4H 回測實證', 'ok': False}
- {'blocking': True, 'item': '小額灰度需手動確認', 'ok': False}

## 測試日誌
- `/mnt/data/asnow_v10_51_pytest_rs.log`
- `/mnt/data/asnow_v10_51_targeted_safety.log`
- `/mnt/data/asnow_v10_51_browser_e2e.log`
