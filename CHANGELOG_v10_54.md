# V10.54 — Runtime write-guard hardening

## Security fixes

- Safe/read-only/no-real-orders environment flags are enforced by the runtime before signed Binance writes.
- Safe/read-only/no-real-orders mode blocks real-mode switching, automatic start, manual trading ticks, and close-all execution.
- `GET /api/engine/tick?trade=1` cannot trigger trading; GET ticks are always read-only.
- Cross-site POST/PUT/PATCH/DELETE requests to localhost state-changing APIs are rejected.
- Real-mode start requires formal launch preflight and explicit `AUTO_SNOWBALL_CANARY_APPROVED=1` manual approval.

## Synchronization

- Runtime, formula audit version, API payloads, README, release manifest, GitHub Actions, browser E2E, and version assertions are synchronized to V10.54.
- V10.53 also fixes the repository launch-gate dynamic-refresh false red.
- Trading formulas and risk parameters remain unchanged.

## Safety

- No real order was sent and live mode was not enabled during verification.
