# TEST_RESULT v10.92

## Result
- Full pytest: `327 passed, 13 skipped`.
- New regression: `test_v192_centerline_then_breakout_entry.py`.

## New regression coverage
- Confirms one tick from below dense zone to above dense zone across centerline only arms L1 and does not open a position.
- Confirms one tick from above dense zone to below dense zone across centerline only arms L1 and does not open a position.
- Confirms LONG L1 opens only after the system is already armed and a later tick crosses the dense-zone upper edge upward.
- Confirms SHORT L1 opens only after the system is already armed and a later tick crosses the dense-zone lower edge downward.

## HTTP smoke
A fresh 5050 runtime was checked after the v10.92 change:
- Main pages and system APIs returned HTTP 200.
- `/api/system/formula-audit` reported v10.92 / D+E/v10.92.
- `/api/coins` returned 10 visible candidates sorted by final score descending.
- `/api/binance/daily-performance` and `/api/research/dense-width` returned `不可判定` in sandbox rather than pretending to have production evidence.
- Formal live readiness remained blocked.

## Safety smoke
- DNS rebinding Host header blocked: HTTP 403.
- Mutating GET `/api/engine/plan` blocked: HTTP 405.
- GET refresh `/api/research/dense-width?refresh=1` blocked: HTTP 405.
- Cross-site POST blocked: HTTP 403.
- Real-mode switch blocked under safe/read-only/no-real-orders with local JSON POST: HTTP 423.
- Start automatic trading blocked under safe/read-only/no-real-orders with local JSON POST: HTTP 423.
- One-key close-all blocked under safe/read-only/no-real-orders with local JSON POST: HTTP 423.

## Notes
- The skipped tests are browser/Playwright or Mac-local formal-gate evidence checks that cannot be satisfied inside this sandbox.
- v10.92 is a centerline-armed-then-breakout-entry update; it does not clear formal-live blockers.
