# TEST_RESULT v10.98

## Full pytest
```bash
AUTO_SNOWBALL_SAFE_MODE=1 AUTO_SNOWBALL_NO_REAL_ORDERS=1 AUTO_SNOWBALL_READ_ONLY=1 BINANCE_READ_ONLY=1 python - <<'PY'
import os, pytest
code = pytest.main(['-q'])
print(f'PYTEST_MAIN_EXIT_CODE={code}', flush=True)
os._exit(code)
PY
```

## Result
- `344 passed, 13 skipped`

## New regression coverage
- `test_v198_centerline_entry_score_triggered_highest.py`
- Confirms `VERSION = 10.98` and `logic_version = D+E/v10.98`.
- Confirms `CENTERLINE_ENTRY_SCORE_CONFIG.basis = triggered_centerline_highest_score`.
- Confirms all centerline-triggered / armed states get 100 raw score and 25 weighted score:
  - `dense_entry_ready=true`;
  - `dense_centerline_reached=true`;
  - `dense_centerline_crossed=true`;
  - `engine_entry_state=ARMED_L1`;
  - `entry_state=ARMED_L1`;
  - `dense_zone_arrival_status=已進入中線`;
  - `dense_centerline_status=已觸及中線`;
  - `dense_centerline_status_label=中線：已觸及`;
  - execution / engine status containing 已啟動追蹤 or 已武裝.
- Confirms inside-zone distance score remains below 100 until centerline is actually triggered.
- Confirms formula-audit exposes the A/B sync contract.

## 5050 smoke
A fresh 5050 runtime was checked after the v10.98 change:
- `/`, `/auto-select`, `/calculator`, `/realtime`, `/audit-center`, `/virtual-account`, `/real-account`, `/control-panel` returned HTTP 200.
- `/api/status`, `/api/coins`, `/api/system/formula-audit`, `/api/engine/parameters`, `/api/system/formal-live-readiness`, `/api/binance/daily-performance`, `/api/binance/daily-performance?mode=real`, `/api/research/dense-width` returned HTTP 200.
- `/api/system/formula-audit` reported `ok=true`, `version=10.98`, `logic_version=D+E/v10.98`, and `centerline_entry_score.config.basis=triggered_centerline_highest_score`.
- `/api/coins` returned 10 visible candidates sorted by final score descending.
- `/api/system/formal-live-readiness` returned `formal_live_ready=false` and `must_not_claim_live_ready=true`.

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
- v10.98 is a centerline-entry-score A/B sync update; it does not clear formal-live blockers.
