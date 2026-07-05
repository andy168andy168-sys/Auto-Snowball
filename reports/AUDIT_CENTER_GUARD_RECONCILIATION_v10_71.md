# Auto Snowball v10.71 audit-center guard reconciliation

Status: formal launch remains blocked.

## What was checked

- Compared cached audit-center DOGEUSDC private account truth with the visible stop-loss / profit-guard logic.
- Checked public Binance DOGEUSDC mark and last price for current market reference.
- Checked release package contents for local-only secret/cache/state files.

## DOGEUSDC result from cached audit-center truth

- Position amount: `32159` DOGEUSDC long.
- Entry price: `0.0772`.
- Cached mark price: `0.07701221`.
- Cached unrealized PnL: `-6.03881702 USDC`.
- L1 max-loss line: `-10 USDC`.
- Distance to close line: `3.96118298 USDC`.
- Profit guard: not active yet.
- Next protection trigger: `+20 USDC`.
- Next protection floor: `+16 USDC`.

Interpretation: L1 stop-loss guard is active because DOGE has an open position. Profit guard is not active until total Binance unrealized PnL reaches the L1 protection trigger.

## Fund-flow summary from cached audit-center truth

Virtual mode symbols checked: DOGEUSDC, WIFUSDC, BNBUSDC, BTCUSDC.

- DOGEUSDC net income: `-63.20609887 USDC`.
- WIFUSDC net income: `+1.39114130 USDC`.
- BNBUSDC net income: `+19.46218023 USDC`.
- BTCUSDC net income: `-41.55461274 USDC`.
- Total cached realized/funding/commission net: `-83.90739008 USDC`.

Daily real win rate remains `不可判定` unless complete flat-to-flat trade, order, and income coverage is available. Open positions are not counted as wins or losses.

## Packaging fix

The uploaded v10.70 zip still contained local-only files. V10.71 repackages the release and excludes local credential/cache/state files.

## Validation

- Targeted audit/guard tests: `15 passed`.
- Full non-browser pytest was attempted but did not complete cleanly in the sandbox, so it is not claimed as full pass evidence.
- Sandbox browser evidence is not valid Mac-local 127.0.0.1:5050 browser E2E evidence.
