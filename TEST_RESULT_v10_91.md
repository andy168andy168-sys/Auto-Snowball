# TEST_RESULT v10.91

## Result
- Full pytest: `323 passed, 13 skipped`.
- New regression: `test_v191_centerline_crossing_touch.py`.

## New regression coverage
- Confirms price jump from below dense zone to above dense zone across centerline counts as touched:
  - `dense_centerline_reached=true`
  - `dense_centerline_crossed=true`
  - `dense_entry_ready=true`
  - `dense_centerline_status=已觸及中線`
  - `dense_centerline_status_label=中線：已觸及`
  - UI text no longer shows `先等觸及中線`.
- Confirms price jump from above dense zone to below dense zone across centerline counts as touched.
- Confirms outside movement without crossing the centerline still waits for centerline touch.

## HTTP smoke
A fresh 5050 runtime was checked after the v10.91 change:
- Main pages and system APIs returned HTTP 200.
- `/api/system/formula-audit` reported v10.91 / D+E/v10.91.
- `/api/coins` returned visible candidates sorted by final score descending.
- Formal live readiness remained blocked.

## Notes
- The skipped tests are browser/Playwright or Mac-local formal-gate evidence checks that cannot be satisfied inside this sandbox.
- v10.91 is a centerline crossing-touch consistency update; it does not clear formal-live blockers.
