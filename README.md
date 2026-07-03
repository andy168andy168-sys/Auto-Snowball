# Auto-Snowball

Auto Snowball Web release archive for USDC futures rolling strategy monitoring.

## Current audit target

- Latest audited candidate package: `v10.63`
- Actual 5050 runtime during the 2026-07-03 audit: Spyder `v10.63`
- Latest generated archive: `auto_snowball_web_v10_63_normalized_scores_ui_redesign_e2e.zip`
- Archive SHA256: `0e7157cd2f484d4e97f23ab9628e3a7d9099e9c02fe2657ea923a4d226476059`
- CI mode: safe / read-only only
- Formal live-capital status: **blocked**. Do not enable real trading until Mac-local 5050 browser E2E, signed Binance reconciliation, 365-day / ~2190 4H backtest evidence, formal preflight, and manual small-canary approval all pass.

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
- This GitHub sync does not approve or enable real trading.

## Recent hardening history

- v10.58: Fixed the legacy CI smoke workflow that depended on missing `environment.yml`; uses Python 3.11, `requirements.txt`, pytest and flake8 under safe/read-only/no-real-orders flags.
- v10.57: Blocks `Sec-Fetch-Site: same-site` without Origin for localhost control writes and rebuilds the release archive before provenance attestation when the zip is not committed.
- v10.56: Blocks non-localhost Host headers to prevent DNS rebinding and rejects no-Origin POST writes unless the local-control header is present.
- v10.55: Forces localhost-only bind, POST-only runtime writes, GET no-mutation gate, credential chmod 600, and build provenance attestation.
- v10.54: Enforces safe/read-only/no-real-orders runtime gates before signed Binance writes.

## Restore / run local package

```bash
unzip auto_snowball_web_v10_63_normalized_scores_ui_redesign_e2e.zip
cd auto_snowball_web_v10_63_normalized_scores_ui_redesign_e2e
python -m pip install -r requirements.txt
AUTO_SNOWBALL_SAFE_MODE=1 AUTO_SNOWBALL_NO_REAL_ORDERS=1 AUTO_SNOWBALL_READ_ONLY=1 BINANCE_READ_ONLY=1 python -m pytest -q
AUTO_SNOWBALL_SAFE_MODE=1 AUTO_SNOWBALL_NO_REAL_ORDERS=1 AUTO_SNOWBALL_READ_ONLY=1 BINANCE_READ_ONLY=1 PORT=5050 python main.py
```

Runtime cache/state and local-only files must not be committed. Real trading requires a separate user-approved production run and all launch gates passing.
