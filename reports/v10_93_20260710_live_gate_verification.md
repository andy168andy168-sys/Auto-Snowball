# Auto Snowball v10.93 Live Gate Verification - 2026-07-10

## Runtime Truth
- Primary audit workdir: `/Users/andyna/Documents/自動滾倉系統設計`.
- Actual `127.0.0.1:5050` runtime: version `10.92`, cwd `/Users/andyna/Spyder/auto_snowball_web_v10_92_centerline_then_breakout_e2e`, pid `68412`, started `2026-07-10 00:57:04`.
- v10.93 was packaged as a candidate release only. The active 5050 process was not restarted into v10.93.

## Fix Summary
- Found and fixed a centerline state recording/display issue: after a no-position coin touched or crossed the dense-zone centerline, live rows could show the instantaneous state as `未到中線` even though the engine plan was already `ARMED_L1`.
- v10.93 overlays persisted engine `ARMED_L1` state into live rows, prevents display-only row eligibility from arming execution plans, and resets completed cycles to `WAITING_CENTERLINE`.
- This matches the rule: no-position coins must first touch/cross the centerline, then wait for a later dense-zone upper/lower breakout to open L1; after a completed close, the next cycle must wait for a fresh centerline touch/cross.

## Validation
- Targeted regression: `24 passed, 1 warning in 0.22s`.
- Syntax: `python3 -m py_compile main.py` passed.
- Full runtime pytest: `342 passed, 1 warning in 33.42s`.
- v10.93 browser E2E on isolated/in-process runtime: `13 passed, 1 warning in 24.30s`.
- Actual 5050 browser sweep: 8 pages and `/api/market/live` all returned HTTP 200; console/page errors and non-favicon failed responses were 0.
- Final extracted v10.93 release archive pytest: `342 passed, 1 warning in 32.11s`.
- Release archive forbidden file scan: no credentials, runtime cache/state, formal evidence, pytest/python cache, log, db, or git metadata entries were found.

## Launch Gate
- `/api/system/launch-preflight`: `ok=false`.
- Blocking items: `正式 API 金鑰已設定=false`, `小額灰度需手動確認=false`.
- All 10 visible candidates reported 365 days / 2190 4H bars.
- `/api/system/formal-live-readiness`: `formal_live_ready=false`; do not claim `已達正式上線標準`.

## Binance And Performance
- Virtual reconciliation: data quality ok, 4 symbols checked, demo futures base URL.
- Real reconciliation: data quality failed; private userTrades / income / orders / commissionRate / leverageBracket coverage was incomplete.
- Virtual daily performance: `不可判定`; 0 complete closed rounds, history starts with a closing fill.
- Real daily performance: `不可判定`; private history coverage incomplete, 0 complete closed rounds.
- No leaderboard backtest score was used as true win rate.

## Dense Width Research
- Read-only refresh; runtime parameters were not modified.
- Candidate widths by validation rule: 1.0%, 1.5%, 2.5%, 3.0%, 4.0%.
- 2.0% failed the candidate rule with validation win rate below 70%.
- These are advisory only and do not authorize parameter changes.

## Release
- Local package: `releases/v10.93/auto_snowball_web_v10_93_fresh_centerline_cycle_guard.zip`.
- SHA256: `387bbfeb345486a2ad0f1cf7d78b0819a429ef8df95aef0b93f04ff1673c07bb`.
- Manifest status: `blocked`.

## Safety Note
- No real mode switch and no real order were performed.
- During safety probing, a virtual-mode `start` action returned 200 on the active v10.92 runtime and briefly set virtual `running=true`; it was immediately reverted with `stop`, and final status was `running=false`. This probe is not counted as safety-pass evidence.
