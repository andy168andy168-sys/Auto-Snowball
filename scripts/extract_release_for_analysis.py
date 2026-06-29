#!/usr/bin/env python3
"""
提取 release 包用於分析，生成完整項目結構清單
"""
from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE_DIR = ROOT / 'releases' / 'v10.34'
ZIP_PATH = RELEASE_DIR / 'auto_snowball_web_v10_34_overview_auto_select_sync_e2e.zip'
EXTRACT_DIR = ROOT / '_temp_extract_analysis'


def main() -> int:
    if not ZIP_PATH.exists():
        print(f"ERROR: {ZIP_PATH} not found. Run rebuild_release.py first.")
        return 1
    
    EXTRACT_DIR.mkdir(exist_ok=True)
    
    print(f"📦 Extracting {ZIP_PATH}...")
    with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
        zf.extractall(EXTRACT_DIR)
    
    # 分析結構
    structure = []
    for path in sorted(EXTRACT_DIR.rglob('*')):
        if path.is_file():
            rel = path.relative_to(EXTRACT_DIR)
            size = path.stat().st_size
            structure.append(f"{rel} ({size} bytes)")
    
    print("\n📂 Project Structure:")
    for item in structure[:50]:  # 前 50 項
        print(f"  {item}")
    
    if len(structure) > 50:
        print(f"  ... and {len(structure) - 50} more files")
    
    # 檢查關鍵目錄
    dirs_to_check = [
        'tests', 'test', 'tests_e2e', 'conftest.py',
        'main.py', 'app.py', 'requirements.txt'
    ]
    
    print("\n🔍 Key Components Check:")
    for item in dirs_to_check:
        path = EXTRACT_DIR / item
        if path.exists():
            print(f"  ✅ {item}")
        else:
            print(f"  ❌ {item} (MISSING)")
    
    print(f"\n✅ Extracted to: {EXTRACT_DIR}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
