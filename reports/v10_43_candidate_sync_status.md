# V10.43 Candidate Sync Status

## Status

**SYNCHRONIZED FOR REVIEW / TRACKING ONLY. NOT APPROVED FOR LIVE CAPITAL.**

A V10.43 candidate package was received and sanitized locally. The original package was not committed because it contained local/runtime/cache material, including a local Binance credential filename and pytest/cache artifacts.

## Sanitized release identity

- Source package: `auto_snowball_web_v10_43_candidate_history_gate.zip`
- Sanitized release filename: `auto_snowball_web_v10_43_release_flat.zip`
- Sanitized bytes: `225553`
- Sanitized SHA256: `2f5ee70a920c287aacad00e34b409c223ccbeba5696bbbd24778393f0805dc5a`
- Included source files after sanitization: `111`
- Excluded local/runtime/cache files: `81`
- Release base64 parts required: `7`

## Claimed V10.43 evidence inside package

From `TEST_RESULT_v10_43.md`:

- Candidate-history targeted regression: `2 passed`.
- Safety evidence set: `18 passed`.
- Full source suite: `193 passed in 32.28s`.
- Isolated read-only runtime `127.0.0.1:5051`: 10/10 visible rows passed 365-day / 2190-bar 4H evidence; ranking sorted descending; formula audit and process monitor passed.
- Browser pages loaded as V10.43 with zero console warnings/errors; live clock and prices refreshed.
- No real order was submitted and real trading mode was not enabled.

## V10.43 changelog summary

From `CHANGELOG_v10_43.md`:

- Non-held contracts with explicit 4H history below the formal 2190-bar minimum are excluded before entering the visible leaderboard.
- Rejected cached rows are replaced from the fallback candidate pool and must pass hydration/evidence gates.
- Held symbols are never hidden; if a held contract lacks one year of history, it remains visible and formal launch preflight remains blocked.
- No order path, credential, or trading-mode behavior changed.

## Required before launch

1. Commit the generated `releases/v10.43/manifest.json` and `releases/v10.43/parts/part_00.b64` through `part_06.b64`.
2. Update release CI from V10.42 to V10.43 on the same release branch.
3. Require GitHub Actions PASS for rebuild, archive extraction, executable production safety tests, static production audit, full non-browser pytest, Flask 5050 smoke, and browser E2E.
4. Keep CI read-only / safe-mode only.

## Safety

- No real order was submitted by this sync.
- No live trading approval is granted by this sync.
- The original unsanitized zip must not be committed.
