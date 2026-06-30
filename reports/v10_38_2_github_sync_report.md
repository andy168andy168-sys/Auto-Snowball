# v10.38(2) GitHub Sync Gate Report

## Status

**NOT READY FOR LIVE CAPITAL.**

This report syncs the sanitized v10.38(2) package and the current launch-gate findings to GitHub. It does not approve live trading.

## Package

- Source upload: `auto_snowball_web_v10_38_l1_guard_40_e2e(2).zip`
- GitHub sync artifact: `auto_snowball_web_v10_38_l1_guard_40_e2e_2_github_sync.zip`
- SHA256: `eb0efe764272204db57fe85bce98f4c6ca9c0cbadd69aee35c1fffd21821d765`
- Original upload contained `local credential file`: `True`
- Sanitized artifact removed `local credential file`: `True`

## Sandbox Findings

| Check | Result |
|---|---|
| Full pytest | TIMEOUT after 240s; not acceptable as full pass |
| Non-browser pytest | most non-browser tests passed before timeout; cannot claim full suite passed |
| Playwright | Chromium localhost blocked by sandbox policy; Mac LOCAL_LAUNCH_GATE required |
| 5050 HTTP smoke | PASS in sandbox after removing local credential file |
| `/api/market/live` score sorting | PASS observed through /api/market/live |
| 365d / 2190 4H backtest evidence | PASS observed: API reports visible candidates with 365 days / 2190 4H bars |
| Formula audit | PASS observed through /api/system/formula-audit |
| Binance signed reconciliation | BLOCKED: no signed account/order/trade/fee evidence |

## GitHub Commit a6fa6dee

- Report status: `Not ready for live capital yet`
- Workflow runs: `none found`
- Combined status: `empty`

Remaining blockers reported by a6fa6dee:

- real Binance API key intentionally not configured
- small-size gray release / canary requires manual approval

## Required Before Live Capital

1. Rotate or disable any Binance API key that was present in the original uploaded zip.
2. Run LOCAL_LAUNCH_GATE on the real Mac workdir `/Users/andyna/Documents/自動滾倉系統設計`.
3. Capture passing Mac Playwright browser E2E evidence.
4. Capture signed Binance account/order/trade/fee reconciliation evidence.
5. Complete manual small-size gray release / canary approval.
6. Get a successful GitHub Actions workflow run for the exact release commit.

## Safety

- No real order was submitted.
- No real trading mode switch was performed.
- This synced package is a sanitized artifact for review and tracking only.
