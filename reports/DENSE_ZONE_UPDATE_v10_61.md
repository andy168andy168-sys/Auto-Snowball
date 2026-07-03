# Auto Snowball v10.61 Dense Zone Update

Dense-zone formula updated in the generated v10.61 package.

## Updated contract

- A-side config: `MA_CONFIG.dense_zone_half_pct = 1.5`, `dense_zone_max_width_pct = 3.0`, `density_threshold_pct = 3.0`.
- B-side formula constants: `DENSE_ZONE_HALF_WIDTH_PCT = 0.015`, `DENSE_ZONE_MAX_WIDTH_PCT = 0.03`.
- Formula audit: low `center * 0.985`, high `center * 1.015`, half width `1.5`, total width `3.0`.
- Frontend labels: dense quality threshold is now `<=3% / >3%`.
- New regression test: `test_v161_dense_zone_3pct_a_to_b_sync.py`.

## Validation

- v10.61 A-to-B dense-zone tests: `3 passed`.
- Dense/formula/A-to-B/HTTP E2E related tests: `39 passed`.
- Full pytest: `245 passed, 13 skipped`.
- Browser E2E: `13 skipped` in the sandbox because Chromium policy blocked localhost; rerun on the Mac local 5050 environment for production evidence.
- 5050 smoke: root, auto-select, status, formula-audit, market-live, realtime, and runtime endpoints returned 200.

## Package

- Generated archive: `auto_snowball_web_v10_61_dense_zone_3pct_a_to_b_e2e.zip`.
- SHA256: `6a555dadeef008e5950cfb36841505652a7de331eed99931366d27ff2987dee3`.
