# TEST_RESULT v10.94

- Targeted runtime-state persistence/recovery: `7 passed, 1 warning`.
- Full runtime pytest: `343 passed, 1 warning in 34.13s`.
- Independent browser/E2E suite: `14 passed, 1 warning in 34.98s`.
- Exact extracted v10.94 archive pytest: `343 passed in 43.65s`.
- Forbidden credential/cache/runtime-state/formal-evidence scan: passed.

The regression proves a fresh versioned runtime can load a shared snapshot and retain an ORDIUSDC-like L2 `opened=true` stage and its order ID, while existing fresh-L1 and persisted-L3 recovery tests remain passing.

Actual 127.0.0.1:5050 is still v10.93 and was not restarted. Do not claim `已達正式上線標準`; `正式 API 金鑰已設定=false` and `小額灰度需手動確認=false`.
