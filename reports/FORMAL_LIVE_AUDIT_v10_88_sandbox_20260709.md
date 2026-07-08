# Auto Snowball v10.88 Sandbox Formal Live Gate Audit — 2026-07-09

## Scope
- Input package: `auto_snowball_web_v10_87_websocket_listen_key_redaction.zip`.
- Output package: `auto_snowball_web_v10_88_release_secret_hygiene_e2e.zip`.
- Requested automation scope: sync GitHub, inspect for vulnerabilities, fix if found, run E2E, and check formal live readiness.
- Sandbox cannot access Mac production workdir `/Users/andyna/Documents/自動滾倉系統設計`.
- Safety flags used: `AUTO_SNOWBALL_SAFE_MODE=1`, `AUTO_SNOWBALL_NO_REAL_ORDERS=1`, `AUTO_SNOWBALL_READ_ONLY=1`, `BINANCE_READ_ONLY=1`.
- No real orders were placed. No real trading mode was enabled.

## Vulnerability found and fixed
- Found a real packaging vulnerability in the incoming v10.87 candidate: a local Binance credential file was included in the release zip.
- The report intentionally does not reproduce or display the credential values.
- v10.88 removes the local credential file from the release artifact.
- v10.88 also removes Python/pytest caches, runtime state/cache files, logs and pid files from the release artifact.
- Added `.binance_api_keys.example.json` with placeholder-only values.
- Added `test_v188_release_secret_hygiene.py` to prevent the local key file from being shipped again and to keep ignore patterns synchronized.

## Change summary
- Version bumped to `10.88` / `D+E/v10.88`.
- Only release/package secret hygiene was changed.
- Unchanged formulas: dense-zone, centerline gate, L1 entry boundaries, volume score, volatility score, backtest score, L1-L10 stages, stop-loss, profit-floor protection, final ranking weights, safety gates.
- WebSocket listen-key redaction from v10.87 remains active.
- Dense-width cache canonical visible-symbol key behavior from v10.87 remains active.

## Tests
- Full pytest after A/B test-version sync: `318 passed, 13 skipped`.
- 13 skipped tests are sandbox/browser/Mac-local evidence checks and cannot be counted as formal production browser E2E pass.

## 5050 runtime smoke
A fresh 5050 runtime was started from the inspected v10.88 package. The following returned HTTP 200 without Traceback/Internal Server Error text:
- `/`
- `/auto-select`
- `/calculator`
- `/realtime`
- `/audit-center`
- `/virtual-account`
- `/real-account`
- `/control-panel`
- `/api/status`
- `/api/coins`
- `/api/system/formula-audit`
- `/api/engine/parameters`
- `/api/system/formal-live-readiness`
- `/api/binance/daily-performance`
- `/api/binance/daily-performance?mode=real`
- `/api/research/dense-width`

## A/B sync verification
- `/api/system/formula-audit`: `ok=true`, `version=10.88`, `logic_version=D+E/v10.88`.
- `/api/coins` returned 10 visible candidates sorted by final score descending.
- Existing A/B checks for volume percentage fairness, monotonic volatility, L1-L10 profit-floor backtest scoring, dense/centerline labels, and websocket redaction remain passing.

## Safety guard checks
Runtime write protections behaved as expected:
- DNS rebinding Host header blocked: HTTP 403.
- Mutating GET `/api/engine/plan` blocked: HTTP 405.
- GET refresh `/api/research/dense-width?refresh=1` blocked: HTTP 405.
- Cross-site POST blocked: HTTP 403.
- No-Origin / no-local POST blocked: HTTP 403.
- Real-mode switch attempt `/api/mode` blocked under safe/read-only/no-real-orders with local JSON POST: HTTP 423.
- Start automatic trading `/api/action` blocked under safe/read-only/no-real-orders with local JSON POST: HTTP 423.
- One-key close-all `/api/engine/close-all` with `confirm=CLOSE_ALL` blocked under safe/read-only/no-real-orders with local JSON POST: HTTP 423.

## Binance daily performance and dense-width research
- Virtual U-margined daily performance: `不可判定`; no complete closed rounds and no complete signed private Binance coverage in sandbox.
- Real U-margined daily performance: `不可判定`; no complete closed rounds and no complete signed private Binance coverage in sandbox.
- Recent 10-round wins and rolling 10-round 7-win/8-win ratios: `不可判定`; closed windows are not available in sandbox.
- Dense-width research: `不可判定`; no production one-year 4H histories/private evidence are available in sandbox.
- No leaderboard/backtest score was used as real trading win rate.

## Release artifact scan
- v10.88 release zip excludes `.binance_api_keys.json`, runtime cache/state files, `__pycache__`, `.pytest_cache`, `.pyc`, `.log`, and `.pid`.
- The known leaked credential strings from the incoming v10.87 candidate were not found in the v10.88 release zip.

## Formal live readiness
`/api/system/formal-live-readiness` still returned:
- `formal_live_ready=false`
- `ok=false`
- `must_not_claim_live_ready=true`
- blocking items: 9

Blocking items remain external/production evidence blockers, including Mac-local 5050 Playwright/browser E2E, production workdir evidence, fresh realtime sync evidence, 365-day/2190-bar 4H backtest evidence for all visible candidates, signed Binance reconciliation, complete safety evidence, and user-approved small-canary evidence.

## Conclusion
v10.88 fixes the release secret-hygiene vulnerability found in the uploaded v10.87 candidate and passes all executable sandbox tests. Auto Snowball still has **not** reached true-fund formal live standard. Do not switch to real trading and do not place real orders until the blocking items are cleared on the production Mac host.
