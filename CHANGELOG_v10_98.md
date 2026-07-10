# CHANGELOG v10.98 — Armed Outside-Zone Entry Deadlock Fix

## Fixed
- 修復 ARMED_L1 已在密集區外時無法開 L1 的 runtime 死鎖。
- 舊邏輯要求上一口仍在區內，今口再穿越上下沿；若武裝當口已跳到區外，之後即使一直在區外亦永遠不會觸發。
- 新邏輯：中線觸及/穿越當口只武裝；由下一個 tick 起，只要現價仍高於最新密集區上沿或低於最新密集區下沿，就視為突破成立並嘗試開 LONG/SHORT L1。
- 保留 ARMED_L1 排名輪替追蹤、四槽位上限及 TESTUSDC 污染隔離。

## Unchanged
- 密集區計算、成交量分、波動分、回測分、L1-L10、止損、保盈、排行榜權重及安全守門全部不改。
- 未切換真實模式，未下真實訂單。
