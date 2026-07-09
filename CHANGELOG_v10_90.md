# CHANGELOG v10.90 - Centerline Crossing Guard

## Fixed
- Preserved the previous WebSocket mark price in the live mark-price cache.
- Propagated `previousMarkPrice` into live candidate rows before dense-zone distance and centerline status are calculated.
- A live price that crosses the dense-zone centerline from above or below now marks the row as `已進入中線` and `中線：已觸及`.

## Packaging
- Excluded local `formal_live_evidence.json` from release archives to avoid shipping stale machine-local launch evidence.
- Added release-tooling regression coverage for the exclusion.

## Unchanged
- No ranking weights changed.
- No dense-zone width or trading parameter changed.
- No L1-L10, stop-loss, profit-guard or order path changed.
- No runtime trading mode was switched.
- No real order was placed.

## Formal-Live Status
- Not formally live-ready.
- Current 5050 is still running v10.89 until an operator explicitly approves restart/deploy.
- Current 5050 preflight remains blocked by missing formal API credentials and missing manual small-canary approval.
