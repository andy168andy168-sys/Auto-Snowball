# Auto-Snowball

Auto Snowball Web release archive for USDC futures rolling strategy monitoring.

## Current audit target

- Latest audited local package: `v10.62`
- Latest generated archive: `auto_snowball_web_v10_62_ranking_score_weights_e2e.zip`
- Archive SHA256: `a721cfb5c3027c00489692da24ff2a2982fcf92bda499fa5e7436f0aefe6e64f`
- CI mode: safe / read-only only
- Formal live-capital status: **blocked**. Do not enable real trading until Mac-local 5050 browser E2E, signed Binance reconciliation, 365-day / ~2190 4H backtest evidence, formal preflight, and manual small-canary approval all pass.

## Main v10.62 changes

- Ranking final score formula updated to: `volume*20% + volatility*15% + dense_zone*30% + backtest*10% + zone_entry*25% - risk_penalty`.
- Every positive ranking factor is converted to a 0-100 percentage score before weighting; positive weights total 100% and risk penalty remains independent with a max deduction of 10.
- `RANKING_SCORE_WEIGHTS`, `RANKING_SCORE_CONFIG`, `calc_strategy_rank_fields()`, A-to-B sync contract, and formula audit payload were updated together.
- Added regression test `test_v165_ranking_score_weight_sync.py`.
- Local validation: targeted ranking/A-B formula tests `30 passed`; full pytest `248 passed, 13 skipped`; 5050 smoke endpoints returned 200.
- This GitHub sync does not approve or enable real trading.

## Recent hardening history

- v10.61: Dense zone updated to center ±1.5%, total width 3%, with A/B formula, audit, ranking, execution plan, frontend labels and E2E tests synchronized.
- v10.60/v10.59: Fixed GET read-side effects so pages and live JSON endpoints do not start WebSocket/background workers or persist engine/truth state.
- v10.58: Fixed the legacy CI smoke workflow that depended on missing `environment.yml`; uses Python 3.11, `requirements.txt`, pytest and flake8 under safe/read-only/no-real-orders flags.
- v10.57: Blocks `Sec-Fetch-Site: same-site` without Origin for localhost control writes and rebuilds the release archive before provenance attestation when the zip is not committed.
- v10.56: Blocks non-localhost Host headers to prevent DNS rebinding and rejects no-Origin POST writes unless the local-control header is present.
- v10.55: Forces localhost-only bind, POST-only runtime writes, GET no-mutation gate, credential chmod 600, and build provenance attestation.

## Restore / run local package

```bash
unzip auto_snowball_web_v10_62_ranking_score_weights_e2e.zip
cd auto_snowball_web_v10_62_ranking_score_weights_e2e
python -m pip install -r requirements.txt
AUTO_SNOWBALL_SAFE_MODE=1 AUTO_SNOWBALL_NO_REAL_ORDERS=1 AUTO_SNOWBALL_READ_ONLY=1 BINANCE_READ_ONLY=1 python -m pytest -q
AUTO_SNOWBALL_SAFE_MODE=1 AUTO_SNOWBALL_NO_REAL_ORDERS=1 AUTO_SNOWBALL_READ_ONLY=1 BINANCE_READ_ONLY=1 PORT=5050 python main.py
```

Runtime cache/state and local-only files must not be committed. Real trading requires a separate user-approved production run and all launch gates passing.
