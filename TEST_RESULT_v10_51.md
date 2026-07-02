# TEST_RESULT v10.51

Recheck time: 2026-07-02T15:35:45+08:00

## Result

- Actual `127.0.0.1:5050`: V10.51 at `/Users/andyna/Spyder/auto_snowball_web_v10_51_book_stream_resubscribe_e2e`.
- Source ZIP and actual runtime code tree: identical after excluding runtime state/cache files.
- Release ZIP SHA256 and reconstructed base64-parts SHA256: `0801340950d53cff8b11dbe593f813c6514b5440cfa8ee3cc692d1f26421f41b`.
- Full clean-release pytest: `216 passed in 29.04s`.
- Production-safety/WebSocket regression suite: `27 passed in 0.57s`.
- Isolated browser E2E suite: `12 passed in 27.42s`.
- Actual 5050 read-only Playwright verification: `2 passed in 9.52s`.
- Release tooling regression suite: `17 passed`; reconstructed ZIP hash matched the manifest exactly.
- Release test-placement gate and static production gate: `PASS`.
- All 10 visible USDC candidates: `365` days / `2190` 4H bars; held-position inserts were included.
- Formula audit, A→B synchronization, WebSocket/book status, Binance reconciliation and public mark-price cross-check passed.

## Formal blockers

- `正式 API 金鑰已設定=false`
- `小額灰度需手動確認=false`

Result: **NOT READY FOR LIVE CAPITAL**.

No real order was sent and live mode was not enabled.
