# V10.78 L1 Stop 100 Sync

Local release v10.78 was prepared.

Change:
- L1 stop loss changed from 50 percent of capital to 100 percent of capital.
- Default 100 USDC example now has max-loss close line at -100 USDC.
- A-to-B sync, formula audit, frontend defaults, README, and tests were synchronized.

Validation:
- Targeted regression: 23 passed.
- Non-browser pytest: 284 passed, 6 skipped, 8 deselected.
- Browser group: 1 passed, 7 skipped in the managed sandbox.
- HTTP API E2E on 127.0.0.1:5050 returned 200 for key pages and APIs.

Safety:
- No real Binance orders were sent.
- No trading mode was changed.
- Formal live approval still requires separate local Mac and private Binance evidence.
