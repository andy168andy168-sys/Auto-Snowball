# Auto-Snowball

Auto Snowball Web release archive for USDC futures rolling strategy monitoring.

## Current audit target

- Latest audited local package: `v10.59`
- Latest generated archive: `auto_snowball_web_v10_59_get_live_read_only_hardening.zip`
- Archive SHA256: `2e6b3c866640b035344254fe1cd349ee78528c4b174d7d8f6b054938c05190eb`
- CI mode: safe / read-only only
- Formal live-capital status: **blocked**. Do not enable real trading until Mac-local 5050 browser E2E, signed Binance reconciliation, 365-day / ~2190 4H backtest evidence, formal preflight, and manual small-canary approval all pass.

## Main v10.59 changes

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
unzip auto_snowball_web_v10_59_get_live_read_only_hardening.zip
cd auto_snowball_web_v10_59_get_live_read_only_hardening
python -m pip install -r requirements.txt
AUTO_SNOWBALL_SAFE_MODE=1 AUTO_SNOWBALL_NO_REAL_ORDERS=1 AUTO_SNOWBALL_READ_ONLY=1 BINANCE_READ_ONLY=1 python -m pytest -q
AUTO_SNOWBALL_SAFE_MODE=1 AUTO_SNOWBALL_NO_REAL_ORDERS=1 AUTO_SNOWBALL_READ_ONLY=1 BINANCE_READ_ONLY=1 PORT=5050 python main.py
```

Runtime cache/state and local-only files must not be committed. Real trading requires a separate user-approved production run and all launch gates passing.
