# V10.52 — Launch-gate runner hardening

- Added repository-level `pytest.ini` so root pytest runs only the maintained gate tests and ignores archived/extracted release workspaces that contain duplicate test module names.
- Hardened `scripts/local_launch_gate.py` so missing Playwright browser binaries return a structured failing check instead of aborting the whole launch-gate report.
- Hardened the 5050 listener check to use `lsof`, `ss`, or `netstat` when available and to fail closed when no listener is detected instead of treating a missing `lsof` binary as a pass.
- No trading formulas, risk parameters, order submission logic, account mode switching, or Binance write behavior were changed.
