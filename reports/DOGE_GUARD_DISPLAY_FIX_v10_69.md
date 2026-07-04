# Auto Snowball v10.69 DOGE guard display fix

Status: blocked for formal launch.

## Reason

A DOGE strategy page screenshot showed an unopened strategy displaying placeholder values as if the guard was active:

- stage entry price displayed as `0.00000000`
- stop / guard line displayed while no position was open
- distance to guard line displayed from zero unrealized PnL
- next protection floor displayed before L1 was filled

## Fix

- `build_profit_guard_status()` now returns `mode=not_started` when there is no Binance position amount, no opened stage, and no active protected floor.
- Unopened strategy guard fields now render as `-` / `未啟動` instead of active max-loss or profit-floor numbers.
- L1-L10 stage table renders actual entry price only when the stage is opened and has a positive average price.
- Frontend live refresh applies the same inactive guard rule and no longer reintroduces zero-entry placeholders.
- Existing active-position max-loss and profit-floor behavior is preserved.
- Release zip was repacked without local credential/cache/state files.

## Validation

- Targeted DOGE / guard regression: `12 passed`.
- Non-browser pytest subset: `273 passed, 6 skipped`.
- Browser subset: `7 skipped`; this is not Mac-local browser E2E evidence.
- Safe/read-only 5050 smoke returned 200 for `/`, `/strategy/3`, `/api/status`, `/api/system/formula-audit`, `/api/system/runtime`, `/api/system/formal-live-readiness`, and `/api/strategy/3/live`.

Formal launch remains blocked until all Mac-local and signed Binance evidence gates pass.
