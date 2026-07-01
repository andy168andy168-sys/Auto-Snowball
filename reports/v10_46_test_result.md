# V10.46 Test Result

- Full pytest: `192 passed, 12 skipped in 14.36s`.
- Non-browser pytest: `192 passed, 12 deselected in 1.04s`.
- Safety targeted tests: `21 passed in 0.71s`.
- Ranking/backtest/formula targeted tests: `18 passed in 0.57s`.
- 5050 HTTP smoke: PASS; no 500/Traceback on primary pages and launch-gate APIs.
- Browser E2E: not counted as pass in this sandbox because Chromium blocked localhost with `ERR_BLOCKED_BY_ADMINISTRATOR`; tests now skip cleanly instead of failing/hanging.
- Launch preflight: NOT READY. Blocking items: 正式 API 金鑰已設定, 即時 Mark Price 新鮮, 小額灰度需手動確認.
- No real order was submitted and real trading mode was not enabled.
