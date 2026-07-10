# CHANGELOG v10.94 - Cross-Version Roll State Persistence

## Fixed

- 修復版本化 runtime 目錄切換後只讀新目錄 `.roll_engine_state.json`，導致 Binance 舊倉無法延續已開啟 L2/L10 的問題。
- 滾倉狀態現在同時保存到 runtime 目錄與版本外 `~/.local/state/auto-snowball/.roll_engine_state.json`。
- 新 runtime 目錄沒有本地快照時會載入版本外快照，保留每一階段的 `opened` 與 `orderId`，再以 Binance 持倉真值校正。

## Validation

- Targeted state persistence/recovery: `7 passed`.
- Full runtime pytest: `343 passed, 1 warning in 34.13s`.
- Independent browser/E2E: `14 passed, 1 warning in 34.98s`.
- Exact extracted archive pytest: `343 passed in 43.65s`.

## Safety

- Actual 5050 remains v10.93; v10.94 was not deployed or restarted.
- No real-mode switch, real order, parameter change, or automatic restart was performed.
- Formal launch remains blocked by the real API credential gate and manual small-canary approval.
