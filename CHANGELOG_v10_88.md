# CHANGELOG v10.88 — Release Secret Hygiene Hardening

## Changed
- 修復 v10.87 候選 zip 封裝漏洞：release zip 不得包含本機 `.binance_api_keys.json`。
- 同步移除 release 內所有 `__pycache__`、`.pytest_cache`、`.pyc`、`.log`、`.pid` 及 runtime/cache/state 檔案。
- 新增 `.binance_api_keys.example.json`，只保留安全 placeholder，方便本機部署後自行建立真正金鑰檔。
- 新增 `test_v188_release_secret_hygiene.py`，直接掃描 release tree，防止本機 key/cache/state/cache bytecode 再被打包。
- WebSocket listen-key redaction、密集區 cache symbol-set 穩定性、v10.87 L1-L10 保盈回測分、v10.86 波動單調分全部保留。

## Unchanged
- 入場公式不改。
- 密集區公式不改。
- 成交量分不改。
- 波動分不改。
- 回測分不改。
- L1-L10 階梯不改。
- 止損 / 保盈公式不改。
- 最終排行榜權重不改。
- 真實模式守門、read-only/safe/no-real-orders 防護不改。

## Safety
- 未自動重啟交易。
- 未切換真實模式。
- 未下真實訂單。
