# V10.66 Formal Live Audit Report

Status: **blocked**.

V10.66 fixes a release packaging vulnerability and adds explicit formal-live readiness, daily Binance performance, and dense-zone width research gates.

## Fixed

- Removed local Binance credential file from the release snapshot.
- Removed runtime cache/state files from the final packaged zip.
- Added `/api/system/formal-live-readiness`.
- Added `/api/binance/daily-performance` with strict `不可判定` behavior when private data is incomplete.
- Added `/api/research/dense-width` read-only evaluation gate.
- Added v169 regression tests.

## Validation

- Full pytest: `261 passed, 13 skipped`.
- Browser subset: `7 skipped`; sandbox skip is not formal browser E2E evidence.
- 5050 smoke endpoints returned 200 in safe/read-only mode.

## Formal launch decision

Not ready. Do not enable real trading until all blocking evidence passes on the Mac primary workdir and actual 127.0.0.1:5050 instance.
