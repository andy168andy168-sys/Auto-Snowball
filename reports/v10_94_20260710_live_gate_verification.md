# Auto Snowball v10.94 Live Gate Verification - 2026-07-10

## Confirmed issue

The active v10.93 runtime directory was started without the v10.92 state snapshot. v10.92 had ORDIUSDC at L2 with L1/L2 opened and orderId 121852122; v10.93 loaded only its own snapshot and Binance recovery conservatively rebuilt L1 because position quantity cannot reliably infer stage. This explains the observed L2 to L1 reset.

## Fix

v10.94 writes roll-engine state to both the versioned runtime directory and `~/.local/state/auto-snowball/.roll_engine_state.json`. A fresh versioned runtime with no local snapshot loads the shared snapshot and preserves opened stages/order IDs before Binance truth reconciliation.

## Validation

- v10.94 runtime pytest: `343 passed, 1 warning in 34.13s`.
- Targeted persistence/recovery: `7 passed`.
- Independent browser/E2E: `14 passed, 1 warning in 34.98s`.
- Exact extracted archive pytest: `343 passed in 43.65s`.
- Package SHA256: `a8674cc8c4033d58a41dc2e4de9459474c13a5360341b49472283fad1307b67f`.
- ZIP forbidden-artifact scan: no credentials, cache/state, formal evidence, Python/pytest cache, logs, databases, or git metadata.

## Formal status

Actual 5050 remains v10.93 at `/Users/andyna/Spyder/auto_snowball_web_v10_93_fresh_centerline_cycle_guard`; v10.94 is a candidate only and was not restarted. Formal launch remains blocked by `正式 API 金鑰已設定=false` and `小額灰度需手動確認=false`. No real order or mode switch occurred.
