from scripts import local_launch_gate
from scripts import local_launch_gate_5050_binance as gate_5050


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


def test_market_validator_rejects_rank_drift():
    payload = market_payload()
    payload["coins"][1]["rank"] = 3
    ok, detail = local_launch_gate.validate_market(payload)
    assert not ok
    assert "expected 2" in detail


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
        lambda _url: {
            "ok": True,
            "checks": [{"ok": True}],
            "formula": {
                "dense_zone": {"half_width_pct": 1.5},
                "profit_guard": {
                    "first_trigger_pct": 30,
                    "first_floor_pct": 24,
                    "protection_ratio": 80,
                },
                "stop_loss": {"default_pct": 10},
            },
        },
    )
    failures = []
    gate_5050.check_formula_audit("http://127.0.0.1:5050", failures)
    assert failures == []


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
