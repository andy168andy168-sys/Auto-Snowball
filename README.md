# Auto-Snowball

Auto Snowball Web release archive for USDC futures rolling strategy monitoring.

## Current release target

- Release version: `v10.50`
- Release manifest: `releases/v10.50/manifest.json`
- Release archive filename after reconstruction: `auto_snowball_web_v10_50_overview_top4_shared_ui_e2e.zip`
- Release archive SHA256: `0d5f5b38366385d2396a7f202819302f24f3d548e59ba905fde4368179028163`
- CI mode: safe / read-only only
- Formal live-capital status: blocked until `正式 API 金鑰已設定` and `小額灰度需手動確認` both pass.

## Main v10.50 changes

- Overview and execution center share the same Top-4 rolling-coin component and live update chain.
- Execution center removes six duplicate summary cards and their obsolete update targets.
- Formula/version labels, ranking, execution plan and A-to-B dense-zone guard are synchronized to `D+E/v10.50`.
- Release validation: `213 passed`; targeted production safety suite: `25 passed`; live 5050 Playwright E2E: `1 passed`.
- The archive excludes API keys, runtime state, caches, logs and Python caches.
- This GitHub sync does not approve or enable real trading.

## Launch-gate tooling patch v10.49

- This is a tooling-only compatibility patch for auditing the V10.48 runtime; the current application release remains V10.50.
- The launch gate validates the runtime dense-zone relationship (`total width = 2 × half width`) and explicit A→B synchronization instead of hard-coding retired formula values.
- Formal preflight requests use a longer timeout and report the actual blocking items.
- Browser navigation uses a 30-second `load` wait plus a short observation window.
- The verified V10.48 runtime remained blocked by `正式 API 金鑰已設定` and `小額灰度需手動確認`; this patch does not approve real trading.

## Current GitHub Actions archive gate

- The existing rebuild workflow still targets the historical `v10.43` base64-parts archive.
- The checked-in `v10.50` base64 parts reconstruct the directly verified release artifact; the workflow target was not changed by this sync.

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
python - <<'PY'
import base64, json, pathlib
release = pathlib.Path("releases/v10.50")
manifest = json.loads((release / "manifest.json").read_text())
payload = "".join((release / "parts" / name).read_text().strip() for name in manifest["parts"])
(release / manifest["filename"]).write_bytes(base64.b64decode(payload))
PY
cd releases/v10.50 && shasum -a 256 -c SHA256SUMS && cd ../..
unzip releases/v10.50/auto_snowball_web_v10_50_overview_top4_shared_ui_e2e.zip
cd auto_snowball_web_v10_50_overview_top4_shared_ui_e2e
python -m pip install -r requirements.txt
pytest -q
python main.py
```

Runtime cache/state and local-only files are not committed.
