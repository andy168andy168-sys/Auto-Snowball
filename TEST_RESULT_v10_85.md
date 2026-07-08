# TEST_RESULT v10.85

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
- `307 passed, 13 skipped`
- The force-exit wrapper was used only after `pytest.main()` returned code 0, to avoid waiting on sandbox non-daemon background threads after all tests had completed.

## New regression coverage
- `test_v185_backtest_l1_priority_score.py`
- Confirms `BACKTEST_SCORE_CONFIG.basis = l1_profit_floor_priority`.
- Confirms L1 score is 100 and L10 score is 10.
- Confirms merely opening L1 without profit-floor protection is 0, not 100.
- Confirms stop-loss remains below all stage scores.
- Confirms formula-audit and A/B sync expose the backtest scoring contract.
- Confirms UI labels use `一年L1保盈分` instead of the old `一年回測層級` wording.

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
- `/api/system/formula-audit` → 200, `ok=true`, `version=10.85`, `logic_version=D+E/v10.85`, `backtest_basis=l1_profit_floor_priority`
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
- Real-mode switch blocked under safe/read-only/no-real-orders: HTTP 423.
- Start automatic trading blocked under safe/read-only/no-real-orders: HTTP 423.
- One-key close-all blocked under safe/read-only/no-real-orders: HTTP 423.

## Notes
- The skipped tests are browser/Playwright or Mac-local formal-gate evidence checks that cannot be satisfied inside this sandbox.
- v10.85 is a backtest-score-only formula update; it does not clear formal-live blockers.
