# Auto-Snowball

Auto Snowball Web release archive for USDC futures rolling strategy monitoring.

## Current release target

- Release version: `v10.42`
- Release manifest: `releases/v10.42/manifest.json`
- Release archive filename: `auto_snowball_web_v10_42_release_flat.zip`
- Source package SHA256 before safety-test injection: `f8371c1c485e7dd672dcec7a0d8c36ab0aa600bff4dbe1895dbf37bdca23e7c3`
- CI mode: safe / read-only only

## Main v10.42 changes

- GitHub Actions release CI now targets `v10.42` instead of the old release archive.
- Overview and auto-select use the same final ranking source.
- Reconciliation evidence exposes structured data-quality status and concrete per-symbol issues.
- Runtime rendering avoids first-paint blocking while evidence APIs still enforce full hydration.
- This sync does not approve real trading.

## Release archive safety-test gate

The release CI rebuilds the `v10.42` archive and injects pytest files required by `scripts/assert_release_tests_inside_archive.py` directly into the ZIP before hash validation and extraction.

Injected release-only safety evidence covers:

- rate-limit backoff
- WebSocket disconnect / reconnect
- order idempotency / duplicate-order protection
- timeout query-order recovery
- circuit breaker
- close-all / process monitor / watchdog
- one-year 4H backtest coverage
- formula consistency
- browser E2E / Playwright / 5050 / auto-select evidence

## Restore release zip

```bash
AUTO_SNOWBALL_RELEASE_VERSION=v10.42 python scripts/rebuild_release.py
unzip releases/v10.42/auto_snowball_web_v10_42_release_flat.zip -d auto_snowball_web_v10_42
cd auto_snowball_web_v10_42
python -m pip install -r requirements.txt
pytest -q
python main.py
```

Runtime cache/state and local-only files are not committed.
