# Auto-Snowball

Auto Snowball Web release archive for USDC futures rolling strategy monitoring.

## Current release target

- Release version: `v10.54`
- Release manifest: `releases/v10.54/manifest.json`
- Release archive filename after reconstruction: `auto_snowball_web_v10_54_read_only_gate_hardening.zip`
- Release archive SHA256: `f3f0cc8fc5ccdcc622b1d617aa2ba65de1c0740ba4eed00c88419b37ab8b9c69`
- CI mode: safe / read-only only
- Formal live-capital status: blocked until `安全／唯讀交易鎖已解除`, `正式 API 金鑰已設定`, and `小額灰度需手動確認` all pass in a user-approved production run.

## Main v10.54 changes

- Safe/read-only/no-real-orders flags are enforced inside the runtime before signed Binance writes.
- Real-mode switching, automatic start, trading ticks and close-all fail closed while the applicable safety lock is active.
- GET requests can no longer trigger trading, and cross-site state-changing requests to localhost are rejected.
- Real-mode start is coupled to formal preflight and explicit manual canary approval.
- V10.51 book-stream recovery and V10.50 shared Top-4 rendering remain unchanged.
- Release validation: `225 passed`; targeted production safety/WebSocket suite: `32 passed`; browser/HTTP E2E: `12 passed`; live 5050 Playwright verification: `2 passed`.
- The archive excludes API keys, runtime state, caches, logs and Python caches.
- This GitHub sync does not approve or enable real trading.

## Launch-gate tooling patch v10.53

- Restores `validate_market_refresh()` to compare consecutive market snapshots instead of invoking undeclared Playwright state.
- Dynamic refresh now passes only when synchronized rows remain valid and either a tracked live field or the payload timestamp advances.
- Adds regression coverage for timestamp-only advancement, live-field advancement, and unchanged snapshots.
- The audited application runtime remains V10.51; V10.53 is a repository-side verification-tooling patch only.
- Formal live-capital status remains blocked by `正式 API 金鑰已設定` and `小額灰度需手動確認`.

## Launch-gate tooling patch v10.49

- This was a tooling-only compatibility patch for auditing the V10.48 runtime; it did not change the application release or trading formulas.
- The launch gate validates the runtime dense-zone relationship (`total width = 2 × half width`) and explicit A→B synchronization instead of hard-coding retired formula values.
- Formal preflight requests use a longer timeout and report the actual blocking items.
- Browser navigation uses a 30-second `load` wait plus a short observation window.
- The verified V10.48 runtime remained blocked by `正式 API 金鑰已設定` and `小額灰度需手動確認`; this patch does not approve real trading.

## Current GitHub Actions archive gate

- The rebuild workflow targets the `v10.54` base64-parts archive.
- Existing executable safety tests inside the release are compiled and preserved; missing gate tests are injected before validation.
- The checked-in `v10.54` base64 parts reconstruct the directly verified release artifact.

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

The release CI rebuilds the `v10.54` archive and verifies or injects pytest files required by `scripts/assert_release_tests_inside_archive.py` before extraction.

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
release = pathlib.Path("releases/v10.54")
manifest = json.loads((release / "manifest.json").read_text())
payload = "".join((release / "parts" / name).read_text().strip() for name in manifest["parts"])
(release / manifest["filename"]).write_bytes(base64.b64decode(payload))
PY
cd releases/v10.54 && shasum -a 256 -c SHA256SUMS && cd ../..
unzip releases/v10.54/auto_snowball_web_v10_54_read_only_gate_hardening.zip
cd auto_snowball_web_v10_54_read_only_gate_hardening
python -m pip install -r requirements.txt
pytest -q
python main.py
```

Runtime cache/state and local-only files are not committed.
