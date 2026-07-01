# V10.48 Launch Gate Report — NOT READY FOR LIVE CAPITAL

本次檢查遵守：禁止自動下真實訂單、禁止切換真實交易模式。

## 結論

未達正式上線標準。不可通知「已達正式上線標準」。

## 已修正 / 升級

- V10.48 修正一年 4H 回測證據：即使阻擋，也必須輸出 machine-readable `bars=0`, `lookback_days=0`, `interval=4h`, `ok=false`，避免守門測試 TypeError 或假通過。
- 同步 Audit Center A 端顯示至 `最新 D/E/v10.48 邏輯`，與 B 端 `main.VERSION` / formula audit 一致。
- 保留 V10.47 的密集區中心 ±1%、總寬度 2% 與 A→B 同步守門。

## 5050 Runtime

- Runtime version: `10.48`
- Host/port: `127.0.0.1:5050`, `port_ok=true`
- Actual cwd: `/mnt/data/auto_snowball_web_v10_48_live_gate_machine_readable_e2e`
- Expected primary workdir: `/Users/andyna/Documents/自動滾倉系統設計`
- 判定：sandbox 5050 可用，但無法直接驗證使用者 Mac 本機工作目錄。

## Tests

- Targeted safety/formula/A→B tests: `35 passed`
- Full pytest: `196 passed, 12 skipped`
- Browser Playwright E2E: `6 skipped` because sandbox Chromium blocks localhost with `ERR_BLOCKED_BY_ADMINISTRATOR`; therefore this is not a full browser pass.

## Formula / Dense Zone

- Formula audit: `ok=true`
- Logic version: `D+E/v10.48`
- Dense zone center: `(six_line_high + six_line_low) / 2`
- Dense zone low: `center * 0.99`
- Dense zone high: `center * 1.01`
- Half width: `1.0%`
- Total width: `2.0%`
- A→B sync: `ok=true`

## Ranking / Realtime

- Top10 sorted by final score descending: `true`
- Active realtime symbols: `BTCUSDC`, `ETHUSDC`, `SOLUSDC`, `BNBUSDC`
- 5050 smoke endpoints `/`, `/auto-select`, `/realtime`, `/audit-center`, `/api/status`, `/api/system/runtime`, `/api/system/formula-audit`, `/api/market/live`, `/api/realtime`, `/api/system/backtest-evidence`, `/api/system/launch-preflight`, `/api/binance/reconciliation?refresh=0`, `/api/system/process-monitor`, `/api/ws/status` all returned HTTP 200 in sandbox.

## Blocking Items

- 5050 actual cwd is sandbox path, not the requested Mac workdir; Mac `/Users/andyna/Documents/自動滾倉系統設計` cannot be verified here.
- Missing 365-day / ~2190 4H backtest proof for all visible candidates.
- Formal launch preflight is not satisfied.
- Binance reconciliation `dataQuality` is not clean: `account_ok=false`, `balance_ok=false`, `orders_ok=false`.
- Runtime WebSocket mark price freshness is false / no fresh mark price in sandbox runtime.
- Browser Playwright E2E skipped in sandbox due Chromium localhost policy; not a full browser pass.

## Binance / Preflight Details

- Backtest evidence: `ok=false`, `blocking_count=10`.
- Launch preflight: `ok=false`.
- Preflight blockers: formal API keys not set, mark price freshness false, all visible candidates missing one-year 4H proof, small canary manual confirmation required.
- Reconciliation dataQuality: `ok=false`; issues: `account_ok=false`, `balance_ok=false`, `orders_ok=false`.

## Live Gate Result

`NOT_READY_FOR_LIVE_CAPITAL`

Do not send real orders. Do not switch to live trading mode.