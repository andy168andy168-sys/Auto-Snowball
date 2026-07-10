# Auto Snowball v10.96 Live-Gate Verification - 2026-07-10

## Runtime truth
- Actual `127.0.0.1:5050`: v10.94 at `/Users/andyna/Spyder/auto_snowball_web_v10_94_cross_version_state_persistence`, pid 1413.
- v10.96 is an undeployed candidate. No restart, mode switch, parameter update, or real order was performed.

## Fixed
- `ARMED_L1` plans no longer disappear when ranking rotation moves the symbol outside the latest top four.
- Armed plans retain one of the same four execution slots until breakout/open or explicit cycle reset.
- pytest state writes are isolated from production shared state.
- Legacy `TESTUSDC` events are removed when loading state.

## Validation
- Targeted retention/centerline/persistence/idempotency: 20 passed.
- Full candidate pytest: 351 passed.
- Browser/E2E: 13 passed.
- Exact extracted archive pytest: 351 passed.
- Forbidden artifact scan: 0.
- All 10 visible candidates had 2190 4H bars / 365 days.

## Current formal blockers
- Safe verification environment variables are not set on actual 5050.
- Reconciliation `dataQuality.ok=false`: XRPUSDC and BNBUSDC private fee/leverage/trades/income/orders coverage failed.
- `正式 API 金鑰已設定=false`.
- `交易所真值新鮮=false` and `即時 Mark Price 新鮮=false` were observed during the final local gate run.
- `小額灰度需手動確認=false`.
- Actual 5050 remains v10.94; v10.96 has not been deployed and has no live armed-to-breakout evidence.

## Daily performance
- Virtual: 可判定. Recent 10 = 5 wins / 50%; 13 rolling windows, 7-win ratio 0%, 8-win ratio 0%.
- Real: 不可判定 because private full-account trade/order/income coverage is incomplete.

## Dense-width research
- Read-only; runtime parameters unchanged.
- All widths met the research threshold in this refresh: 1.0% 75.19% (133 validation), 1.5% 73.29% (146), 2.0% 72.39% (163), 2.5% 73.94% (165), 3.0% 75.14% (177), 4.0% 73.96% (192).
- Recent real-trade difference remains 不可判定.
