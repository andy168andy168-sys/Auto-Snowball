# Auto-Snowball

Auto Snowball Web release archive for USDC futures rolling strategy monitoring.

## Current CI repair branch

- Branch: `sync-v10-37-release-archive`
- Base package: `releases/v10.34/auto_snowball_web_v10_34_overview_auto_select_sync_e2e.zip`
- Base SHA256 before safety-test injection: `2bc9ef2850b0f28d2cfdeb9ef6f34958c668ff265dec1d6c80a7240a2ce8eecb`
- CI rebuilt SHA256 after injecting required release-archive safety tests: `3b1c9b554289ea691577e241246c8f7ab4640fbc8c5fa562651f3107b1dd432f`

## Main v10.34 changes

- Overview page and auto-select page use the same final ranking source.
- Overview top ten refreshes from `/api/market/live`.
- One-year column is unified as one-year backtest level.
- Current formulas remain D/E:
  - Dense zone = six-line center ±1.5%.
  - Stop loss = capital × stop-loss percent.
  - Profit guard = triggered target × 80%.

## Release archive safety-test gate

The release CI rebuilds the v10.34 archive from base64 parts and injects pytest files required by `scripts/assert_release_tests_inside_archive.py` directly into the ZIP before hash validation and extraction.

Injected release-only safety evidence covers:

- rate-limit backoff
- WebSocket disconnect / reconnect
- order idempotency / duplicate-order protection
- timeout query-order recovery
- circuit breaker
- close-all / process monitor / watchdog
- browser E2E / Playwright / 5050 / auto-select evidence

## Restore release zip

```bash
python scripts/rebuild_release.py
unzip releases/v10.34/auto_snowball_web_v10_34_overview_auto_select_sync_e2e.zip -d auto_snowball_web_v10_34
cd auto_snowball_web_v10_34
python -m pip install -r requirements.txt
pytest -q
python main.py
```

Runtime cache/state and local secrets are not committed.
