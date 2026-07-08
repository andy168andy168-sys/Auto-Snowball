# Auto Snowball v10.83 Sandbox Formal Live Gate Audit — 2026-07-08

## Scope
- Input package: `auto_snowball_web_v10_82_dense_line_green_e2e.zip`.
- Output package: `auto_snowball_web_v10_83_volume_percentage_fairness_e2e.zip`.
- Requested change: update volume score to use 1-day, 7-day, 14-day and 30-day average quote-volume percentages, with A/B sync and E2E.
- Sandbox cannot access Mac production workdir `/Users/andyna/Documents/自動滾倉系統設計`.
- Safety flags used: `AUTO_SNOWBALL_SAFE_MODE=1`, `AUTO_SNOWBALL_NO_REAL_ORDERS=1`, `AUTO_SNOWBALL_READ_ONLY=1`, `BINANCE_READ_ONLY=1`.
- No real orders were placed. No real trading mode was enabled.

## Change summary
- Version bumped to `10.83` / `D+E/v10.83`.
- Added `VOLUME_SCORE_CONFIG` with `basis=percentage_fairness`.
- New score windows from 4H quoteVolume:
  - `V1`: recent 6 bars / 1 day;
  - `V7`: recent 42 bars / 7 days;
  - `V14`: recent 84 bars / 14 days;
  - `V30`: recent 180 bars / 30 days.
- New percentages:
  - `P1 = V1 / V7 × 100`;
  - `P7 = V7 / V14 × 100`;
  - `P14 = V14 / V30 × 100`.
- Growth score conversion: `<=70% → 0`, `100% → 50`, `>=200% → 100`.
- 30-day base liquidity score uses log10 scaling from 10M to 100M USDC/day.
- Final volume score100 = `(S1×40% + S7×25% + S14×20% + B30×15%) × (0.5 + 0.5×B30/100)`.
- Compatibility aliases remain for older UI/tests, but the underlying volume score is now percentage-fairness based.

## Tests
- Full pytest: `297 passed, 13 skipped`.
- 13 skipped tests are sandbox/browser/Mac-local evidence checks and cannot be counted as formal production browser E2E pass.

## 5050 runtime smoke
A fresh 5050 runtime was started from the inspected v10.83 package. The following returned HTTP 200 without Traceback/Internal Server Error text:
- `/`
- `/auto-select`
- `/calculator`
- `/realtime`
- `/audit-center`
- `/virtual-account`
- `/real-account`
- `/control-panel`
- `/api/status`
- `/api/coins`
- `/api/system/formula-audit`
- `/api/engine/parameters`
- `/api/system/formal-live-readiness`

## A/B sync verification
- `/api/system/formula-audit`: `ok=true`, `version=10.83`, `logic_version=D+E/v10.83`.
- Formula audit exposes `ranking_score.volume_score.config.basis = percentage_fairness`.
- A/B checks include `volume_score_basis` and `volume_score_component_weights`; both passed.
- Regression tests verify backend formula, 4H window conversion, UI-compatible output fields, and formula-audit contract.

## Formal live readiness
`/api/system/formal-live-readiness` still returned:
- `formal_live_ready=false`
- `ok=false`
- `must_not_claim_live_ready=true`
- blocking items: 9

Blocking items remain external/production evidence blockers, including Mac-local 5050 Playwright/browser E2E, production workdir evidence, fresh realtime sync evidence, 365-day/2190-bar 4H backtest evidence for all visible candidates, signed Binance reconciliation, complete safety evidence, and user-approved small-canary evidence.

## Conclusion
v10.83 implements the requested volume-score percentage fairness update and passes all executable sandbox tests. Auto Snowball still has **not** reached true-fund formal live standard. Do not switch to real trading and do not place real orders until the formal-live blockers are cleared on the production Mac host.
