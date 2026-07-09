# Auto Snowball v10.91 Sandbox Formal Live Gate Audit — 2026-07-09

## Scope
- Input package: `auto_snowball_web_v10_90_centerline_crossing_guard.zip`.
- Output package: `auto_snowball_web_v10_91_centerline_crossing_touch_e2e.zip`.
- Requested change: if current price crosses the dense-zone centerline from the previous tick, it must count as centerline touched.
- Safety flags used during sandbox execution: `AUTO_SNOWBALL_SAFE_MODE=1`, `AUTO_SNOWBALL_NO_REAL_ORDERS=1`, `AUTO_SNOWBALL_READ_ONLY=1`, `BINANCE_READ_ONLY=1`.
- No real orders were placed. No real trading mode was enabled.

## Change summary
- Version bumped to `10.91` / `D+E/v10.91`.
- Only centerline touch/crossing display and readiness consistency was changed.
- If `previous_price` and current `price` are on opposite sides of dense-zone centerline, the row is marked as centerline touched even if the current price already jumped outside the dense zone.
- Synchronized fields when crossed:
  - `dense_centerline_reached=true`;
  - `dense_centerline_crossed=true`;
  - `dense_entry_ready=true`;
  - `dense_centerline_status=已觸及中線`;
  - `dense_centerline_status_label=中線：已觸及`;
  - `dense_zone_arrival_status=已進入中線`.
- UI/API no longer shows `未到中線 / 先等觸及中線` when the price already crossed the centerline between ticks.

## Unchanged formulas
- Entry formula unchanged.
- Dense-zone formula unchanged.
- Volume score unchanged.
- Volatility score unchanged.
- Backtest score unchanged.
- L1-L10 stages unchanged.
- Stop-loss and profit-floor formulas unchanged.
- Final ranking weights unchanged.
- Real-mode and read-only/safe/no-real-orders guards unchanged.

## Tests
- Full pytest: `323 passed, 13 skipped`.
- New regression: `test_v191_centerline_crossing_touch.py`.
- The 13 skipped tests are browser/Playwright or Mac-local formal-gate evidence checks and cannot be counted as formal production browser E2E pass.

## 5050 runtime smoke
A fresh 5050 runtime was checked after the v10.91 change.
- Main pages and system APIs returned HTTP 200.
- `/api/system/formula-audit` reported v10.91 / D+E/v10.91.
- `/api/coins` returned visible candidates sorted by final score descending.
- Formal live readiness remained blocked.

## Formal live readiness
v10.91 still does **not** meet true-fund formal-live standard. Required production evidence remains unavailable from this sandbox, including:
1. Mac local 5050 Playwright/browser E2E evidence with matching version/workdir/time.
2. Evidence that audit workdir is `/Users/andyna/Documents/自動滾倉系統設計`.
3. Fresh realtime prices, entry-zone status/score/ranking sync E2E evidence.
4. All visible candidate coins with 365-day/about 2190 4H K-line backtest evidence.
5. Signed Binance reconciliation clean evidence.
6. Complete safety evidence for rate-limit backoff, disconnect/reconnect, order idempotency, timeout query-order recovery, duplicate order guard, circuit breaker, close-all, and process monitor.
7. Latest-version full pytest evidence accepted by the formal gate.
8. Mac local browser E2E all-pass evidence; sandbox skipped E2E is not sufficient.
9. Formal preflight plus user-approved small-canary evidence.

## Conclusion
v10.91 implements the requested centerline crossing-touch rule and passes executable sandbox tests. Auto Snowball still has **not** reached true-fund formal live standard. Do not switch to real trading and do not place real orders until the formal-live blockers are cleared on the production Mac host.
