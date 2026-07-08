# Auto Snowball v10.81 Sandbox Formal Live Gate Audit — 2026-07-08

## Scope
- Input package: `auto_snowball_web_v10_80_centerline_entry_gate_e2e.zip`.
- Output package: `auto_snowball_web_v10_81_ranking_centerline_score_sync_e2e.zip`.
- Requested change: update auto-select/ranking so the old `入區分` concept fully matches the v10.80 centerline-entry gate.
- Sandbox cannot access Mac production workdir `/Users/andyna/Documents/自動滾倉系統設計`.
- Safety flags used: `AUTO_SNOWBALL_SAFE_MODE=1`, `AUTO_SNOWBALL_NO_REAL_ORDERS=1`, `AUTO_SNOWBALL_READ_ONLY=1`, `BINANCE_READ_ONLY=1`.
- No real orders were placed. No real trading mode was enabled.

## Change summary
- Version bumped to `10.81` / `D+E/v10.81`.
- Ranking label changed from `入區分` / `現價入區狀態` to `中線入場分` / `中線入場狀態`.
- Ranking basis changed from `zone_entry*25%` wording to `centerline_entry*25%` wording.
- Ranking 25% entry score now follows the v10.80 execution gate:
  - touched/crossed dense-zone centerline = 100;
  - inside dense zone but not at centerline = score by `dense_centerline_distance_pct`;
  - outside dense zone = low score only.
- Added compatibility aliases: `centerline_entry_score_100` and `centerline_entry_score`, while preserving existing `zone_entry_score_100` and `zone_entry_score` fields.
- Added regression tests for centerline ranking score sync.

## Test results
- Full pytest: `289 passed, 13 skipped`.
- 13 skipped tests are sandbox/browser/Mac-local evidence checks and cannot be counted as formal production browser E2E pass.

## 5050 runtime smoke
A fresh 5050 runtime was started from the inspected v10.81 package. The following returned HTTP 200 without Traceback/Internal Server Error text:
- `/`
- `/auto-select`
- `/api/status`
- `/api/coins`
- `/api/system/formula-audit`
- `/api/engine/parameters`
- `/api/system/formal-live-readiness`

## Ranking / centerline score verification
- `/api/coins` returned 10 visible candidates sorted by final `score` descending.
- Sample first row: BTCUSDC score `68.5`.
- Sample `zone_entry_score_100` and `centerline_entry_score_100` both returned `78.06`, proving the new alias and compatibility field are synchronized.
- Sample `dense_centerline_distance_pct`: `0.3177048233368634`.
- Sample state: `dense_entry_ready=false`, `dense_zone_arrival_status=區內未到中線`, confirming mere dense-zone entry does not arm L1 and no longer produces a 100 entry score.
- `/api/system/formula-audit`: `ok=true`, `version=10.81`, `logic_version=D+E/v10.81`.
- Ranking formula basis: `final_score = volume*20% + volatility*15% + dense_zone*30% + backtest*10% + centerline_entry*25% - risk_penalty`.

## Formal live readiness
`/api/system/formal-live-readiness` returned:
- `formal_live_ready=false`
- `ok=false`
- `must_not_claim_live_ready=true`
- blocking items: 9

Blocking items remain external/production evidence blockers, including Mac-local 5050 Playwright/browser E2E, production workdir evidence, fresh realtime sync evidence, 365-day/2190-bar 4H backtest evidence for all visible candidates, signed Binance reconciliation, complete safety evidence, and user-approved small-canary evidence.

## Conclusion
v10.81 completes the requested auto-select/ranking centerline-score sync and passes all executable sandbox tests. Auto Snowball still has **not** reached true-fund formal live standard. Do not switch to real trading and do not place real orders until the formal-live blockers are cleared on the production Mac host.
