# V10.50 - Shared Top-4 overview and execution UI

## Web UI

- Adds the Top-4 rolling-coin cards to the overview.
- Uses `_top4_roll_cards.html` and `renderTop4GridV1050()` on both overview and execution-center pages.
- Removes six duplicate execution summary cards and their obsolete live-update targets.
- Removes implementation notes from the reconciliation/audit display while keeping formula and reconciliation guards active.

## Synchronization contract

- Ranking, live price, entry status, entry score and rank use the same live row source.
- Formula/version labels, execution plan and dense-zone A-to-B checks are synchronized to `D+E/v10.50`.

## Safety

- Trading formulas, risk parameters, order logic and account mode are unchanged.
- The release archive excludes Binance API keys and local runtime state.
- This release does not authorize real orders or switching to live mode.
