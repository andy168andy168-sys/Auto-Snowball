# CHANGELOG v10.95 - Cross-Version State Consistency Guard

## Fixed
- 修復 v10.94 啟動載入共享快照時，`now_str()` 尚未定義而被靜默略過的問題。
- 本版本與共享快照同時存在時，現在驗證兩份 JSON 並依 `saved_at` 選擇最新狀態；相同時間優先版本外共享快照。
- 載入最新快照後會修復另一份缺失或較舊的副本，避免版本回切時 L3 倒退成舊 L2。
- 共享快照寫入失敗時 `save_roll_engine_state()` 不再因本地檔成功而誤報成功。
- 每次原子寫入使用唯一暫存檔，避免不同程序共用固定 `.tmp` 名稱。

## Validation
- Targeted persistence/recovery/idempotency: `12 passed`.
- Full runtime pytest: `348 passed in 37.35s`.
- Browser/E2E suite: `13 passed in 22.63s`.

## Safety and deployment
- 未自動重啟或部署目前 `127.0.0.1:5050`；現行 runtime 仍是 v10.94。
- 未切換真實模式、未下真實訂單、未修改密集區參數。
- 正式上線仍受 API 金鑰、小額灰度及本次 Binance 對帳資料品質阻擋。
