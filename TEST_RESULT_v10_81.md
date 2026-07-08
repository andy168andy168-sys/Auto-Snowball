# TEST_RESULT v10.81

## Command
```bash
AUTO_SNOWBALL_SAFE_MODE=1 AUTO_SNOWBALL_NO_REAL_ORDERS=1 AUTO_SNOWBALL_READ_ONLY=1 BINANCE_READ_ONLY=1 python3 -m pytest -q
```

## Result
- `289 passed, 13 skipped`

## New regression coverage
- `test_v181_centerline_ranking_score_sync.py`
- Confirms `中線入場分` label replaces old `現價入區分`/`入區分` wording.
- Confirms `centerline_entry_score_100` and `zone_entry_score_100` remain synchronized.
- Confirms merely being inside dense zone but not at centerline does not score 100.

## HTTP smoke
Started with:
```bash
AUTO_SNOWBALL_SAFE_MODE=1 AUTO_SNOWBALL_NO_REAL_ORDERS=1 AUTO_SNOWBALL_READ_ONLY=1 BINANCE_READ_ONLY=1 PORT=5050 python3 main.py
```

Checked endpoints:
- `/` → 200
- `/auto-select` → 200
- `/api/status` → 200
- `/api/coins` → 200
- `/api/system/formula-audit` → 200, `ok=true`, `version=10.81`, `logic_version=D+E/v10.81`
- `/api/engine/parameters` → 200
- `/api/system/formal-live-readiness` → 200, `formal_live_ready=false`, `must_not_claim_live_ready=true`, blocking items remain 9

## Notes
- The skipped tests are browser/Playwright or Mac-local formal-gate evidence checks that cannot be satisfied inside this sandbox.
- v10.81 is a ranking/UI/API score-alignment update only; it does not clear formal-live blockers.
