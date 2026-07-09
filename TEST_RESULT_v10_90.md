# TEST_RESULT v10.90

## Code Verification
- Centerline/formula targeted regression: `12 passed, 1 warning`.
- Full pytest from the patched v10.90 runtime tree: `333 passed, 1 warning`.
- Full pytest from the extracted v10.90 release archive: `333 passed, 1 warning`.
- Workspace release/tooling pytest: `25 passed`.
- Release archive test placement: `RELEASE_ARCHIVE_TEST_PLACEMENT=PASS`.

## Actual 5050 Browser E2E
- Runtime checked: `127.0.0.1:5050`, current process version `10.89`.
- Pages checked with Chromium/Playwright: `/`, `/auto-select`, `/calculator`, `/realtime`, `/audit-center`, `/virtual-account`, `/real-account`, `/control-panel`, plus `/api/market/live`.
- Result after per-page stabilization: all returned HTTP 200; requestfailed/pageerror/console error count was `0`.
- `/api/market/live`: 10 rows; final scores sorted descending; price, entry-zone status, entry score and rank refreshed.

## Isolated v10.90 Browser E2E
- Extracted archive started read-only on `127.0.0.1:5051`, not deployed to live 5050.
- Same 8-page plus `/api/market/live` Playwright sweep returned HTTP 200 with requestfailed/pageerror/console error count `0`.
- The isolated local gate intentionally failed the formal 5050 port check because 5051 cannot be used as formal launch evidence.

## Launch Gate
- Local 5050 launch gate with Binance public kline coverage result: `LOCAL_LAUNCH_GATE=FAIL`.
- Failure reason was limited to formal launch preflight blockers:
  - `正式 API 金鑰已設定`
  - `小額灰度需手動確認`
- All 10 visible USDC candidates had 2190 one-year 4H Binance klines: `ARBUSDC`, `BNBUSDC`, `BTCUSDC`, `DOGEUSDC`, `ETHUSDC`, `KAITOUSDC`, `ORDIUSDC`, `TIAUSDC`, `UNIUSDC`, `XRPUSDC`.

## Binance And Daily Performance
- Signed read-only reconciliation refresh:
  - `dataQuality.ok=true`
  - `account_ok=true`
  - `balance_ok=true`
  - `orders_ok=true`
  - `symbols_checked=4`
- Daily U-margined futures performance:
  - virtual account: `不可判定`; reason: trade history starts from closing fills and lacks matching opening fills.
  - real account: `不可判定`; reason: complete private `userTrades` / `allOrders` / `income` or full-account symbol coverage is incomplete.
- Open positions were not counted in win rate; leaderboard backtest score was not used as real win rate.

## Dense-Width Research
- Read-only POST refresh completed for all visible candidates; no runtime parameter was changed.
- Candidate widths by rule `validation_samples >= 30` and `validation_win_rate_pct >= 70`:
  - 1.0% total width: 140 validation samples, 74.29% validation win rate, 7.43 wins per 10, 7-win ratio 81.68%, 8-win ratio 61.07%, max losing streak 4.
  - 1.5% total width: 159 validation samples, 71.07% validation win rate, 7.11 wins per 10, 7-win ratio 78.00%, 8-win ratio 54.00%, max losing streak 7.
  - 2.5% total width: 174 validation samples, 71.84% validation win rate, 7.18 wins per 10, 7-win ratio 70.91%, 8-win ratio 43.64%, max losing streak 4.
  - 3.0% total width: 186 validation samples, 72.58% validation win rate, 7.26 wins per 10, 7-win ratio 70.06%, 8-win ratio 42.94%, max losing streak 4.
  - 4.0% total width: 200 validation samples, 72.00% validation win rate, 7.20 wins per 10, 7-win ratio 65.45%, 8-win ratio 43.98%, max losing streak 4.
- 2.0% total width is not a candidate: 170 validation samples, 68.24% validation win rate.
- Recent real-trade difference remains `不可判定`; no fixed 10-trade 7-8 win outcome is promised.

## Safety
- Direct 5050 probes:
  - DNS rebinding Host probe: HTTP 403.
  - Mutating GET `/api/engine/tick?trade=1`: HTTP 405.
  - GET refresh `/api/binance/reconciliation?refresh=1`: HTTP 405.
  - GET refresh `/api/research/dense-width?refresh=1`: HTTP 405.
  - Cross-site POST to signed reconciliation refresh: HTTP 403.
  - `/api/engine/close-all` without `confirm=CLOSE_ALL`: HTTP 400, no close-all executed.
- Process monitor stayed `ok=true`; circuit breaker `open=false`.
- No real trading mode switch, no runtime trading restart, and no real order was performed.

## Package
- `releases/v10.90/auto_snowball_web_v10_90_centerline_crossing_guard.zip`
- SHA256: `7af4c846f71321b68adab6054b6ea7bd406303d3d9765f32f186020aa8a663b4`
- Zip scan: 292 files, forbidden secret/cache/state/evidence artifacts found: 0.
