# CHANGELOG v10.93 - Fresh Centerline Cycle Guard

## Fixed
- 無持倉幣只有「現價先觸及/穿越密集區中線」才會啟動本輪 L1 等待。
- 已觸及中線後，排行榜 / live row 會保留 engine 的 `ARMED_L1` 狀態，顯示「中線已觸及，等待密集區突破」；不再因現價短暫離開中線而誤顯示未到中線。
- `prepare_execution_plans()` 不再因展示 row 的 `dense_entry_ready` / `execution_eligible` 直接武裝計畫，避免系統沒有記錄真實穿越就進入可買入狀態。
- 完成賣出 / 平倉後，計畫會重置為 `WAITING_CENTERLINE`，下一輪必須重新等待現價觸及或穿越中線。

## Unchanged
- 真正買入仍必須在已武裝後，由後續價格突破密集區上沿或下沿才開 L1。
- 密集區寬度、六線、距離、L1-L10、止損、保盈、排行榜權重與 Binance 下單守門不變。
- 密集區寬度研究仍只提出建議，不自動修改執行中參數。

## Safety
- 未自動重啟 `127.0.0.1:5050`。
- 未切換真實模式。
- 未下真實訂單。
