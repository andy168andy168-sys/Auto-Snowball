# CHANGELOG v10.49

## Scope

Workspace/tooling patch for the V10.48 formal-launch audit. The current application release remains V10.50, and this patch does not change trading formulas or trading mode.

## Fixed

- Replaced retired dense-zone and L1 constants with runtime relationship checks.
- Added explicit validation of the formula-audit A→B synchronization payload.
- Increased browser navigation tolerance to 30 seconds while keeping `load` plus a short observation window.
- Added a 30-second timeout for formal launch-preflight evidence generation.
- Added a V10.48 browser overlay that reuses a listening port 5050 process instead of starting a duplicate server.

## Safety

- No order logic, credentials, or trading mode were changed.
- No real orders were submitted and real mode was not enabled.
- Formal launch remains blocked by `正式 API 金鑰已設定` and `小額灰度需手動確認`.
