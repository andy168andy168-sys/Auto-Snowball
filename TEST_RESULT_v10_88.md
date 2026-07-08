# TEST_RESULT v10.88

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
- First run after version bump exposed old hard-coded `10.87` tests and a too-strict hygiene test that scanned pytest-created cache.
- After A/B test version sync and hygiene-test correction: `318 passed, 13 skipped`.

## New regression coverage
- `test_v188_release_secret_hygiene.py`
- Confirms `VERSION = 10.88` and `logic_version = D+E/v10.88`.
- Confirms `.binance_api_keys.json` is absent from release root.
- Confirms `.gitignore` covers local key, runtime cache/state, `__pycache__`, `.pyc`, `.pytest_cache`, log and pid artifacts.
- Confirms `.binance_api_keys.example.json` contains placeholder-only values.

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
- `/api/system/formula-audit` → 200, `ok=true`, `version=10.88`, `logic_version=D+E/v10.88`
- `/api/engine/parameters` → 200
- `/api/system/formal-live-readiness` → 200, `formal_live_ready=false`, `must_not_claim_live_ready=true`, blocking items remain 9
- `/api/binance/daily-performance` → 200, `不可判定`
- `/api/binance/daily-performance?mode=real` → 200, `不可判定`
- `/api/research/dense-width` → 200, `不可判定`

## Safety smoke
- DNS rebinding Host header blocked: HTTP 403.
- Mutating GET `/api/engine/plan` blocked: HTTP 405.
- GET refresh `/api/research/dense-width?refresh=1` blocked: HTTP 405.
- Cross-site POST blocked: HTTP 403.
- No-Origin / no-local POST blocked: HTTP 403.
- Real-mode switch blocked under safe/read-only/no-real-orders with local JSON POST: HTTP 423.
- Start automatic trading blocked under safe/read-only/no-real-orders with local JSON POST: HTTP 423.
- One-key close-all blocked under safe/read-only/no-real-orders with local JSON POST: HTTP 423.

## Release artifact scan
- `auto_snowball_web_v10_88_release_secret_hygiene_e2e.zip` excludes `.binance_api_keys.json`, `__pycache__`, `.pytest_cache`, `.pyc`, `.log`, `.pid`, and runtime cache/state files.
- The known leaked credential strings from the incoming v10.87 candidate were not found in the v10.88 release zip.

## Notes
- The skipped tests are browser/Playwright or Mac-local formal-gate evidence checks that cannot be satisfied inside this sandbox.
- v10.88 is a release-secret-hygiene/security packaging update; it does not clear formal-live blockers.
