# TEST_RESULT v10.87

## Command
```bash
AUTO_SNOWBALL_SAFE_MODE=1 AUTO_SNOWBALL_NO_REAL_ORDERS=1 AUTO_SNOWBALL_READ_ONLY=1 BINANCE_READ_ONLY=1 python - <<'PY'
import os, pytest
code = pytest.main(['-q'])
print(f'PYTEST_MAIN_EXIT_CODE={code}', flush=True)
os._exit(code)
PY
```

## Result
- `313 passed, 13 skipped`

## New regression coverage
- `test_v187_backtest_profit_floor_stage_score.py`
- Confirms `VERSION = 10.87` and `logic_version = D+E/v10.87`.
- Confirms `BACKTEST_SCORE_CONFIG.basis = stage_profit_floor_priority`.
- Confirms score table:
  - L1 保盈 = 100;
  - L2 保盈 = 90;
  - L3 保盈 = 80;
  - L4 保盈 = 70;
  - L5 保盈 = 60;
  - L6 保盈 = 50;
  - L7 保盈 = 40;
  - L8 保盈 = 30;
  - L9 保盈 = 20;
  - L10 保盈 = 10.
- Confirms未完成保盈 / unresolved = 0.
- Confirms止損 = -10, then normalization clamps below 0 and stop-loss rate still applies as an extra penalty.
- Confirms scoring uses actual `protected_stage`, not merely `opened_stages`.
- Confirms formula-audit exposes the A/B sync contract.

## HTTP smoke
Started with:
```bash
AUTO_SNOWBALL_SAFE_MODE=1 AUTO_SNOWBALL_NO_REAL_ORDERS=1 AUTO_SNOWBALL_READ_ONLY=1 BINANCE_READ_ONLY=1 PORT=5050 python main.py
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
- `/api/system/formula-audit` → 200, `ok=true`, `version=10.87`, `logic_version=D+E/v10.87`, `backtest_basis=stage_profit_floor_priority`
- `/api/engine/parameters` → 200
- `/api/system/formal-live-readiness` → 200, `formal_live_ready=false`, `must_not_claim_live_ready=true`, blocking items remain 9
- `/api/binance/daily-performance` → 200
- `/api/binance/daily-performance?mode=real` → 200
- `/api/research/dense-width` → 200

## Safety smoke
- DNS rebinding Host header blocked: HTTP 403.
- Mutating GET `/api/engine/plan` blocked: HTTP 405.
- GET refresh `/api/research/dense-width?refresh=1` blocked: HTTP 405.
- Cross-site POST blocked: HTTP 403.
- No-Origin / no-local POST blocked: HTTP 403.
- Real-mode switch blocked under safe/read-only/no-real-orders with local JSON POST: HTTP 423.
- Start automatic trading blocked under safe/read-only/no-real-orders with local JSON POST: HTTP 423.
- One-key close-all blocked under safe/read-only/no-real-orders with local JSON POST: HTTP 423.

## Notes
- The skipped tests are browser/Playwright or Mac-local formal-gate evidence checks that cannot be satisfied inside this sandbox.
- v10.87 is a backtest-score-only formula update; it does not clear formal-live blockers.
