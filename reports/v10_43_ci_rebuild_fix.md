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
- Rebuilt archive SHA256 after safety-test injection: `1017aa6eadad6e9e410173e24fa71b0d69b49dd4bd868c104df96ff8e37a3f84`.
- Release archive test placement: `PASS`.
- Static production-gate audit: `PASS`.
- Rebuilt archive non-browser suite: `191 passed`.
- Workspace gate regression tests: `8 passed`.
- Active 5050 CI gate: `PASS`; formal API credentials and manual canary remain informational CI items and blocking production-preflight items.
- Rebuilt archive isolated browser E2E on 5051: seven main pages loaded, 10 ranking rows rendered, dynamic refresh advanced, and browser warnings/errors were empty.
