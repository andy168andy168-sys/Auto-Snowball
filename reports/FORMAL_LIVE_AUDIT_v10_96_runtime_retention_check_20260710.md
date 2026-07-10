# Auto Snowball v10.96 Runtime Retention Check — 2026-07-10

## Scope
- Package inspected: `auto_snowball_web_v10_96_armed_tracking_retention_guard.zip`.
- User rule: touching/crossing dense-zone centerline starts tracking/arms L1; L1 opens only after a later dense-zone upper/lower breakout.
- Additional issue checked: armed tracking must survive ranking top-four rotation until open/cancel/invalidated.
- Safety flags used: `AUTO_SNOWBALL_SAFE_MODE=1`, `AUTO_SNOWBALL_NO_REAL_ORDERS=1`, `AUTO_SNOWBALL_READ_ONLY=1`, `BINANCE_READ_ONLY=1`.
- No real orders were placed. No real trading mode was enabled.

## Findings
- v10.96 already contains the intended retention guard.
- An `ARMED_L1` symbol remains tracked even after falling outside the latest ranking top four.
- The armed symbol consumes one of the existing four execution slots; the engine does not create a fifth slot.
- Ordinary unarmed symbols outside selected slots are still pruned.
- Synthetic `TESTUSDC` events are removed from production state loading.
- Existing centerline-then-breakout behavior remains active: touching/crossing centerline arms L1 only; actual L1 entry waits for a later upper/lower dense-zone breakout.

## Verification run in sandbox
- Targeted tests run locally: `12 passed` for armed-retention, centerline-crossing touch, and centerline-then-breakout entry tests.
- Full pytest run locally: `338 passed, 13 skipped`.
- 5057 smoke from a fresh v10.96 runtime: main pages and system APIs returned HTTP 200.
- `/api/system/formula-audit`: `ok=true`, `version=10.96`, `logic_version=D+E/v10.96`.
- `/api/coins`: returned 10 visible candidates sorted by final score descending.
- `/api/system/formal-live-readiness`: `formal_live_ready=false`, `must_not_claim_live_ready=true`.

## Safety smoke
- DNS rebinding Host header blocked: HTTP 403.
- Mutating GET `/api/engine/plan` blocked: HTTP 405.
- GET refresh `/api/research/dense-width?refresh=1` blocked: HTTP 405.
- Cross-site POST blocked: HTTP 403.
- Real-mode switch attempt `/api/mode` blocked under safe/read-only/no-real-orders with local JSON POST: HTTP 423.
- Start automatic trading `/api/action` blocked under safe/read-only/no-real-orders with local JSON POST: HTTP 423.
- One-key close-all `/api/engine/close-all` with `confirm=CLOSE_ALL` blocked under safe/read-only/no-real-orders with local JSON POST: HTTP 423.

## Formal live readiness
v10.96 still does **not** meet true-fund formal-live standard in this sandbox. Required production evidence remains unavailable here, including Mac-local browser E2E, actual production workdir evidence, fresh realtime sync evidence, signed Binance reconciliation, production safety evidence, and user-approved small-canary evidence.

## Conclusion
No new code change is required for the issue described by the user. v10.96 already implements the required behavior: centerline touch/crossing arms tracking, the later dense-zone breakout opens L1, and ARMED_L1 tracking is retained across ranking rotation. No v10.97 was produced.
