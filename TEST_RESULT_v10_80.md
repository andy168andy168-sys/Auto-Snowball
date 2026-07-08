# TEST_RESULT v10.80

## Command
```bash
pytest -q
```

## Result
- `286 passed, 13 skipped`

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
- `/api/system/formula-audit` → 200, `ok=true`, `version=10.80`, `logic_version=D+E/v10.80`
- `/api/engine/parameters` → 200
- `/api/system/formal-live-readiness` → 200, `formal_live_ready=false`, `must_not_claim_live_ready=true`, blocking items remain 9

## Notes
- The skipped tests are browser/Playwright or Mac-local formal-gate evidence checks that cannot be satisfied inside this sandbox.
- v10.80 is a trading-parameter logic update only; it does not clear formal-live blockers.
