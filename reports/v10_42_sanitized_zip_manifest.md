# V10.42 Sanitized Zip Manifest

## Status

**SYNCHRONIZED TO MAIN FOR REVIEW / TRACKING ONLY.**

This manifest records the user-uploaded sanitized V10.42 package received at `2026-07-01T00:01:07+08:00`. It is not a launch approval and does not enable live capital.

## File Identity

- Uploaded file: `auto_snowball_web_v10_42_launch_gate_evidence_sanitized.zip`
- Bytes: `234565`
- SHA256: `4c06e28067bf127f33344f6e735dc9d379a59fde84d5bdd249ea297839ac87f2`
- ZIP entries: `108`

## Content Summary

| Type | Count |
|---|---:|
| Python | 72 |
| Markdown | 20 |
| HTML | 10 |
| Text | 2 |
| CSS | 1 |
| JS | 1 |
| SVG | 1 |
| Other/no extension | 1 |

## Safety Scan

- Common local credential/runtime/cache filename scan: `PASS`
- Binary artifact was not committed directly through this sync.
- This repository update records only manifest evidence.

## Package Evidence Summary

The sanitized package contains V10.42 evidence text reporting:

- Targeted reconciliation and shared-ranking tests: `8 passed`.
- Browser regression: `1 passed`.
- Full suite against isolated read-only runtime: `191 passed in 42.57s`.
- Final clean extracted archive rerun: `191 passed in 40.54s`.
- No real order submitted and no real trading mode enabled.

## Current Launch Decision

`formal_launch = false`

Reason: GitHub Actions release gate still fails at the executable production safety test placement gate. A passing workflow run is still required before any live-capital release.
