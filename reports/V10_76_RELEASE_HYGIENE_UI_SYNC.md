# V10.76 Release Hygiene UI Sync

Local package v10.76 was prepared from v10.75.

Fixes:
- Removed runtime cache and state files from the release package.
- Removed stale plus 80 USDC fallback text from the execution center profit guard summary.
- Added regression coverage for release hygiene and current 50 percent protection labels.

Validation:
- Non browser pytest group passed: 285 passed, 6 skipped.
- Browser group skipped in managed sandbox policy; local Mac browser evidence is still required.
- Formal live status remains blocked until all external evidence is complete.
