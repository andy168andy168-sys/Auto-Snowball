# V10.49 browser gate overlay

Copy `test_v148_browser_playwright_5050_auto_select.py.overlay` into the V10.48 runtime test suite as `test_v148_browser_playwright_5050_auto_select.py`.

The `.overlay` suffix prevents root-level pytest from collecting this runtime-specific test before it is installed. This is a test/tooling overlay only: it keeps the application version at V10.48, uses a 30-second `load` navigation timeout, waits briefly after load, and avoids starting a second server when port 5050 is already listening.
