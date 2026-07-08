# Auto Snowball v10.83 Formal Live Gate Re-run — 2026-07-08 18:46 TPE

## Scope
- Package inspected: `auto_snowball_web_v10_83_volume_percentage_fairness_e2e.zip`.
- SHA256 verified: `440792491d890fd93590f4de0d8e06aa716c4969141c5f08d3f0e7f945120e3f`.
- Runtime tested from sandbox directory: `/mnt/data/audit_v10_83_run/auto_snowball_web_v10_83_volume_percentage_fairness_e2e`.
- Requested Mac production workdir could not be accessed from this sandbox: `/Users/andyna/Documents/自動滾倉系統設計`.
- Safety flags used: `AUTO_SNOWBALL_SAFE_MODE=1`, `AUTO_SNOWBALL_NO_REAL_ORDERS=1`, `AUTO_SNOWBALL_READ_ONLY=1`, `BINANCE_READ_ONLY=1`.
- No real orders were placed. No real trading mode was enabled.

## Vulnerability check
- No new code vulnerability was found in this re-run.
- No code change was required.
- No v10.84 package was produced.
- v10.83 volume percentage fairness formula remains active in the formula-audit contract.

## Pytest / E2E status
- Full pytest: `297 passed, 13 skipped`.
- Skipped tests are sandbox/browser/Mac-local evidence checks and cannot be counted as formal production browser E2E pass.

## 5050 runtime smoke
A fresh 5050 runtime was started from the inspected v10.83 package. The following returned HTTP 200 without Traceback/Internal Server Error text:
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

## Ranking / formula verification
- `/api/coins` returned 10 visible candidates sorted by final `score` descending.
- Score order was: BTCUSDC 68.50, ETHUSDC 67.47, ADAUSDC 54.20, SOLUSDC 52.98, AVAXUSDC 52.67, XRPUSDC 51.42, BNBUSDC 51.11, LINKUSDC 36.74, DOGEUSDC 32.85, TIAUSDC 19.32.
- `/api/system/formula-audit`: `ok=true`, `version=10.83`, `logic_version=D+E/v10.83`.
- Formula audit exposes `ranking_score.volume_score.config.basis = percentage_fairness`.
- A/B checks include `volume_score_basis` and `volume_score_component_weights`; both passed.
- Current `/api/coins` source summary is sandbox system-estimate fallback because Binance DNS/WebSocket/private keys are unavailable in this environment; production live values must be verified on the Mac host.

## Safety guard checks
Runtime write protections behaved as expected:
- DNS rebinding Host header blocked: HTTP 403.
- Mutating GET `/api/engine/plan` blocked: HTTP 405.
- GET refresh `/api/research/dense-width?refresh=1` blocked: HTTP 405.
- Cross-site POST blocked: HTTP 403.
- No-Origin / no-local POST blocked: HTTP 403.
- Real-mode switch attempt `/api/mode` blocked under safe/read-only/no-real-orders: HTTP 423.
- Start automatic trading `/api/action` blocked under safe/read-only/no-real-orders: HTTP 423.
- One-key close-all `/api/engine/close-all` with `confirm=CLOSE_ALL` blocked under safe/read-only/no-real-orders: HTTP 423.

## Binance daily performance and dense-width research
- Virtual U-margined daily performance: `不可判定`; no complete closed rounds and no complete signed private Binance coverage in sandbox.
- Real U-margined daily performance: `不可判定`; no complete closed rounds and no complete signed private Binance coverage in sandbox.
- Recent 10-round wins and rolling 10-round 7-win/8-win ratios: `不可判定`; closed windows = 0.
- Dense-width research: `不可判定`; read-only true; no candidate width because complete one-year 4H histories/private production evidence are not available in sandbox.
- No leaderboard/backtest score was used as real trading win rate.

## Formal live readiness
`/api/system/formal-live-readiness` returned:
- `formal_live_ready=false`
- `ok=false`
- `must_not_claim_live_ready=true`
- blocking items: 9

Blocking items:
1. Need Mac local 5050 Playwright/browser E2E evidence with matching version/workdir/time.
2. Need evidence that audit workdir is `/Users/andyna/Documents/自動滾倉系統設計`.
3. Need fresh realtime prices, entry-zone status/score/ranking sync E2E evidence.
4. Need all visible candidate coins to have 365-day/about 2190 4H K-line backtest evidence.
5. Need signed Binance reconciliation clean evidence.
6. Need complete safety test evidence for rate-limit backoff, disconnect/reconnect, order idempotency, timeout query-order recovery, duplicate order guard, circuit breaker, close-all, and process monitor.
7. Need latest-version full pytest evidence accepted by the formal gate.
8. Need Mac local browser E2E all-pass evidence; sandbox skipped E2E is not sufficient.
9. Need formal preflight plus user-approved small-canary evidence.

## Conclusion
v10.83 passed executable sandbox pytest and 5050/API/safety smoke checks, and no new vulnerability was found. Auto Snowball still has **not** reached true-fund formal live standard. Do not switch to real trading and do not place real orders until the blocking items are cleared on the production Mac host.
