# Auto Snowball v10.95 Live-Gate Verification - 2026-07-10

## Runtime truth
- Actual `127.0.0.1:5050`: v10.94 at `/Users/andyna/Spyder/auto_snowball_web_v10_94_cross_version_state_persistence`, pid 1413.
- v10.95 is an undeployed candidate; no restart, real-mode switch, real order, or parameter change was performed.

## Fixed vulnerabilities
- v10.94 could silently skip startup state recovery because `load_roll_engine_state()` evaluated `now_str()` before that helper was defined.
- A stale runtime-local snapshot always won over a newer shared snapshot.
- A local-only write could report cross-version persistence success after the shared write failed.
- Fixed in v10.95 with initialization-safe timestamps, newest-valid-snapshot selection, peer-copy healing, shared-write success semantics, unique temporary files, and regression tests.

## Validation
- Targeted state persistence/recovery/idempotency: 12 passed.
- Full candidate pytest: 348 passed.
- Browser/E2E: 13 passed.
- Exact extracted archive pytest: 348 passed.
- All 10 visible candidates had 2190 4H bars and 365-day evidence.

## Formal blockers
- Safe verification environment variables were not set on the live runtime process.
- Reconciliation `dataQuality.ok=false`: XRPUSDC and BNBUSDC private commission/leverage/trades/income/orders coverage failed.
- `正式 API 金鑰已設定=false`.
- `小額灰度需手動確認=false`.
- Actual 5050 remains v10.94; v10.95 has not been deployed.

## Daily performance and dense-width research
- Virtual account: determinable after read-only refresh; recent 10 = 5 wins / 50%; rolling 10 windows = 14, 7-win ratio 0%, 8-win ratio 0%.
- Real account: `不可判定` because private full-account history coverage is incomplete.
- Dense width refresh was read-only and changed no parameter. All six widths met the research candidate threshold, but recent real-trade comparison remains `不可判定`.
