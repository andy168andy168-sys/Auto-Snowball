# V10.46 Launch Gate Evidence Report

Status: **NOT READY FOR LIVE CAPITAL**

Reason: not all launch-gate checks have executable evidence. No real order was submitted and real trading mode was not enabled.

## Changes made
- Upgraded package from V10.45 to V10.46.
- Fixed `current_exchange_truth(force=False)` so ordinary pages and `/api/realtime` are cache-first and non-blocking.
- Kept signed Binance REST reconciliation restricted to explicit sync / preflight paths.
- Removed the uploaded local `.binance_api_keys.json` from the release package.

## Runtime / 5050
- Version: 10.46
- Host/port: 127.0.0.1:5050
- Port OK: True
- Actual cwd: `/mnt/data/auto_v10_45_work/auto_snowball_web_v10_45_l1_guard_20`
- Expected primary workdir: `/Users/andyna/Documents/自動滾倉系統設計`

## HTTP 5050 smoke
PASS: `/`, `/auto-select`, `/api/market/live`, `/api/realtime`, `/api/system/runtime`, `/api/system/backtest-evidence`, `/api/system/launch-preflight`, `/api/binance/reconciliation?refresh=0`, `/api/system/formula-audit` returned without Traceback / 500 text.

## Ranking evidence
Sorted by final score descending: **True**

1. TIAUSDC score=53.79 price=0.3726 bars=2190 days=365
2. ETHUSDC score=35.89 price=1603.94 bars=2190 days=365
3. AVAXUSDC score=27.66 price=6.671 bars=2190 days=365
4. KAITOUSDC score=22.52 price=0.5834 bars=2190 days=365
5. ORDIUSDC score=20.01 price=3.616 bars=2190 days=365
6. BTCUSDC score=19.44 price=59751.6 bars=2190 days=365
7. DOGEUSDC score=16.4 price=0.07243 bars=2190 days=365
8. BNBUSDC score=16.3 price=550.01 bars=2190 days=365
9. XRPUSDC score=15.93 price=1.0537 bars=2190 days=365
10. 1000PEPEUSDC score=12.64 price=0.0022986 bars=2190 days=365

## One-year 4H backtest evidence
API `/api/system/backtest-evidence` ok: **True**; visible count: 10; required: 365 days / 2190 bars.

- TIAUSDC: 2190 bars / 365 days / 4h / PASS
- ETHUSDC: 2190 bars / 365 days / 4h / PASS
- AVAXUSDC: 2190 bars / 365 days / 4h / PASS
- KAITOUSDC: 2190 bars / 365 days / 4h / PASS
- ORDIUSDC: 2190 bars / 365 days / 4h / PASS
- BTCUSDC: 2190 bars / 365 days / 4h / PASS
- DOGEUSDC: 2190 bars / 365 days / 4h / PASS
- BNBUSDC: 2190 bars / 365 days / 4h / PASS
- XRPUSDC: 2190 bars / 365 days / 4h / PASS
- 1000PEPEUSDC: 2190 bars / 365 days / 4h / PASS

## Formula audit
- Formula audit ok: True
- Logic version: D+E/v10.34
- Dense zone: center ±1.5%, total width 3%.
- L1 profit guard: trigger +20%, floor +16%, protection ratio 80%.
- Stop loss: capital × max_loss_pct / 100, default 10%.

## Safety / resilience tests
- Full pytest: 192 passed, 12 skipped.
- Non-browser pytest: 192 passed, 12 deselected.
- Safety targeted set: 21 passed.
- Ranking/backtest/formula targeted set: 18 passed.
- Covered: rate-limit backoff, disconnect/reconnect, order idempotency, timeout query-order recovery, duplicate order guard, circuit breaker, close-all confirmation, process monitor.

## Binance reconciliation
Data-quality ok: **False**

Issues:
- account_ok=false
- balance_ok=false
- orders_ok=false
- TIAUSDC: endpoint premiumIndex failed
- TIAUSDC: endpoint commissionRate failed
- TIAUSDC: endpoint leverageBracket failed
- TIAUSDC: endpoint userTrades failed
- TIAUSDC: endpoint income failed
- TIAUSDC: endpoint orders failed
- AVAXUSDC: endpoint premiumIndex failed
- AVAXUSDC: endpoint commissionRate failed
- AVAXUSDC: endpoint leverageBracket failed
- AVAXUSDC: endpoint userTrades failed
- AVAXUSDC: endpoint income failed
- AVAXUSDC: endpoint orders failed
- KAITOUSDC: endpoint premiumIndex failed
- KAITOUSDC: endpoint commissionRate failed
- KAITOUSDC: endpoint leverageBracket failed
- KAITOUSDC: endpoint userTrades failed
- KAITOUSDC: endpoint income failed
- KAITOUSDC: endpoint orders failed

Public Binance read-only price sample through connector:
- TIAUSDC: 0.3713000
- ETHUSDC: 1599.20
- BTCUSDC: 59607.5

## Launch preflight
Preflight ok: **False**

Checks:
- PASS｜5050 實際執行埠正確
- BLOCK｜正式 API 金鑰已設定
- PASS｜交易所真值新鮮
- BLOCK｜即時 Mark Price 新鮮
- PASS｜公式守門通過
- PASS｜所有可見候選幣有一年 4H 回測實證
- PASS｜熔斷器未打開
- BLOCK｜小額灰度需手動確認

Blocking items:
- 正式 API 金鑰已設定
- 即時 Mark Price 新鮮
- 小額灰度需手動確認

## Browser E2E limitation
The sandbox Chromium blocks localhost navigation with `ERR_BLOCKED_BY_ADMINISTRATOR`. Therefore browser-console E2E cannot be counted as passed in this environment. HTTP-level 5050 smoke passed, but formal browser E2E remains a blocking item until rerun in the user's local Chrome/Playwright environment.

## Decision
Do **not** declare live-capital readiness. Do not switch to real mode and do not place real orders.
