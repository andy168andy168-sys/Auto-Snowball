# Auto Snowball V10.58 Live Gate Report

Conclusion: **not ready for real-capital production launch**. No real orders were placed and no real trading mode was enabled.

## Passed evidence

- 5050 HTTP smoke: `/` 200, `/auto-select` 200, `/api/market/live` 200.
- Runtime: version `10.58`, port `5050`, host_ok `True`.
- Ranking sorted by score: `True`; visible candidates: `10`.
- Active Top rows sync: `True`; active_count `4`.
- Formula audit: ok `True`, logic `D+E/v10.58`, A-to-B sync `True`.
- Tests: targeted security/CI `30 passed`; non-browser pytest `233 passed`.
- Security smoke: evil Host `403`, no-Origin POST `403`, same-site POST `403`, same-origin POST `200`.

## Blocking items

- Runtime cwd is `/mnt/data/asnow_v10_58_audit`, not the requested Mac workdir `/Users/andyna/Documents/auto-roll-system-design`.
- 365-day / about 2190-bar 4H backtest evidence is missing for visible candidates.
- Binance reconciliation data quality is not clean.
- Fresh mark-price websocket evidence is missing.
- Formal launch preflight is not satisfied.
- Browser E2E was skipped in the sandbox, so it is not a full pass.
- Small-canary launch approval is not confirmed.

## Preflight blockers

- Safe/read-only lock is still active.
- Production credentials are not available in this sandbox.
- Fresh mark-price evidence is missing.
- One-year 4H backtest evidence is missing.
- Manual small-canary approval is still false.
