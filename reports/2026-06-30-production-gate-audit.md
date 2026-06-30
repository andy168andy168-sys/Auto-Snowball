# 2026-06-30 Production Gate Audit

## Status

Not ready for live capital yet.

## Runtime verified

- Active service: `http://127.0.0.1:5050`
- Actual runtime directory: `/Users/andyna/Spyder/auto_snowball_web_v10_38_l1_guard_40_e2e`
- Version observed at runtime: `v10.38`
- Browser sweep passed on `/`, `/auto-select`, `/realtime`, `/audit-center`
- No browser console warnings or errors observed during the final sweep

## Binance and strategy checks

- Binance truth sync passed after read-only refresh
- Mark price freshness gate passed
- Formula audit passed
- Visible candidate coins all carried one-year backtest evidence: `365` days and `2190` 4H bars
- Ranking order was verified as final-score descending
- Home page and auto-select page ranking order stayed synchronized
- Process monitor reported circuit breaker cleared and runtime healthy

## Fixes applied during this audit

1. Fixed market-order quantity normalization so symbols such as `1000BONKUSDC` clamp to Binance `MARKET_LOT_SIZE.maxQty` and no longer risk `-4005 Quantity greater than max quantity.`
2. Fixed launch preflight so it refreshes read-only exchange truth before evaluating freshness, removing the false-red state after restart.

## Validation

```text
python3 -m pytest -q -ra
180 passed, 1 warning in 57.99s
```

## Remaining blockers

- Real Binance API key is intentionally not configured yet
- Small-size gray release / canary confirmation still requires manual user approval

## Safety

- No real mode switch was performed automatically
- No real orders were submitted
- Audit stayed on virtual / read-only verification paths for exchange truth checks
