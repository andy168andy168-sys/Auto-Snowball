# V10.51 — Book stream 重新訂閱修正

## 修正

- 候選 symbols 改變時只重新訂閱與 symbols 相關的 market stream。
- 全市場 `!bookTicker` stream 不再因候選 symbols 改變被標成 `resubscribing`；只有虛擬/真實帳戶模式切換時才重啟。
- `bookTicker` 在泛用 24h ticker 判斷之前分流，恢復 bid/ask 與 spread cache。
- 有效 mark/ticker/kline/book 事件會原子恢復 stream 狀態為 `connected` 並清除舊錯誤。
- 新增 book payload 與 symbols refresh 行為回歸測試。

## 同步契約

- Runtime、公式標籤、API payload、README、release manifest 與版本測試同步到 V10.51。
- V10.50 的共用 Top-4 UI 與 `renderTop4GridV1050()` 保持不變。
- GitHub Actions、release rebuild 預設版本與工作目錄同步到 V10.51。
- Rebuild 會以 ZIP member basename 辨識並驗證既有安全測試，避免重複注入造成 archive hash 漂移。

## 安全

- 交易公式、風控參數、下單邏輯與帳戶模式未變更。
- 驗證全程使用 safe/read-only/no-real-orders；不包含 API 金鑰與 runtime state。
