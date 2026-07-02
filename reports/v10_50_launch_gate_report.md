# V10.50 Launch Gate Report - NOT READY FOR LIVE CAPITAL

Run time: 2026-07-02T10:25:10+08:00

## Runtime and browser

- Actual runtime: `127.0.0.1:5050`, version `10.50`.
- Runtime cwd: `/Users/andyna/Spyder/auto_snowball_web_v10_50_overview_top4_shared_ui_e2e`.
- Root, auto-select and market API returned HTTP 200.
- Browser E2E passed with no console/page errors.

## Ranking, live data and backtest evidence

- Ten visible candidates were sorted by descending score with ranks 1-10.
- Two snapshots confirmed live price/updated-at advancement.
- Every visible candidate, including `1000BONKUSDC`, had 365 days and 2190 4H bars.

## Formula, reconciliation and safety evidence

- Formula audit and dense-zone A-to-B synchronization passed.
- Dense-zone half width is 1%, total width is 2%; L1/profit floor is 80% of trigger; default stop loss is 10% of capital.
- Binance reconciliation reported account, balance, orders and data quality healthy.
- Rate-limit backoff, reconnect, idempotency/duplicate guard, timeout query-order recovery, circuit breaker, close-all and watchdog tests passed.
- Full pytest: `213 passed`; targeted production-safety tests: `25 passed`; live Playwright E2E: `1 passed`.

## Blocking items

- `正式 API 金鑰已設定`
- `小額灰度需手動確認`

The formal preflight is therefore `ok=false`. No real order was sent and live mode was not enabled.
