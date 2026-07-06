# Auto Snowball v10.73 Test Result

## Changed parameters

- `DEFAULT_MAX_LOSS_PCT`: 10% -> 50%.
- L1 target total floating profit: 20% / 20 USDC -> 50% / 50 USDC, using default 100 USDC capital.
- `FLOATING_ROLL_PROTECTION_RATIO`: 80% -> 50%.
- Default protection triggers: 50 / 100 / 300 / 700 / 1540 USDC.
- Default protection floors: 25 / 50 / 150 / 350 / 770 USDC.
- A->B sync contract now checks dense-zone config, ranking weights, L1 max loss, L1 target total profit, profit protection ratio, and L1 profit floor.

## Validation

- Full pytest: `279 passed, 13 skipped`.
- HTTP/API E2E and launch preflight smoke: `5 passed`.
- Browser Playwright E2E attempted but skipped in this sandbox because Chromium policy blocks localhost navigation with `net::ERR_BLOCKED_BY_ADMINISTRATOR`.

## Safety

- Runtime flags used for validation: `AUTO_SNOWBALL_SAFE_MODE=1`, `AUTO_SNOWBALL_NO_REAL_ORDERS=1`, `AUTO_SNOWBALL_READ_ONLY=1`, `BINANCE_READ_ONLY=1`.
- Formal live-capital launch remains blocked unless all formal live evidence is supplied and passes.
