# Auto-Snowball

Auto Snowball Web release archive for USDC futures rolling strategy monitoring.

## Current release target

- Release version: `v10.51`
- Release manifest: `releases/v10.51/manifest.json`
- Release archive filename after reconstruction: `auto_snowball_web_v10_51_book_stream_resubscribe_e2e.zip`
- Release archive SHA256: `0801340950d53cff8b11dbe593f813c6514b5440cfa8ee3cc692d1f26421f41b`
- CI mode: safe / read-only only
- Formal live-capital status: blocked until `正式 API 金鑰已設定` and `小額灰度需手動確認` both pass.

## Main v10.51 changes

- Candidate-symbol refreshes resubscribe only symbol-dependent market streams; the all-market `!bookTicker` stream remains connected.
- `bookTicker` payloads are routed before the generic ticker parser, restoring bid/ask and spread caches.
- Valid market events atomically recover stale WebSocket status and clear old errors.
- V10.50 shared Top-4 overview/execution rendering remains unchanged.
- Release validation: `216 passed`; targeted production safety/WebSocket suite: `27 passed`; browser E2E: `12 passed`; live 5050 Playwright verification: `2 passed`.
- The archive excludes API keys, runtime state, caches, logs and Python caches.
- This GitHub sync does not approve or enable real trading.

## Launch-gate tooling patch v10.49

- This was a tooling-only compatibility patch for auditing the V10.48 runtime; it did not change the application release or trading formulas.
- The launch gate validates the runtime dense-zone relationship (`total width = 2 × half width`) and explicit A→B synchronization instead of hard-coding retired formula values.
- Formal preflight requests use a longer timeout and report the actual blocking items.
- Browser navigation uses a 30-second `load` wait plus a short observation window.
- The verified V10.48 runtime remained blocked by `正式 API 金鑰已設定` and `小額灰度需手動確認`; this patch does not approve real trading.

## Current GitHub Actions archive gate

- The rebuild workflow targets the `v10.51` base64-parts archive.
- Existing executable safety tests inside the release are compiled and preserved; missing gate tests are injected before validation.
- The checked-in `v10.51` base64 parts reconstruct the directly verified release artifact.

## Historical v10.43 changes

- GitHub Actions release CI now targets the complete `v10.43` manifest and seven base64 parts.
- Visible non-held candidates with less than 365 days / 2190 bars of 4H history are excluded before ranking; held symbols remain visible and launch-blocking.
- The release includes `backtest_evidence_v10_43.json` for the active and cold-start candidate sets using the runtime's machine-readable 365-day / 2190-bar / 4H evidence contract.
- Cold-start fallback replaces unavailable `TONUSDC` with `TIAUSDC`, whose USDⓈ-M Futures 4H history meets the one-year minimum.
- Overview and auto-select use the same final ranking source.
- Reconciliation evidence exposes structured data-quality status and concrete per-symbol issues.
- Runtime rendering avoids first-paint blocking while evidence APIs still enforce full hydration.
- This sync does not approve real trading.

## Release archive safety-test gate

The release CI rebuilds the `v10.51` archive and verifies or injects pytest files required by `scripts/assert_release_tests_inside_archive.py` before extraction.

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
python - <<'PY'
import base64, json, pathlib
release = pathlib.Path("releases/v10.51")
manifest = json.loads((release / "manifest.json").read_text())
payload = "".join((release / "parts" / name).read_text().strip() for name in manifest["parts"])
(release / manifest["filename"]).write_bytes(base64.b64decode(payload))
PY
cd releases/v10.51 && shasum -a 256 -c SHA256SUMS && cd ../..
unzip releases/v10.51/auto_snowball_web_v10_51_book_stream_resubscribe_e2e.zip
cd auto_snowball_web_v10_51_book_stream_resubscribe_e2e
python -m pip install -r requirements.txt
pytest -q
python main.py
```

Runtime cache/state and local-only files are not committed.
