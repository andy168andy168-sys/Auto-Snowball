# V10.51 launch-gate recheck

Audit time: 2026-07-02T15:35:45+08:00

## Actual 5050 runtime

- Runtime: V10.51 at `/Users/andyna/Spyder/auto_snowball_web_v10_51_book_stream_resubscribe_e2e`.
- Port 5050 and process-monitor identity passed.
- ZIP, reconstructed release parts and runtime code tree matched.

## Technical evidence

- 10 visible candidates were ranked by descending final score with ranks 1–10.
- Price updates advanced between snapshots; entry status, entry score and rank fields were present and synchronized.
- All visible candidates, including WIFUSDC, BTCUSDC and BNBUSDC held-position inserts, had 365 days / 2190 bars / 4H evidence.
- Formula audit and dense-zone A→B synchronization passed.
- Book stream stayed `connected`, `book_ticker_count=10`, and event timestamps advanced.
- Binance reconciliation diagnostics passed with no data-quality issues; all held positions remained visible.
- Public Binance mark prices were available for all 10 visible symbols and agreed with runtime prices within 0.1% at observation time.
- Full pytest: `216 passed`; safety/WebSocket: `27 passed`; isolated browser E2E: `12 passed`; actual 5050 Playwright: `2 passed`.
- Release tooling regressions: `17 passed`; reconstructed hash matched the manifest; test-placement and static production gates passed.

## Result

`NOT_READY_FOR_LIVE_CAPITAL`

Blocking items:

- `正式 API 金鑰已設定`
- `小額灰度需手動確認`

All verification was read-only. No real order was sent and live mode was not enabled.
