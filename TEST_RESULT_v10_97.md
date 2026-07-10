# TEST_RESULT v10.97

## Result
- Full pytest: `340 passed, 13 skipped`.
- Focused regression and launch/hygiene checks: `23 passed` before full run.
- 5050 smoke: main pages and system APIs returned HTTP 200.

## New regression coverage
- `test_v197_armed_snapshot_breakout_real_sequence.py`
- Confirms real candidate sequence:
  1. candidate starts in `WAITING_CENTERLINE`;
  2. current price touches/crosses centerline;
  3. system enters `ARMED_L1` and snapshots the current dense-zone low/high;
  4. later dense-zone boundaries move;
  5. later price breaks the armed snapshot high/low;
  6. system opens `L1` instead of chasing the moving boundary forever.
- Confirms temporary missing dense-zone cache does not wipe `ARMED_L1` tracking state.
- Confirms existing v10.96 rank-rotation retention still works.
- Confirms existing v10.92 centerline-then-breakout rule still works.

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
- `/api/system/formula-audit` → 200, `ok=true`, `version=10.97`, `logic_version=D+E/v10.97`
- `/api/engine/parameters` → 200
- `/api/system/formal-live-readiness` → 200, `formal_live_ready=false`, `must_not_claim_live_ready=true`
- `/api/binance/daily-performance` → 200, `不可判定`
- `/api/binance/daily-performance?mode=real` → 200, `不可判定`
- `/api/research/dense-width` → 200, `不可判定`

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
- v10.97 is an armed-tracking runtime sequencing fix; it does not clear formal-live blockers.
