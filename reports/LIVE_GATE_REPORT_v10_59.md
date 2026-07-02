# Auto Snowball V10.59 Live Gate Report

Conclusion: **not ready for real-capital production launch**. No real orders were placed and no real trading mode was enabled.

## Passed evidence

- 5050 HTTP smoke: `/` 200, `/auto-select` 200, `/realtime` 200, `/api/market/live` 200, `/api/realtime` 200.
- Runtime: version `10.59`, port `5050`, host_ok `true`, port_ok `true`.
- Ranking sorted by score: `true`; visible candidates: 10.
- Active top rows count: 4.
- Formula audit: ok `true`, logic `D+E/v10.59`, A-to-B sync `true`.
- Tests: targeted security/read-only `23 passed`; non-browser pytest `237 passed`.
- Security smoke: evil Host `403`, no-Origin POST `403`, same-site POST `403`, same-origin POST `200`, local header POST `200`.

## Blocking items

- Runtime cwd is `/mnt/data/asnow_v10_59_audit/auto_snowball_web_v10_58_ci_smoke_live_gate_hardening`, not `/Users/andyna/Documents/自動滾倉系統設計`.
- Browser E2E was skipped in the sandbox, so it is not a full pass.
- 365-day / about 2190-bar 4H backtest evidence is missing for visible candidates: BTCUSDC, ETHUSDC, SOLUSDC, BNBUSDC, XRPUSDC, ADAUSDC, AVAXUSDC, LINKUSDC, DOGEUSDC, TIAUSDC.
- Binance signed account/balance/orders reconciliation is unavailable in this sandbox because production API keys are not set here.
- Fresh Mark Price WebSocket evidence is missing.
- Formal launch preflight is not satisfied.
- Safe/read-only/no-real-orders lock is still active.
- Manual small-canary approval is not confirmed.
