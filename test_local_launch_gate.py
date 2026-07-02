from scripts import local_launch_gate
from scripts import local_launch_gate_5050_binance as gate_5050
from scripts import rebuild_release


def market_payload():
    return {
        "coins": [
            {
                "symbol": "BTCUSDC",
                "rank": 1,
                "score": 90,
                "price": 100,
                "dense_zone_arrival_status": "尚未進入",
                "zone_entry_score": 3,
                "backtest_kline_bars": 2190,
                "backtest_lookback_days": 365,
                "backtest_kline_interval": "4h",
            },
            {
                "symbol": "ETHUSDC",
                "rank": 2,
                "score": 80,
                "price": 50,
                "dense_zone_arrival_status": "已進入",
                "zone_entry_score": 18,
                "backtest_kline_bars": 2190,
                "backtest_lookback_days": 365,
                "backtest_kline_interval": "4h",
            },
        ]
    }


def test_market_validator_accepts_runtime_field_names_and_score_fallback():
    ok, detail = local_launch_gate.validate_market(market_payload())
    assert ok, detail


def test_formal_preflight_uses_longer_runtime_timeout():
    assert local_launch_gate.runtime_endpoint_timeout("/api/system/runtime") == 12.0
    assert local_launch_gate.runtime_endpoint_timeout("/api/system/launch-preflight") == 30.0


def test_market_validator_rejects_rank_drift():
    payload = market_payload()
    payload["coins"][1]["rank"] = 3
    ok, detail = local_launch_gate.validate_market(payload)
    assert not ok
    assert "expected 2" in detail


def test_ci_market_validator_defers_backtest_to_bundled_artifact():
    payload = market_payload()
    for row in payload["coins"]:
        row.pop("backtest_kline_bars")
        row.pop("backtest_lookback_days")
        row.pop("backtest_kline_interval")
    ok, detail = local_launch_gate.validate_market(payload, require_backtest=False)
    assert ok, detail


def test_ci_backtest_artifact_must_cover_every_visible_symbol(tmp_path):
    evidence = {
        "checks": [
            {"symbol": "BTCUSDC", "bars": 2190, "lookback_days": 365, "interval": "4h", "ok": True},
            {"symbol": "ETHUSDC", "bars": 2190, "lookback_days": 365, "interval": "4h", "ok": True},
        ]
    }
    (tmp_path / "backtest_evidence_v10_43.json").write_text(__import__("json").dumps(evidence), encoding="utf-8")
    ok, detail = local_launch_gate.validate_backtest_artifact(tmp_path, market_payload())
    assert ok, detail

    evidence["checks"].pop()
    (tmp_path / "backtest_evidence_v10_43.json").write_text(__import__("json").dumps(evidence), encoding="utf-8")
    ok, detail = local_launch_gate.validate_backtest_artifact(tmp_path, market_payload())
    assert not ok
    assert "ETHUSDC" in detail


def test_market_refresh_accepts_new_timestamp_with_synchronized_rows():
    before = market_payload()
    before["updated_at"] = "2026-06-30 23:00:00"
    after = market_payload()
    after["updated_at"] = "2026-06-30 23:00:01"
    ok, detail = local_launch_gate.validate_market_refresh(before, after)
    assert ok, detail


def test_5050_gate_uses_usds_m_futures_klines():
    assert gate_5050.BINANCE_FUTURES_KLINES == "https://fapi.binance.com/fapi/v1/klines"


def test_5050_gate_visible_symbols_ignore_websocket_metadata():
    payload = market_payload()
    payload["websocket_status"] = {
        "symbols": ["BTCUSDC", "ETHUSDC", "ZECUSDC"],
        "kline_symbols": ["ZECUSDC"],
    }
    rows = max(gate_5050.find_row_lists(payload), key=len)
    assert gate_5050.find_symbols(rows) == ["BTCUSDC", "ETHUSDC"]


def test_formula_audit_validates_runtime_formula_payload(monkeypatch):
    monkeypatch.setattr(
        gate_5050,
        "get_json",
        lambda _url, timeout=8: {
            "ok": True,
            "checks": [{"ok": True}],
            "a_to_b_sync": {
                "ok": True,
                "checks": [
                    {"field": "dense_zone_half_pct", "a_value": 1.0, "b_value": 1.0, "ok": True},
                    {"field": "dense_zone_max_width_pct", "a_value": 2.0, "b_value": 2.0, "ok": True},
                ],
            },
            "formula": {
                "dense_zone": {"half_width_pct": 1.0, "total_width_pct": 2.0},
                "profit_guard": {
                    "first_trigger_pct": 20,
                    "first_floor_pct": 16,
                    "first_trigger_usdc": 20,
                    "first_floor_usdc": 16,
                    "protection_ratio": 80,
                },
                "stop_loss": {"default_pct": 10},
            },
        },
    )
    failures = []
    gate_5050.check_formula_audit("http://127.0.0.1:5050", failures)
    assert failures == []


def test_formula_audit_rejects_floor_not_derived_from_trigger(monkeypatch):
    monkeypatch.setattr(
        gate_5050,
        "get_json",
        lambda _url, timeout=8: {
            "ok": True,
            "checks": [{"ok": True}],
            "a_to_b_sync": {"ok": True, "checks": [{"ok": True}]},
            "formula": {
                "dense_zone": {"half_width_pct": 1.0, "total_width_pct": 2.0},
                "profit_guard": {
                    "first_trigger_pct": 20,
                    "first_floor_pct": 24,
                    "protection_ratio": 80,
                },
                "stop_loss": {"default_pct": 10},
            },
        },
    )
    failures = []
    gate_5050.check_formula_audit("http://127.0.0.1:5050", failures)
    assert any("L1 floor formula mismatch" in item for item in failures)


def test_formula_audit_rejects_dense_total_width_drift(monkeypatch):
    monkeypatch.setattr(
        gate_5050,
        "get_json",
        lambda _url, timeout=8: {
            "ok": True,
            "checks": [{"ok": True}],
            "a_to_b_sync": {"ok": True, "checks": [{"ok": True}]},
            "formula": {
                "dense_zone": {"half_width_pct": 1.0, "total_width_pct": 3.0},
                "profit_guard": {
                    "first_trigger_pct": 20,
                    "first_floor_pct": 16,
                    "protection_ratio": 80,
                },
                "stop_loss": {"default_pct": 10},
            },
        },
    )
    failures = []
    gate_5050.check_formula_audit("http://127.0.0.1:5050", failures)
    assert any("dense total-width formula mismatch" in item for item in failures)


def test_launch_preflight_surfaces_manual_blockers(monkeypatch):
    monkeypatch.setattr(
        gate_5050,
        "get_json",
        lambda _url, timeout=8: {
            "ok": False,
            "blocking_items": [
                {"item": "正式 API 金鑰已設定", "ok": False},
                {"item": "小額灰度需手動確認", "ok": False},
            ],
        },
    )
    failures = []
    gate_5050.check_launch_preflight("http://127.0.0.1:5050", failures)
    assert failures == ["formal launch preflight blocked: 正式 API 金鑰已設定, 小額灰度需手動確認"]


def test_reconciliation_checks_status_objects_and_derivable_leverage(monkeypatch):
    payload = {
        "diagnostics": {"account_ok": True, "balance_ok": True, "orders_ok": True},
        "symbols": [
            {
                "symbol": "1000BONKUSDC",
                "endpoint_status": {"orders": {"ok": True, "error": None}},
                "position": {
                    "positionAmt": "-100000",
                    "entryPrice": "0.0042",
                    "breakEvenPrice": "0.0042",
                    "markPrice": "0.0041",
                    "unRealizedProfit": "10",
                    "liquidationPrice": "0.1",
                    "notional": "-410",
                    "initialMargin": "16.4",
                    "leverage": None,
                },
            }
        ],
    }
    monkeypatch.setattr(gate_5050, "get_json", lambda _url, timeout=5: payload)
    failures = []
    gate_5050.check_reconciliation("http://127.0.0.1:5050", failures)
    assert failures == []


def test_browser_gate_avoids_networkidle_wait():
    source = local_launch_gate.run_playwright.__code__.co_consts
    assert "networkidle" not in source
    assert 30000 in source


def test_ci_browser_gate_does_not_repeat_market_api_navigation():
    source = __import__("inspect").getsource(local_launch_gate.main)
    assert "run_playwright(urls[:2])" in source


def test_injected_release_gate_files_compile():
    for name, content in rebuild_release.RELEASE_ARCHIVE_TESTS.items():
        if name.endswith(".py"):
            compile(content, name, "exec")
