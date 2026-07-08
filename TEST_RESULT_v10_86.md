# TEST_RESULT v10.86

## Command
```bash
AUTO_SNOWBALL_SAFE_MODE=1 AUTO_SNOWBALL_NO_REAL_ORDERS=1 AUTO_SNOWBALL_READ_ONLY=1 BINANCE_READ_ONLY=1 pytest -q
```

## Result
- `310 passed, 13 skipped`

## New regression coverage
- `test_v186_volatility_monotonic_score.py`
- Confirms `VERSION = 10.86` and `logic_version = D+E/v10.86`.
- Confirms `VOLATILITY_SCORE_CONFIG.basis = monotonic_abs_24h_change`.
- Confirms 24h absolute volatility scoring is monotonic:
  - 0% → 0;
  - 1% → 5;
  - 5% → 25;
  - 10% → 50;
  - 20% → 100;
  - 30% → 100 capped.
- Confirms `priceChangePercent = -5` uses absolute value and scores 25.
- Confirms volatility weight remains 15 and other ranking weights remain unchanged.
- Confirms formula-audit exposes the new A/B sync contract.

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
- `/api/system/formula-audit` → 200, `ok=true`, `version=10.86`, `logic_version=D+E/v10.86`, `volatility_basis=monotonic_abs_24h_change`
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
- Real-mode switch blocked under safe/read-only/no-real-orders with JSON POST: HTTP 423.
- Start automatic trading blocked under safe/read-only/no-real-orders with JSON POST: HTTP 423.
- One-key close-all blocked under safe/read-only/no-real-orders with JSON POST: HTTP 423.

## Notes
- The skipped tests are browser/Playwright or Mac-local formal-gate evidence checks that cannot be satisfied inside this sandbox.
- v10.86 is a volatility-score-only formula update; it does not clear formal-live blockers.
