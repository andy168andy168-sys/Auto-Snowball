# TEST_RESULT v10.93

Validation refreshed by the 2026-07-10 Auto Snowball formal launch-gate automation.

## Result

- Full runtime pytest: `342 passed, 1 warning in 56.17s`.
- Independent browser/E2E suite: `14 passed, 1 warning in 53.85s`.
- Actual 127.0.0.1:5050 in-app browser scan: 8 pages loaded with no console errors, page errors, or visible error alerts. /audit-center exceeded the initial 20-second navigation wait but completed and rendered fully on the same tab; it is recorded as slow-load evidence, not a browser error.
- Actual 5050 endpoint probes: cross-site POST `403`; GET trading, dense-width refresh, reconciliation refresh, and action routes `405`.
- Visible-candidate launch gate: 10 candidates, each with `2190` 4H bars and `365` lookback days.
- Ranking/live synchronization: descending final-score order held across two read-only samples 3.5 seconds apart; 7 of 10 rows changed live price or score while entry status, centerline-entry score, and rank fields remained present.
- Formula audit: `ok=true`, version `10.93`, A-to-B synchronization passed.
- Signed virtual demo reconciliation: account, balance, orders, and data quality all passed for 4 checked symbols.

## Daily performance

- Virtual account: `可判定`; 24 complete closed rounds across 2026-07-03 to 2026-07-08. Recent 10: 5 wins, 50.0%; rolling 10 windows: 15, 7-win ratio 0.0%, 8-win ratio 0.0%. Daily records include realized PnL, opening/closing fees, funding fee, and net PnL; open positions are excluded.
- Real account: `不可判定`; real credentials are absent and private userTrades/income/orders coverage failed. No real win rate is reported and no leaderboard score is substituted.

## Dense-width research

Read-only refresh with 70% training / 30% validation, no overlapping position per symbol, current L1-L10, stop-loss, and profit-protection logic. All six requested widths met the candidate rule (at least 30 complete samples and validation win rate at least 70%):

- 1.0%: 382 total, 145 validation, 74.48% validation win rate, 7.45 wins per 10, 72.06% 7-win ratio, 61.03% 8-win ratio, max losing streak 6.
- 1.5%: 441 total, 160 validation, 73.75%, 7.38, 80.13%, 62.91%, max losing streak 7.
- 2.0%: 492 total, 176 validation, 71.02%, 7.10, 73.05%, 43.11%, max losing streak 6.
- 2.5%: 519 total, 181 validation, 74.03%, 7.40, 75.00%, 50.00%, max losing streak 4.
- 3.0%: 548 total, 191 validation, 74.35%, 7.43, 74.73%, 48.90%, max losing streak 3.
- 4.0%: 595 total, 204 validation, 73.53%, 7.35, 71.79%, 51.79%, max losing streak 5.

Recent real-trade difference is `不可判定` because real private history is incomplete. Widths remain advisory; no runtime parameter was changed.

## Formal launch status

- This report does not approve real-capital launch.
- Actual 5050 runtime is version `10.93` at `/Users/andyna/Spyder/auto_snowball_web_v10_93_fresh_centerline_cycle_guard`.
- Formal readiness is blocked only by `正式 API 金鑰已設定=false` and `小額灰度需手動確認=false`.
- No real mode switch and no real order were performed.
