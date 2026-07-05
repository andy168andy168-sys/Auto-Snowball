# Auto Snowball v10.72 version contract fix

Status: formal launch remains blocked.

## Issue found

Full pytest on v10.71 failed because several legacy regression tests were still hard-coded to version `10.70` while the runtime was already `10.71`.

Affected areas:

- launch preflight version alignment
- formula-audit logic version
- audit-center formula snapshot
- HTTP E2E status/formula version checks
- L1 guard sync test
- ranking weight preservation test

## Fix

- Updated runtime to `VERSION = 10.72`.
- Updated stale test assertions so formula-audit and E2E checks track `main.VERSION` and `D+E/v{main.VERSION}`.
- Added `test_v174_version_contract_and_package_hygiene.py`.
- Repacked the release with local-only credential/cache/state/log/pid/pycache files excluded.

## Validation

- Targeted safety/formula/process tests: `20 passed`.
- Full pytest: `279 passed, 13 skipped`.
- Browser subset: `12 skipped` in sandbox; not valid Mac-local browser evidence.
- 5050 smoke in safe/read-only mode returned 200 for key pages and APIs.

## Gate decision

Not ready for formal launch. Mac-local 5050 browser E2E, signed reconciliation, one-year 4H candidate evidence, dense-width validation, full external evidence and user-approved canary proof remain required.
