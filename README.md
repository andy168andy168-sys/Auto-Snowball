# Auto-Snowball

Auto Snowball Web release archive for USDC futures rolling strategy monitoring.

## Current audit target

- Latest generated candidate package: `v10.74`
- Mac-local `127.0.0.1:5050` runtime: not externally verified by this connector environment; must be checked on the operator Mac before approval.
- Latest generated archive: `auto_snowball_web_v10_74_ui_label_clarity_e2e.zip`
- Archive SHA256: `4bbd3b78a850d7130e96d07d8f40fc6d8d3b59dc90e1b11ed34787cc51271db9`
- CI mode: safe / read-only only
- Formal capital status: **blocked**. Mac-local 5050 browser E2E, signed Binance reconciliation, 365-day / ~2190 4H backtest evidence, dense-width validation, formal preflight, and manual small-canary approval are still required.

## Main v10.74 changes

- UI label clarity fix only: `六線密集距離` is renamed to `六線分散距離`.
- The dense-zone bounds column now separately displays `交易密集區寬度 3.00%`.
- Trading dense-zone formula remains unchanged: six-line center ±1.5%, total width 3.00%.
- L1 logic, stop-loss logic, profit-protection logic, order-cycle logic, restart behavior, and mode behavior were not changed.
- Local validation: full pytest `281 passed, 13 skipped`; targeted UI/version regression `10 passed`; HTTP smoke on safe local port 5055 returned 200 for `/strategy/1`, `/auto-select`, and `/api/system/formula-audit`.
- Formal launch remains blocked by missing Mac-local browser E2E, signed Binance reconciliation, one-year 4H evidence for all visible candidates, dense-width validation, preflight and user-approved small-canary evidence.

## Main v10.73 changes

- Changes L1 max loss from 10% to 50%; with default 100 USDC capital the close-all loss line is -50 USDC.
- Changes L1 target total floating profit from 20% / 20 USDC to 50% / 50 USDC.
- Changes profit-protection ratio from 80% to 50%; L1 protection floor becomes +25 USDC, with L2-L5 floors +50 / +150 / +350 / +770 USDC.
- Extends the A-to-B sync contract to cover L1 max loss, L1 target total profit, profit-protection ratio and L1 protection floor.
- Validation evidence in the uploaded package: full pytest `279 passed, 13 skipped`; HTTP/API E2E and launch preflight smoke `5 passed`; Browser Playwright E2E was attempted but skipped in the sandbox due to Chromium localhost policy, so it is not valid Mac-local 5050 browser evidence.
- Formal launch remains blocked by missing Mac-local browser E2E, signed Binance reconciliation, one-year 4H evidence for all visible candidates, dense-width validation, preflight and user-approved small-canary evidence.

## Main v10.63 changes

- Removes formula derivations, source-priority rules and implementation notes from both templates and dynamic JavaScript rendering.
- Redesigns navigation, live status, cards, tables, controls and responsive layouts.
- Displays volume, volatility, dense-zone, backtest, zone-entry and risk scores on a common 0-100 scale.
- Volume score uses 24h quote-volume rank 50% + seven-day daily-average rank 30% + current activity rank 20%.
- Preserves the requested final formula: volume 20% + volatility 15% + dense zone 30% + backtest 10% + zone entry 25% - risk penalty.
- Local validation: full pytest `265 passed`; safety/resilience `70 passed`; browser E2E `13 passed`; seven-page console/page errors `0`.
- Formal launch remains blocked by missing formal API credentials and missing manual small-size canary approval.

## Main v10.62 changes

- Ranking final score formula updated to: `volume*20% + volatility*15% + dense_zone*30% + backtest*10% + zone_entry*25% - risk_penalty`.
- Every positive ranking factor is converted to a 0-100 percentage score before weighting; positive weights total 100% and risk penalty remains independent with a max deduction of 10.
- `RANKING_SCORE_WEIGHTS`, `RANKING_SCORE_CONFIG`, `calc_strategy_rank_fields()`, A-to-B sync contract, and formula audit payload were updated together.
- Added regression test `test_v165_ranking_score_weight_sync.py`.

## Main v10.61 changes

- Changes the dense zone to six-line center ±1.5%, total width 3%.
- Uses one shared width source for backend formula, ranking, live distance, L1, audit payload, UI and tests.
- Removes formula derivations, implementation notes and source-priority explanations from the user-facing WEB interface.
- Redesigns navigation, live status, cards, tables, controls and responsive layout.
- Local validation: full pytest `258 passed`; safety/resilience suite `59 passed`; browser E2E `6 passed`; five-page console/page errors `0`.
- Formal launch remains blocked by missing formal API credentials, missing manual small-size canary approval, and the current 5050 runtime not loading this packaged UI candidate.

## Main v10.60 changes

- Makes `GET /api/system/launch-preflight` cache-only; signed Binance reconciliation is reserved for explicit same-origin POST control paths.
- Prevents backtest evidence and shared live-row GET paths from scheduling background hydration by default.
- Prevents `GET /api/kline-monitor` from rewriting account truth cache.
- Local validation: full pytest `255 passed`; browser E2E `2 passed`; safety/resilience suite `48 passed`.
- Formal launch remains blocked by missing formal API credentials and missing manual small-size canary approval.

## v10.59 changes

- Fixed a new GET read-side effect vulnerability: server-rendered pages and live JSON endpoints no longer auto-start WebSocket threads from GET requests.
- Fixed GET live endpoint background side effects: `/api/coins` and `/api/market/live` no longer schedule missing line/backtest hydration workers during read requests.
- Fixed strategy read endpoints: `/strategy/<rank>` and `/api/strategy/<rank>/live` no longer rebuild or persist engine plans on GET; they render a display-only copy.
- Fixed symbol truth read endpoint: `/api/binance/symbol-truth/<symbol>` no longer triggers signed Binance reconciliation or truth-cache writes on GET.
- Local validation: targeted security/read-only gate `23 passed`; non-browser pytest `237 passed`; browser E2E `13 skipped` in the sandbox environment.
- This GitHub sync does not approve mode switching.

## Recent hardening history

- v10.58: Fixed the legacy CI smoke workflow that depended on missing `environment.yml`; uses Python 3.11, `requirements.txt`, pytest and flake8 under safe/read-only/no-order flags.
- v10.57: Blocks `Sec-Fetch-Site: same-site` without Origin for localhost control writes and rebuilds the release archive before provenance attestation when the zip is not committed.
