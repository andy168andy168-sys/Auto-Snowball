# Auto Snowball v10.97 Full-System Security Audit — 2026-07-10

## Scope
- Input: `auto_snowball_web_v10_96_armed_tracking_retention_guard.zip`
- Output: `auto_snowball_web_v10_97_runtime_state_mode_isolation_e2e.zip`
- Safety flags: safe mode, no real orders, read-only, Binance read-only.
- No real orders were placed and real mode was not enabled.

## Vulnerabilities found

### 1. Release-bundled runtime snapshot poisoning — fixed
The v10.96 archive contained `.market_sync_cache.json` and `.roll_engine_state.json`. On a clean HOME, importing v10.96 loaded the bundled plans (`ORDIUSDC`, `XRPUSDC`, `BNBUSDC`, `BTCUSDC`) and bundled market ranking immediately. The loader could then copy that release-local snapshot into the version-neutral shared state file.

Impact:
- stale position/ARMED_L1/stage/order state could enter a new deployment;
- demo market data could appear as current fallback truth;
- the package could overwrite a valid shared snapshot if its timestamp was newer.

Fix:
- runtime files moved outside release root;
- release-root runtime files ignored by default;
- explicit legacy import flag required;
- clean package excludes all runtime files.

### 2. Cross-account engine-state contamination — fixed
The prior single engine snapshot could be reused across virtual and real account modes. An ARMED_L1 or stage/orderId from one account path could survive a mode change.

Fix:
- engine state is mode-scoped: `.roll_engine_state.virtual.json` and `.roll_engine_state.real.json`;
- old external unscoped state migrates only when its embedded mode matches;
- mode switch saves source state, stops old-mode WebSocket state, clears memory plans, and loads only destination-mode state.

### 3. Mode switching while engine running — fixed
Account mode could be changed while automatic trading was running, creating a race between engine thread, truth source and WebSocket account path.

Fix:
- switching to a different account mode returns HTTP 409 until the engine is paused.

### 4. virtual/real market-cache mixing — fixed
The global market cache could be reused after account-mode changes.

Fix:
- all ranking, real-time, WebSocket-symbol and execution-market paths use a mode-aware cache helper;
- mode mismatch returns no cached coins and requires a fresh sync.

### 5. Mutable evidence/parameters in release directory — fixed
Audit cache, calculator parameters and formal-live evidence were rooted in the versioned release directory.

Fix:
- credentials, market cache, audit cache, engine parameters, engine state and formal-live evidence all default to a private version-neutral state directory;
- writes are atomic and private (directory 0700, files 0600).

## Unchanged trading logic
- Centerline touch/crossing only arms L1.
- A later dense-zone upper/lower breakout opens L1.
- ARMED_L1 survives ranking rotation within the four execution slots.
- Dense-zone, volume, volatility, backtest, L1-L10, stop-loss, profit-floor and ranking-weight formulas are unchanged.

## Verification
- Full pytest: `343 passed, 13 skipped`.
- Security subset: `68 passed`.
- JavaScript syntax check passed.
- All 11 Jinja templates parsed successfully.
- Clean 5050 runtime returned HTTP 200 for all primary pages and APIs.
- Formula audit: v10.97 / D+E/v10.97 / ok=true.
- 10 visible candidates were sorted by final score descending.
- Runtime write guards returned expected 403/405/423 results.
- Release root stayed free of runtime files during execution.

## Browser limitation
System Chromium could launch, but localhost navigation was blocked by sandbox administrator policy (`ERR_BLOCKED_BY_ADMINISTRATOR`). This is not counted as a browser E2E pass.

## Formal-live result
Auto Snowball has **not** reached true-fund formal-live standard. The formal endpoint still reports 9 blockers, including Mac-local browser E2E, production workdir evidence, fresh realtime sequence evidence, full 365-day candidate evidence, signed Binance reconciliation, complete production safety evidence and user-approved small-canary evidence.
