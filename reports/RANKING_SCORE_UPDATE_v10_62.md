# Auto Snowball v10.62 Ranking Score Update

## User requested formula

`final_score = 成交量分 ×20% + 波動分 ×15% + 密集區分 ×30% + 回測分 ×10% + 入區分 ×25% - 風險扣分`

## Implementation

- Added `RANKING_SCORE_WEIGHTS`:
  - volume: 20
  - volatility: 15
  - dense_zone: 30
  - backtest: 10
  - zone_entry: 25
  - risk_penalty_max: 10
- All positive factors are converted to 0-100 percentage scores before weighting.
- `calc_strategy_rank_fields()` now uses only the new weighted formula for `base_score` and `score`.
- `a_to_b_sync_contract_payload()` now verifies ranking weights in addition to dense-zone settings.
- `current_formula_audit_payload()` exposes the ranking formula and weights.
- Frontend/template stale dense-zone 2% wording was corrected to 3% where it affected current pages.
- Added regression test `test_v165_ranking_score_weight_sync.py`.

## Validation

- Targeted ranking / A-B formula tests: `30 passed`.
- Full pytest: `248 passed, 13 skipped`.
- 5050 smoke: root, auto-select, status, formula-audit, market-live, realtime, runtime all returned 200.

No real orders were placed and no real trading mode was enabled.
