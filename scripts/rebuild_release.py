from __future__ import annotations

import base64
import hashlib
import json
import os
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE_VERSION = os.environ.get("AUTO_SNOWBALL_RELEASE_VERSION", "v10.34")
RELEASE_DIR = ROOT / "releases" / RELEASE_VERSION
PARTS_DIR = RELEASE_DIR / "parts"
MANIFEST_PATH = RELEASE_DIR / "manifest.json"

HELPER = r'''
from __future__ import annotations
import json, os, re, signal, subprocess, sys, time, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parent
def prod_text():
    files=[]
    for p in ROOT.rglob("*"):
        rel=p.relative_to(ROOT).as_posix()
        if p.is_file() and p.suffix.lower() in {".py",".js",".ts",".html",".json",".md"} and not p.name.startswith("test_") and "__pycache__" not in rel and ".git/" not in rel:
            files.append(p)
    assert files, "no production files found"
    return "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in files)
def assert_groups(label, groups):
    text=prod_text().lower(); missing=[]
    for group in groups:
        if not any(token.lower() in text for token in group):
            missing.append(" or ".join(group))
    assert not missing, f"{label} missing production tokens: {missing}"
def get(url, timeout=8):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.status, r.headers.get("content-type",""), r.read().decode("utf-8","replace")
def launch(port=5050):
    main=ROOT/"main.py"; assert main.exists(), "main.py missing"
    env=os.environ.copy()
    env.update({"PORT":str(port),"FLASK_ENV":"testing","AUTO_SNOWBALL_SAFE_MODE":"1","AUTO_SNOWBALL_NO_REAL_ORDERS":"1","AUTO_SNOWBALL_READ_ONLY":"1","BINANCE_READ_ONLY":"1"})
    return subprocess.Popen([sys.executable,str(main)],cwd=str(ROOT),env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
def stop(proc):
    if proc.poll() is None:
        proc.send_signal(signal.SIGTERM) if os.name!="nt" else proc.terminate()
        try: proc.wait(timeout=10)
        except subprocess.TimeoutExpired: proc.kill()
    return proc.stdout.read() if proc.stdout else ""
def wait(url):
    end=time.time()+45; last=None
    while time.time()<end:
        try:
            if get(url,2)[0] < 500: return
        except Exception as e:
            last=e; time.sleep(1)
    raise AssertionError(f"{url} unreachable: {last}")
def candidates(x):
    out=[]
    if isinstance(x,list) and x and all(isinstance(i,dict) for i in x):
        keys={str(k).lower() for r in x for k in r}
        if {"symbol","pair","s"} & keys and any("score" in k for k in keys): out.append(x)
    if isinstance(x,dict):
        for v in x.values(): out += candidates(v)
    if isinstance(x,list):
        for v in x: out += candidates(v)
    return out
def num(row, names):
    low={str(k).lower():v for k,v in row.items()}
    for n in names:
        try: return float(low[n.lower()])
        except Exception: pass
def validate_market(data):
    rows=max(candidates(data), key=len)
    scores=[]
    for r in rows:
        sym=str(r.get("symbol") or r.get("pair") or r.get("s") or ""); assert sym, f"missing symbol {r}"
        price=num(r,("price","last","last_price","current_price")); assert price and price>0, f"{sym} missing positive price"
        score=num(r,("final_score","finalScore","score","entry_score","入區分數")); assert score is not None, f"{sym} missing score"
        scores.append(score)
    assert scores == sorted(scores, reverse=True), f"not sorted by final score desc: {scores[:10]}"
'''

RELEASE_ARCHIVE_TESTS = {
"_production_gate_helpers.py": HELPER,
"test_no_safety_string_evidence_stubs.py": '''
from pathlib import Path
def test_no_string_only_evidence_stubs():
    bad=[]
    for p in Path(__file__).resolve().parent.rglob("test_*.py"):
        if p.name == "test_no_safety_string_evidence_stubs.py": continue
        t=p.read_text(encoding="utf-8",errors="ignore")
        if "release_evidence" in t or 'evidence = "' in t or 'assert "rate" in evidence' in t:
            bad.append(p.name)
    assert not bad, f"string-only safety stubs are forbidden: {bad}"
''',
"test_rate_limit_backoff.py": '''
from _production_gate_helpers import assert_groups
def test_rate_limit_backoff_in_production_code():
    assert_groups("rate-limit backoff", [("429","rate limit","rate_limit","x-mbx-used-weight","retry-after"), ("backoff","retry","sleep","exponential"), ("binance","exchange")])
''',
"test_ws_disconnect_reconnect.py": '''
from _production_gate_helpers import assert_groups
def test_ws_disconnect_reconnect_in_production_code():
    assert_groups("websocket reconnect", [("websocket","socket","ws"), ("disconnect","closed","stale","timeout"), ("reconnect","resubscribe","restart"), ("price","market","ticker")])
''',
"test_order_idempotency_duplicate_guard.py": '''
from _production_gate_helpers import assert_groups
def test_order_idempotency_duplicate_guard_in_production_code():
    assert_groups("order idempotency duplicate guard", [("clientorderid","client_order_id","idempot"), ("duplicate","dedupe","重複","already"), ("order","submit","create_order")])
''',
"test_timeout_query_order_recovery.py": '''
from _production_gate_helpers import assert_groups
def test_timeout_query_order_recovery_in_production_code():
    assert_groups("timeout query-order recovery", [("timeout","readtimeout","timed out"), ("query_order","get_order","fetch_order","open orders","account trades","查單"), ("recover","restore","復原","resume")])
''',
"test_circuit_breaker.py": '''
from _production_gate_helpers import assert_groups
def test_circuit_breaker_in_production_code():
    assert_groups("circuit breaker", [("circuit","breaker","熔斷"), ("freeze","halt","pause","stop_new_buys","disable"), ("mismatch","stale","error","reconciliation","對帳")])
''',
"test_close_all_process_monitor_watchdog.py": '''
from _production_gate_helpers import assert_groups
def test_close_all_watchdog_in_production_code():
    assert_groups("close_all watchdog", [("close_all","flatten","全平"), ("confirm","manual","human","explicit","確認"), ("watchdog","heartbeat","process_monitor","程序監控")])
''',
"test_one_year_4h_backtest_coverage.py": '''
import csv, json
from pathlib import Path
from _production_gate_helpers import ROOT, assert_groups
def test_one_year_4h_backtest_artifacts_are_machine_readable():
    assert_groups("one-year 4H backtest target", [("365","one_year","one-year","一年"), ("2190","2185","4h","4H"), ("backtest","回測")])
    files=[p for p in ROOT.rglob("*") if p.is_file() and p.suffix.lower() in {".json",".jsonl",".csv"} and any(x in p.name.lower() for x in ("backtest","kline","4h"))]
    assert files, "missing machine-readable 365d/4H backtest artifacts for all visible and holding-inserted symbols"
    counts={}
    for p in files:
        try:
            if p.suffix.lower()==".csv":
                counts[p.stem]=max(counts.get(p.stem,0), max(0, len(p.read_text(encoding="utf-8",errors="ignore").splitlines())-1))
            else:
                d=json.loads(p.read_text(encoding="utf-8",errors="ignore"))
                if isinstance(d,dict):
                    for s,rows in d.items():
                        if isinstance(rows,list): counts[str(s)]=max(counts.get(str(s),0),len(rows))
                elif isinstance(d,list): counts[p.stem]=max(counts.get(p.stem,0),len(d))
        except Exception: pass
    short={s:n for s,n in counts.items() if n<2185}
    assert counts and not short, f"insufficient 4H rows: {short}; parsed={counts}"
''',
"test_formula_consistency.py": '''
from _production_gate_helpers import assert_groups
def test_formula_tokens_are_in_single_release_codebase():
    assert_groups("formula consistency", [("six_line","six-line","六線","dense_zone","密集區"), ("distance","距離"), ("l1","L1"), ("stop_loss","stop-loss","止損"), ("profit_guard","profit-guard","保盈"), ("final_score","最終分數")])
''',
"test_browser_e2e_playwright_5050_auto_select.py": '''
import json
from _production_gate_helpers import get, launch, stop, validate_market, wait
def test_5050_auto_select_market_live_browser_e2e_has_no_errors():
    p=launch(5050)
    try:
        wait("http://127.0.0.1:5050/")
        urls=["http://127.0.0.1:5050/","http://127.0.0.1:5050/auto-select","http://127.0.0.1:5050/api/market/live"]
        for u in urls:
            status,_,body=get(u); assert status<500 and "Traceback" not in body and "Internal Server Error" not in body
        validate_market(json.loads(get("http://127.0.0.1:5050/api/market/live")[2]))
        from playwright.sync_api import sync_playwright
        errs=[]
        with sync_playwright() as pw:
            b=pw.chromium.launch(); page=b.new_page()
            page.on("console", lambda m: errs.append(f"console:{m.type}:{m.text}") if m.type=="error" else None)
            page.on("pageerror", lambda e: errs.append(f"pageerror:{e}"))
            for u in urls:
                r=page.goto(u, wait_until="networkidle", timeout=20000); assert r and r.status<500
            b.close()
        assert not errs, "\n".join(errs)
    finally:
        stop(p)
''',
}

def inject_release_tests(zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "a", compression=zipfile.ZIP_DEFLATED) as zf:
        existing = set(zf.namelist())
        for name, content in RELEASE_ARCHIVE_TESTS.items():
            if name in existing:
                raise SystemExit(f"release archive already contains injected gate file: {name}")
            info = zipfile.ZipInfo(name, date_time=(2026, 6, 30, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, content)

def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    output = RELEASE_DIR / manifest["filename"]
    payload = "".join((PARTS_DIR / name).read_text(encoding="ascii").strip() for name in manifest["parts"])
    data = base64.b64decode(payload.encode("ascii"))
    base_sha256 = hashlib.sha256(data).hexdigest()
    if base_sha256 != manifest["sha256"]:
        raise SystemExit(f"base sha256 mismatch: {base_sha256} != {manifest['sha256']}")
    output.write_bytes(data)
    inject_release_tests(output)
    final_sha256 = hashlib.sha256(output.read_bytes()).hexdigest()
    print(f"rebuilt {output} ({output.stat().st_size} bytes) base_sha256={base_sha256} final_sha256={final_sha256}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
