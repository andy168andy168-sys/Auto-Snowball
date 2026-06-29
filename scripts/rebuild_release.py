from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE_DIR = ROOT / 'releases' / 'v10.34'
PARTS_DIR = RELEASE_DIR / 'parts'
MANIFEST_PATH = RELEASE_DIR / 'manifest.json'


def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))
    output = RELEASE_DIR / manifest['filename']
    payload = ''.join((PARTS_DIR / name).read_text(encoding='ascii').strip() for name in manifest['parts'])
    data = base64.b64decode(payload.encode('ascii'))
    sha256 = hashlib.sha256(data).hexdigest()
    if sha256 != manifest['sha256']:
        raise SystemExit(f"sha256 mismatch: {sha256} != {manifest['sha256']}")
    output.write_bytes(data)
    print(f"rebuilt {output} ({len(data)} bytes) sha256={sha256}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
