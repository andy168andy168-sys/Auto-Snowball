# Auto Snowball v10.80 Sandbox Formal Live Gate Audit — 2026-07-08

## Scope
- Input package: `auto_snowball_web_v10_79_release_provenance_hardening_e2e.zip`.
- Output package: `auto_snowball_web_v10_80_centerline_entry_gate_e2e.zip`.
- Requested change: 第三項由「現價必須先進入密集區」改為「現價必須先進入 / 觸及 / 穿越密集區中線」。
- Sandbox cannot access Mac production workdir `/Users/andyna/Documents/自動滾倉系統設計`.
- Safety flags used for smoke test: `AUTO_SNOWBALL_SAFE_MODE=1`, `AUTO_SNOWBALL_NO_REAL_ORDERS=1`, `AUTO_SNOWBALL_READ_ONLY=1`, `BINANCE_READ_ONLY=1`.
- No real orders were placed. No real trading mode was enabled.

## Change summary
- Added V10.80 centerline gate logic.
- New rule: L1 can be armed only after current price touches the dense-zone centerline, or the latest markPrice crosses the centerline from the previous markPrice.
- If price is merely inside the dense zone but not at/crossed the centerline, status becomes `區內未到中線` and `execution_eligible=false`.
- After centerline gate passes, L1 still waits for latest dense-zone upper/lower breakout; dense-zone boundaries are still dynamic and not locked.

## A/B sync
- A formula: dense zone remains six-line center ±1.5% total 3%.
- A formula: entry gate is now `CENTERLINE`.
- B engine: `mark_reached_dense_zone_centerline()` enforces the same gate before `ARMED_L1`.
- Web labels and ranking fields now expose `dense_entry_ready`, `dense_centerline_reached`, and `dense_centerline_distance_pct`.
- `/api/system/formula-audit` returned `ok=true`, `version=10.80`, `logic_version=D+E/v10.80`.

## Tests
- Full pytest: `286 passed, 13 skipped`.
- 5050 smoke: `/`, `/auto-select`, `/api/status`, `/api/coins`, `/api/system/formula-audit`, `/api/engine/parameters`, `/api/system/formal-live-readiness` all returned HTTP 200 without Traceback/Internal Server Error text.

## Formal live readiness
- `/api/system/formal-live-readiness`: `formal_live_ready=false`, `ok=false`, `must_not_claim_live_ready=true`.
- Blocking items remain 9, including missing Mac-local Playwright evidence, production workdir evidence, fresh realtime sync evidence, signed Binance reconciliation, one-year 4H K-line backtest coverage, complete safety proof, and user-approved small-canary evidence.

## Conclusion
v10.80 implements the requested centerline-entry gate and passes executable sandbox tests. It still must not be declared ready for true-fund formal live trading until all formal-live blockers are cleared on the production Mac host.
