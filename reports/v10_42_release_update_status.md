# V10.42 Release Update Status

## Completed

- Removed the tracked `releases/v10.34` manifest and part files from `main`.
- Updated GitHub Actions release CI to target `v10.42` paths.
- Updated `scripts/rebuild_release.py` default release version to `v10.42`.
- Added `releases/v10.42/manifest.json` for the flattened sanitized V10.42 release archive.
- Updated README from the old v10.34 release target to v10.42.

## Current release identity

- Release archive filename: `auto_snowball_web_v10_42_release_flat.zip`
- Bytes: `222469`
- SHA256: `f8371c1c485e7dd672dcec7a0d8c36ab0aa600bff4dbe1895dbf37bdca23e7c3`
- Base64 length: `296628`
- Part count expected by manifest: `6`

## Remaining blocker

The V10.42 base64 part files listed by `releases/v10.42/manifest.json` must be committed before GitHub Actions can rebuild the release ZIP. Until those part files are present and CI passes, formal launch remains disabled.

## Safety

- This update does not approve live capital.
- This update does not enable real trading.
