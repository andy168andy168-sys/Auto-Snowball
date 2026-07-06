# Auto Snowball v10.74

## UI label clarity fix

- Renames the ranking table column from `六線密集距離` to `六線分散距離` to avoid confusing the MA/EMA six-line spread with the trading dense-zone width.
- Adds `交易密集區寬度 3.00%` under the dense-zone bounds display.
- Keeps the trading formula unchanged: dense zone remains six-line center ±1.5% / total width 3.00%.
- Adds formula-audit display-label contract so A/B UI labels and B-side formula payload stay synchronized.

## Safety

- No live parameters changed.
- No real orders, restarts, or live-mode switches are authorized by this release.
- Formal live-capital launch remains blocked until Mac-local browser E2E, signed Binance reconciliation, one-year 4H evidence, dense-width validation, formal preflight and user-approved canary all pass.
