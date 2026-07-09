# Auto Snowball v10.90 Formal Live Gate Audit - 2026-07-10

## Summary
Auto Snowball has not reached true-fund formal live standard.

v10.90 fixes the live centerline crossing display logic and has been packaged and verified, but the current `127.0.0.1:5050` process is still v10.89. It was not automatically restarted, deployed, switched to real mode, or used to place a real order.

## Fixed In v10.90
- WebSocket mark-price updates now keep the previous mark price.
- Live candidate rows now receive the previous mark price before dense-zone centerline status is calculated.
- If BNB or any other symbol moves from above the dense-zone centerline to below it, the row is now treated as having touched/crossed the centerline.
- Local formal-live evidence is excluded from the release archive.

Expected UI after the fixed version is deployed: `dense_zone_arrival_status=已進入中線`, `中線：已觸及`, and distance to centerline shown as `0.00%` at the crossing event.

## Actual 5050 Runtime
- Runtime endpoint: `http://127.0.0.1:5050/api/system/runtime`.
- Current process version: `10.89`.
- Runtime cwd: `/Users/andyna/Spyder/auto_snowball_web_v10_89_credential_state_hardening_e2e`.
- Required primary workdir: `/Users/andyna/Documents/自動滾倉系統設計`.
- Port and host: `127.0.0.1:5050`, reachable.
- Formal preflight blockers: `正式 API 金鑰已設定=false`, `小額灰度需手動確認=false`.

## Browser E2E
- Actual 5050 per-page Playwright sweep covered `/`, `/auto-select`, `/calculator`, `/realtime`, `/audit-center`, `/virtual-account`, `/real-account`, `/control-panel`, and `/api/market/live`.
- Result: all HTTP 200; requestfailed/pageerror/console error count `0`.
- Isolated v10.90 archive on `127.0.0.1:5051` passed the same sweep, then the 5051 process was stopped.

## Candidate Evidence
- Visible candidates from the actual 5050 local gate: `ARBUSDC`, `BNBUSDC`, `BTCUSDC`, `DOGEUSDC`, `ETHUSDC`, `KAITOUSDC`, `ORDIUSDC`, `TIAUSDC`, `UNIUSDC`, `XRPUSDC`.
- Full public-kline verifier confirmed 2190 Binance 4H bars for each visible candidate.
- Formula audit passed.
- Market/live validation confirmed ranking by final score descending plus live price, entry-zone status, entry score and rank refresh.

## Binance Reconciliation
Signed read-only reconciliation refresh:
- `dataQuality.ok=true`.
- `account_ok=true`.
- `balance_ok=true`.
- `orders_ok=true`.
- `symbols_checked=4`.

## Daily Binance Performance
Daily U-margined futures performance remains not determinable:
- Virtual account: `不可判定`; trade history starts from closing fills and lacks matching opening fills.
- Real account: `不可判定`; complete private `userTrades`, `allOrders`, `income` or full-account symbol coverage is incomplete.

No leaderboard backtest score was used as real win rate, and open positions were excluded.

## Dense-Width Research
Read-only dense-width refresh completed without changing runtime parameters, restarting trading, placing orders or switching real mode.

| Total width | Center range | Validation samples | Validation win rate | Wins per 10 | 7-win ratio | 8-win ratio | Max losing streak | Candidate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1.0% | +/-0.5% | 140 | 74.29% | 7.43 | 81.68% | 61.07% | 4 | yes |
| 1.5% | +/-0.75% | 159 | 71.07% | 7.11 | 78.00% | 54.00% | 7 | yes |
| 2.0% | +/-1.0% | 170 | 68.24% | 6.82 | 65.84% | 36.02% | 6 | no |
| 2.5% | +/-1.25% | 174 | 71.84% | 7.18 | 70.91% | 43.64% | 4 | yes |
| 3.0% | +/-1.5% | 186 | 72.58% | 7.26 | 70.06% | 42.94% | 4 | yes |
| 4.0% | +/-2.0% | 200 | 72.00% | 7.20 | 65.45% | 43.98% | 4 | yes |

Research recommendation only: 1.0% has the strongest validation win rate in this run. No fixed 10-trade 7-8 win outcome is promised, and no runtime parameter was changed.

## Tests
- Centerline/formula targeted regression: `12 passed`.
- Full pytest on patched v10.90 runtime tree: `333 passed`.
- Full pytest on extracted v10.90 archive: `333 passed`.
- Workspace release tests: `25 passed`.
- Release archive test placement: `PASS`.
- Local 5050 launch gate: failed only on formal preflight blockers `正式 API 金鑰已設定` and `小額灰度需手動確認`.

## Safety Probes
- DNS rebinding Host probe: HTTP 403.
- Mutating GET `/api/engine/tick?trade=1`: HTTP 405.
- GET refresh `/api/binance/reconciliation?refresh=1`: HTTP 405.
- GET refresh `/api/research/dense-width?refresh=1`: HTTP 405.
- Cross-site POST to signed reconciliation refresh: HTTP 403.
- `/api/engine/close-all` without `confirm=CLOSE_ALL`: HTTP 400.
- Process monitor: `ok=true`; circuit breaker `open=false`.

## Package
- `releases/v10.90/auto_snowball_web_v10_90_centerline_crossing_guard.zip`.
- SHA256: `7af4c846f71321b68adab6054b6ea7bd406303d3d9765f32f186020aa8a663b4`.
- Zip scan: 292 files, forbidden secret/cache/state/evidence artifacts found: 0.

## Formal Decision
Not ready for true-fund formal launch.

Blocking items:
- Formal real-account API credentials are not configured.
- Manual small-canary approval is missing.
- Daily virtual and real performance are both `不可判定`.
- v10.90 is packaged but not deployed to the actual 5050 runtime.
- GitHub sync still needs successful remote upload/PR evidence before it can be treated as complete.
