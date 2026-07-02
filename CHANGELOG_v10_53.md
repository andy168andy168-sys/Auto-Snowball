# V10.53 — Dynamic refresh gate regression fix

## Fixed

- Removed an accidental Playwright block from `validate_market_refresh()` that referenced undeclared `sync_playwright`, `errors`, and `urls` values.
- Restored the intended read-only comparison of consecutive `/api/market/live` snapshots.
- The refresh gate now validates the second snapshot, requires common symbols, and passes only when a tracked live field or `updated_at` advances.

## Regression coverage

- A newer `updated_at` timestamp with synchronized rows passes.
- A live-price change with the same timestamp passes.
- An unchanged snapshot fails closed.

## Scope and safety

- V10.53 is a repository-side launch-gate tooling patch. The audited application runtime remains V10.51.
- No trading formula, risk parameter, order path, account mode, runtime release archive, or Binance write behavior changed.
- Verification remained safe/read-only/no-real-orders.
