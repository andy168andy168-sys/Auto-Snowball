# Auto Snowball v10.93 Live Gate Verification - 2026-07-10

## Runtime truth

- Primary audit workdir: `/Users/andyna/Documents/自動滾倉系統設計`.
- Actual `127.0.0.1:5050`: version `10.93`, cwd `/Users/andyna/Spyder/auto_snowball_web_v10_93_fresh_centerline_cycle_guard`, pid `1414`, started `2026-07-10 14:11:07`.
- Runtime remains virtual mode. No real-mode switch, real order, parameter change, or restart was performed by this audit.

## Validation

- Full runtime pytest: `342 passed, 1 warning in 56.17s`.
- Independent browser/E2E suite: `14 passed, 1 warning in 53.85s`.
- In-app browser actual 5050 scan: /, /auto-select, /realtime, /audit-center, /virtual-account, /real-account, /control-panel, and /calculator all rendered without console errors, page errors, or visible error alerts. /audit-center had a slow initial navigation wait but rendered fully afterward.
- Live HTTP ranking check: 10 rows sorted descending by final score; two samples 3.5 seconds apart showed live price/score changes in 7 rows and preserved price, centerline-entry state, centerline-entry score, and rank fields.
- Safety route probes: cross-site POSTs returned 403; GET trading/dense refresh/reconciliation refresh/action routes returned 405.
- Process monitor: websocket public/book/user threads alive, no stuck tick, circuit breaker closed.
- Formula audit: A-to-B synchronization and six-line/dense-zone/distance/L1/stop-loss/profit-protection checks all passed.

## Backtest evidence

All 10 currently visible candidates, including held-position insertion, expose `2190` 4H bars and `365` lookback days. The local 5050 gate also fetched `2190` public Binance 4H bars for each visible symbol. Formal preflight backtest evidence is `ok=true`.

## Binance reconciliation and daily performance

- Virtual demo-futures signed reconciliation: `account_ok=true`, `balance_ok=true`, `orders_ok=true`, `data_quality_ok=true`, 4 symbols checked.
- Virtual daily performance is `可判定`: 24 complete closed rounds across 2026-07-03 through 2026-07-08. Recent 10 has 5 wins (50.0%); 15 rolling windows have 0.0% at 7 wins and 0.0% at 8 wins. Open positions are excluded.
- Real daily performance and private reconciliation are `不可判定`: no real API credentials and userTrades/income/orders coverage is incomplete. No ranking backtest score is used as real win rate.

## Dense-width research (advisory only)

Read-only 70/30 training/validation refresh completed for all requested widths with no overlapping positions per symbol and current L1-L10/stop-loss/profit-protection logic.

| Width | Total | Validation | Validation win rate | Wins/10 | 7-win ratio | 8-win ratio | Max losing streak |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.0% | 382 | 145 | 74.48% | 7.45 | 72.06% | 61.03% | 6 |
| 1.5% | 441 | 160 | 73.75% | 7.38 | 80.13% | 62.91% | 7 |
| 2.0% | 492 | 176 | 71.02% | 7.10 | 73.05% | 43.11% | 6 |
| 2.5% | 519 | 181 | 74.03% | 7.40 | 75.00% | 50.00% | 4 |
| 3.0% | 548 | 191 | 74.35% | 7.43 | 74.73% | 48.90% | 3 |
| 4.0% | 595 | 204 | 73.53% | 7.35 | 71.79% | 51.79% | 5 |

All six widths satisfy the candidate threshold. Recent real-trade difference remains `不可判定` because real private history is incomplete. No parameter was changed.

## Formal gate

`/api/system/formal-live-readiness` is current and reports only one blocking group: formal preflight is not complete because `正式 API 金鑰已設定=false` and `小額灰度需手動確認=false`. Therefore do not claim `已達正式上線標準`.
