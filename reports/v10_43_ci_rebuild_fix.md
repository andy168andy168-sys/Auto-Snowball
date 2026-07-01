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

- Base archive SHA256: `6d078b880b4905d8570bd3f7096a41e382bbf03cbdfc124e3fb64d4b2094ebf2`.
- Rebuilt archive SHA256 after safety-test injection: `70d0b1854947f1d2178cdfbd283960180269fea03235bb62f2aeb1e5f9a83ac2`.
- Release archive test placement: `PASS`.
- Static production-gate audit: `PASS`.
- Rebuilt archive non-browser suite with all browser-dependent tests excluded: `190 passed`.
- Self-contained browser suites: `10 passed`; active-5050 ranking synchronization browser test: `1 passed`.
- Workspace gate regression tests: `9 passed`.
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
