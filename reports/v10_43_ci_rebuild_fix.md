# V10.43 CI Rebuild Fix

## Root cause

The release workflow targeted V10.42, but the repository contained only its manifest and none of the base64 parts named by that manifest. `scripts/rebuild_release.py` therefore stopped before producing the ZIP, and the following hash step reported `rebuilt v10.42 release archive missing`.

## Fix

- Move the release workflow target to the verified V10.43 candidate-history package.
- Commit all seven base64 parts referenced by the V10.43 manifest.
- Keep safety-test injection, hash recording, archive extraction, static production audit, full non-browser pytest, 5050 smoke, and browser E2E in the same CI job.
- Require runtime identity, process monitor, formula audit, backtest evidence, ranking fields, and dynamic refresh in CI; record the production-credential/manual-canary preflight as informational because CI is intentionally read-only.
- Make missing manifests and parts fail with their exact paths before the hash step.
- Print the release directory contents around archive creation for actionable CI diagnostics.
- Use page `load` plus a short stabilization wait in the injected browser gate.
- Package `backtest_evidence_v10_43.json` and validate the runtime evidence contract (`bars >= 2190`, `lookback_days >= 365`, `interval = 4h`, `ok = true`) for every visible symbol.

## Safety and launch status

CI remains in safe, no-real-orders, read-only mode. This repair does not configure production API credentials, authorize the manual small-size canary, place a real order, or switch the application to real trading mode.

## Local verification

- Base archive SHA256: `f73067313cae9f5f0a7d65986a61c551ef4717218ee9a8aa22022412cf7796ad`.
- Rebuilt archive SHA256 after safety-test injection: `56baf7f11460bebf470cb1b16342cf2920dba9cc8a9ae16b2477183aded87228`.
- Release archive test placement: `PASS`.
- Static production-gate audit: `PASS`.
- Rebuilt archive non-browser suite with all browser-dependent tests excluded: `192 passed`.
- Self-contained browser suites: `10 passed`; active-5050 ranking synchronization browser test: `1 passed`.
- Workspace gate regression tests: `12 passed`.
- Active 5050 CI gate: `PASS`; formal API credentials and manual canary remain informational CI items and blocking production-preflight items.
- Rebuilt archive isolated browser E2E on 5051: seven main pages loaded, 10 ranking rows rendered, dynamic refresh advanced, and browser warnings/errors were empty.

## GitHub Actions run 102 follow-up

- The original rebuild/hash failure was fixed; rebuild, hash, extraction, archive placement, static audit, and non-browser command all reached completion.
- Run 102 exposed a stale `auto_snowball_web_v10_42` working directory in the 5050 step.
- It also exposed that `test_v148_browser_playwright_5050_auto_select.py` was still collected before the workflow started the 5050 server; the failure was hidden by `pytest | tee` because `pipefail` was not enabled.
- The workflow now enables `pipefail`, excludes all browser-dependent tests from the non-browser suite, runs the self-contained browser tests explicitly, starts the 5050 server from the V10.43 directory, then runs the active-5050 browser test and local launch gate.

## GitHub Actions run 106 follow-up

- The corrected V10.43 working directory, rebuild/hash, archive checks, static audit, and strict non-browser suite passed.
- Explicit execution exposed an invalid generated generic browser test: the outer Python string had expanded `"\\n"` into a literal newline inside the injected source.
- The generator now preserves the escaped newline, compiles every injected Python file before writing the ZIP, and has a workspace regression test covering all injected files.
- `AUTO_SNOWBALL_E2E_PORT` permits an isolated local port while CI continues to default to required port 5050.
- Rebuilt generic browser gate on isolated port 5052: `1 passed`.

## GitHub Actions run 108 follow-up

- All explicit browser tests and the V10.43 5050 server startup passed.
- The final local gate correctly rejected CI cold-start fallback rows because their runtime backtest cache was empty.
- CI now keeps ranking/live-field/dynamic-refresh checks strict and separately requires bundled machine-readable evidence to cover every visible cold-start symbol; production/local runs still require the live runtime backtest endpoint itself to pass.
- The bundled evidence covers 14 active and cold-start symbols with 2190 bars / 365 days / 4H metadata.
- The invalid `TONUSDC` cold-start fallback was replaced with `TIAUSDC`; Binance public USDⓈ-M Futures verification returned 2190 one-year 4H bars for every cold-start symbol.
- Browser E2E navigates only the HTML pages after the market API has already been validated over HTTP, avoiding a duplicate cold-start history hydration; navigation exceptions are recorded as gate failures instead of escaping as tracebacks.
- Live ranking now merges cached backtest evidence immediately and schedules missing one-year 4H hydration in one background worker, so a cold `/api/market/live` request cannot block on ten paginated Binance history calls.
- Final cold-start CI-equivalent gate on isolated port 5053: `PASS`; final browser groups: generic `1 passed`, self-contained suites `10 passed`, active-5050 v148 `1 passed`.
