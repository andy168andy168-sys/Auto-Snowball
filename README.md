# Auto-Snowball

Auto Snowball Web release archive for USDC futures rolling strategy monitoring.

## Current release target

- Release version: `v10.43`
- Release manifest: `releases/v10.43/manifest.json`
- Release archive filename: `auto_snowball_web_v10_43_candidate_history_gate.zip`
- Source package SHA256 before safety-test injection: `4cb6161ec59e8635439a78c2a48561ed722b55722acaab579ead64d98add1072`
- CI mode: safe / read-only only

## Main v10.43 changes

- GitHub Actions release CI now targets the complete `v10.43` manifest and seven base64 parts.
- Visible non-held candidates with less than 365 days / 2190 bars of 4H history are excluded before ranking; held symbols remain visible and launch-blocking.
- The release includes `backtest_evidence_v10_43.json` for the active and cold-start candidate sets using the runtime's machine-readable 365-day / 2190-bar / 4H evidence contract.
- Cold-start fallback replaces unavailable `TONUSDC` with `TIAUSDC`, whose USDⓈ-M Futures 4H history meets the one-year minimum.
- Overview and auto-select use the same final ranking source.
- Reconciliation evidence exposes structured data-quality status and concrete per-symbol issues.
- Runtime rendering avoids first-paint blocking while evidence APIs still enforce full hydration.
- This sync does not approve real trading.

## Release archive safety-test gate

The release CI rebuilds the `v10.43` archive and injects pytest files required by `scripts/assert_release_tests_inside_archive.py` directly into the ZIP before hash validation and extraction.

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
AUTO_SNOWBALL_RELEASE_VERSION=v10.43 python scripts/rebuild_release.py
unzip releases/v10.43/auto_snowball_web_v10_43_candidate_history_gate.zip -d auto_snowball_web_v10_43
cd auto_snowball_web_v10_43
python -m pip install -r requirements.txt
pytest -q
python main.py
```

Runtime cache/state and local-only files are not committed.
