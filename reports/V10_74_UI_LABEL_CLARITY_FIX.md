# V10.74 UI Label Clarity Fix

## Finding

BNB dense-zone bounds such as `560.1421 – 577.2023` are consistent with the active formula: six-line center ±1.5%, total width 3.00%.

The issue was display wording: `六線密集距離` could be confused with the trading dense-zone width. The value represents the MA/EMA six-line spread, not the final trade-zone total width.

## Fix

- Change visible column label to `六線分散距離`.
- Display `交易密集區寬度 3.00%` separately under the dense-zone bounds.
- Add formula-audit display-label contract:
  - `six_line_zone_distance_pct` => `六線分散距離`
  - `dense_zone_total_pct` => `交易密集區寬度`
  - `dense_zone_distance_pct` => `現價距離密集區`
- Keep dense-zone formula, L1 logic, stop-loss and profit-protection logic unchanged.

## Local validation

- Targeted regression: `10 passed`.
- Full pytest: `281 passed, 13 skipped`.
- HTTP smoke on safe local port 5055: `/strategy/1`, `/auto-select`, `/api/system/formula-audit` all HTTP 200.
- Release archive generated: `auto_snowball_web_v10_74_ui_label_clarity_e2e.zip`.
- Archive SHA256: `4bbd3b78a850d7130e96d07d8f40fc6d8d3b59dc90e1b11ed34787cc51271db9`.

## Launch gate

Formal live-capital status remains `blocked`. This report does not approve live trading or mode switching.
