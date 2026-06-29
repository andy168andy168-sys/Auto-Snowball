# Auto-Snowball

Auto Snowball Web v10.34 release archive for Binance USDC futures rolling strategy monitoring.

## Current uploaded version

- Version: v10.34
- Package: `releases/v10.34/auto_snowball_web_v10_34_overview_auto_select_sync_e2e.zip`
- SHA256: `2bc9ef2850b0f28d2cfdeb9ef6f34958c668ff265dec1d6c80a7240a2ce8eecb`

## Main v10.34 changes

- Overview page and auto-select page use the same final ranking source.
- Overview top ten refreshes from `/api/market/live`.
- One-year column is unified as one-year backtest level.
- Current formulas remain D/E:
  - Dense zone = six-line center ±1.5%.
  - Stop loss = capital × stop-loss percent.
  - Profit guard = triggered target × 80%.

## Restore release zip

The zip is stored as base64 parts under `releases/v10.34/parts/`.

```bash
python scripts/rebuild_release.py
unzip releases/v10.34/auto_snowball_web_v10_34_overview_auto_select_sync_e2e.zip -d auto_snowball_web_v10_34
cd auto_snowball_web_v10_34
python -m pip install -r requirements.txt
pytest -q
python main.py
```

Runtime cache/state and API secrets are not committed. Use local environment variables or local ignored config for Binance credentials.
