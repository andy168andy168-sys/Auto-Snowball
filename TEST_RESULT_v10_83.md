# TEST_RESULT v10.83

## Command
```bash
AUTO_SNOWBALL_SAFE_MODE=1 AUTO_SNOWBALL_NO_REAL_ORDERS=1 AUTO_SNOWBALL_READ_ONLY=1 BINANCE_READ_ONLY=1 python3 -m pytest -q
```

## Result
- `297 passed, 13 skipped`

## New regression coverage
- `test_v183_volume_percentage_fairness.py`
- Confirms growth-score piecewise contract: 70% = 0, 100% = 50, 200% = 100.
- Confirms 30-day base liquidity uses log scale and caps between 10M and 100M USDC/day.
- Confirms 1D/7D, 7D/14D and 14D/30D percentages are produced from 4H quoteVolume windows.
- Confirms `/api/system/formula-audit` exposes `percentage_fairness` and A/B checks pass.

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
- `/api/coins` → 200
- `/api/system/formula-audit` → 200, `ok=true`, `version=10.83`, `logic_version=D+E/v10.83`, `volume_basis=percentage_fairness`
- `/api/engine/parameters` → 200
- `/api/system/formal-live-readiness` → 200, `formal_live_ready=false`, `must_not_claim_live_ready=true`, blocking items remain 9

## Notes
- The skipped tests are browser/Playwright or Mac-local formal-gate evidence checks that cannot be satisfied inside this sandbox.
- v10.83 is a ranking/API/A-B score-formula update only; it does not clear formal-live blockers.
