# V10.42 GitHub Sync Gate Report

## Status

**SYNCED FOR REVIEW / TRACKING ONLY. NOT APPROVED FOR LIVE CAPITAL.**

This report records the uploaded V10.42 launch-gate evidence package and the current safety status. It does not approve real trading, Mode 2, or live capital.

## Package

- Source upload: `auto_snowball_web_v10_42_launch_gate_evidence.zip`
- Source SHA256: `504d1ef96979d5bcb22c9e20a1883c1659a3d7612859324c67f178a76c344f01`
- Source bytes: `655826`
- Sanitized local artifact: `auto_snowball_web_v10_42_launch_gate_evidence_sanitized.zip`
- Sanitized SHA256: `4c06e28067bf127f33344f6e735dc9d379a59fde84d5bdd249ea297839ac87f2`
- Sanitized bytes: `234565`
- Included source files after sanitization: `108`
- Excluded unsafe/runtime/cache items: `85`

## Sanitization

The uploaded zip contained local/runtime/cache material that must not be committed as release truth:

- `.binance_api_keys.json`
- `.pytest_cache/`
- `__pycache__/`
- `.audit_truth_cache.json`
- `.market_sync_cache.json`
- `.roll_engine_state.json`

These were excluded from the sanitized local artifact and from this GitHub sync report.

## V10.42 Claimed Evidence Inside Package

From `TEST_RESULT_v10_42.md`:

```text
# V10.42 Test Result

- Targeted reconciliation and shared-ranking tests: `8 passed`.
- Browser regression that previously exposed cross-page ranking drift: `1 passed`.
- Full suite against isolated read-only runtime `127.0.0.1:5051`: `191 passed in 42.57s`.
- In-app browser verified V10.42 on home, auto-select, realtime, calculator, audit center, and control panel with zero console warnings/errors.
- Home and auto-select displayed the same ten symbols in the same order; auto-select scores were descending.
- Realtime rendered four synchronized `L1 trigger +30% -> protect +24%` rows.
- No real order was submitted and real trading mode was not enabled.

- Final clean extracted archive rerun: `191 passed in 40.54s`.
```

From `CHANGELOG_v10_42.md`:

```text
# V10.42 Reconciliation Evidence Gate

- `/api/binance/reconciliation` now exposes `dataQuality.ok`, per-symbol checks, and concrete issues.
- Non-zero positions require exchange entry, break-even, mark, unrealized PnL, liquidation, notional, and initial-margin fields.
- Leverage is accepted from Binance directly or derived from `abs(notional) / initialMargin` when the demo endpoint omits the direct field.
- Audit tooling now uses USDⓈ-M Futures 4H Klines, current runtime field names, structured reconciliation status, and load-based browser waits.
- Home and auto-select server rendering now share a five-second ranking snapshot; their one-second live API refresh remains unchanged.
- Clean-package first render no longer blocks on a synchronous one-year Kline hydration; evidence APIs still perform and enforce the full hydration.
- No real-order path or trading-mode behavior was changed.
```

## Independent GitHub Actions Finding

The checked GitHub Actions job `28455811584 / 84330150455` failed before full release validation. The failed gate was `Require executable production safety tests inside archive`, reporting that `test_no_safety_string_evidence_stubs.py` still used string-only evidence stubs. Therefore this sync cannot be used as a launch approval until a new workflow run passes the production safety gate, full pytest, Flask 5050 smoke, and browser E2E.

## Required Before Launch

1. Rotate / revoke any Binance key that was pasted or packaged locally.
2. Ensure no credential file is committed or packed into future release archives.
3. Replace string-only safety evidence stubs with executable production safety tests.
4. Re-run GitHub Actions on the exact V10.42 release commit.
5. Require PASS for production safety tests, full pytest, 5050 Flask smoke, and browser E2E.
6. Keep `AUTO_SNOWBALL_SAFE_MODE=1`, `AUTO_SNOWBALL_NO_REAL_ORDERS=1`, `AUTO_SNOWBALL_READ_ONLY=1`, and `BINANCE_READ_ONLY=1` for CI.

## Safety

- No real order was submitted by this sync.
- No real trading mode was enabled by this sync.
- This is an evidence/report synchronization only.

Synced at: `2026-06-30T23:57:50+08:00`
