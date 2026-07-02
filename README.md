# Auto-Snowball

Auto Snowball Web release archive for USDC futures rolling strategy monitoring.

## Current audit target

- Latest audited local package: `v10.58`
- Latest generated archive: `auto_snowball_web_v10_58_ci_smoke_live_gate_hardening.zip`
- Archive SHA256: `7de0beb77ea7f8daec4c539dfe78610a982e450756ff9d971bcb5200d8ff1521`
- CI mode: safe / read-only only
- Formal live-capital status: **blocked**. Do not enable real trading until Mac-local 5050 browser E2E, signed Binance reconciliation, 365-day / ~2190 4H backtest evidence, formal preflight, and manual small-canary approval all pass.

## Main v10.58 changes

- Fixed the GitHub Actions `python-package-conda.yml` failure where the workflow tried to run `conda env update --file environment.yml` even though `environment.yml` is not present.
- Replaced the legacy conda smoke workflow with Python 3.11, `requirements.txt`, pytest and flake8 under safe/read-only/no-real-orders environment flags.
- Preserves v10.57 localhost DNS-rebinding, same-site CSRF, and provenance workflow hardening.
- Local validation: targeted security/CI gate `30 passed`; non-browser pytest `233 passed`; browser E2E `13 skipped` in the sandbox environment.
- This GitHub sync does not approve or enable real trading.

## Recent hardening history

- v10.57: Blocks `Sec-Fetch-Site: same-site` without Origin for localhost control writes and rebuilds the release archive before provenance attestation when the zip is not committed.
- v10.56: Blocks non-localhost Host headers to prevent DNS rebinding and rejects no-Origin POST writes unless the local-control header is present.
- v10.55: Forces localhost-only bind, POST-only runtime writes, GET no-mutation gate, credential chmod 600, and build provenance attestation.
- v10.54: Enforces safe/read-only/no-real-orders runtime gates before signed Binance writes.

## Restore / run local package

```bash
unzip auto_snowball_web_v10_58_ci_smoke_live_gate_hardening.zip
cd auto_snowball_web_v10_58_ci_smoke_live_gate_hardening
python -m pip install -r requirements.txt
AUTO_SNOWBALL_SAFE_MODE=1 AUTO_SNOWBALL_NO_REAL_ORDERS=1 AUTO_SNOWBALL_READ_ONLY=1 BINANCE_READ_ONLY=1 python -m pytest -q
AUTO_SNOWBALL_SAFE_MODE=1 AUTO_SNOWBALL_NO_REAL_ORDERS=1 AUTO_SNOWBALL_READ_ONLY=1 BINANCE_READ_ONLY=1 PORT=5050 python main.py
```

Runtime cache/state and local-only files must not be committed. Real trading requires a separate user-approved production run and all launch gates passing.
