# TEST_RESULT v10.84

## Command
```bash
AUTO_SNOWBALL_SAFE_MODE=1 AUTO_SNOWBALL_NO_REAL_ORDERS=1 AUTO_SNOWBALL_READ_ONLY=1 BINANCE_READ_ONLY=1 python3 -m pytest -q
```

## Result
- `302 passed, 13 skipped`

## New regression coverage
- `test_v184_dense_centerline_ui_clarity.py`
- Confirms an inside-dense-zone price that has not reached centerline exposes `dense_zone_membership_status=已入密集區` and `dense_centerline_status=未到中線`.
- Confirms a centerline touch is distinct: `dense_centerline_status=已觸及中線` and `距中線 0.00%`.
- Confirms formula-audit exposes the display contract.
- Confirms templates and JS no longer render the ambiguous `區內 0.00% / 已進入` label.

## HTTP smoke
Started with:
```bash
AUTO_SNOWBALL_SAFE_MODE=1 AUTO_SNOWBALL_NO_REAL_ORDERS=1 AUTO_SNOWBALL_READ_ONLY=1 BINANCE_READ_ONLY=1 PORT=5050 python3 main.py
```

Checked endpoints:
- `/` → 200
- `/auto-select` → 200
- `/calculator` → 200
- `/realtime` → 200
- `/audit-center` → 200
- `/virtual-account` → 200
- `/real-account` → 200
- `/control-panel` → 200
- `/api/status` → 200
- `/api/coins` → 200; 10 candidates sorted by final score descending
- `/api/system/formula-audit` → 200, `ok=true`, `version=10.84`, `logic_version=D+E/v10.84`
- `/api/engine/parameters` → 200
- `/api/system/formal-live-readiness` → 200, `formal_live_ready=false`, `must_not_claim_live_ready=true`, blocking items remain 9

## Safety smoke
- DNS rebinding Host header blocked: HTTP 403.
- Mutating GET `/api/engine/plan` blocked: HTTP 405.
- GET refresh `/api/research/dense-width?refresh=1` blocked: HTTP 405.
- Cross-site POST blocked: HTTP 403.
- No-Origin / no-local POST blocked: HTTP 403.
- Real-mode switch blocked under safe/read-only/no-real-orders: HTTP 423.
- Start automatic trading blocked under safe/read-only/no-real-orders: HTTP 423.
- One-key close-all blocked under safe/read-only/no-real-orders: HTTP 423.

## Notes
- The skipped tests are browser/Playwright or Mac-local formal-gate evidence checks that cannot be satisfied inside this sandbox.
- v10.84 is a UI/API/A-B display clarity update only; it does not clear formal-live blockers.
