# CHANGELOG v10.97 — Runtime State Isolation and Cache Provenance

## Vulnerabilities fixed
- 修復 release zip 誤帶 `.market_sync_cache.json`、`.roll_engine_state.json` 後，乾淨部署會直接載入舊排行榜、舊持倉/武裝計劃的問題。
- 修復版本內舊 `.roll_engine_state.json` 可能因時間較新而覆蓋版本外共享狀態的回滾/污染風險。
- 修復 virtual 行情快取切換到 real 模式後仍可能被排行榜/執行選幣使用的資料路徑污染。
- 修復 virtual / real 共用同一份滾倉計劃快照，可能把 ARMED_L1、stage/orderId 帶到另一帳戶模式的風險。
- 修復自動交易執行中仍可切換帳戶模式的競態風險；現在必須先暫停。
- 修復正式上線 evidence 放在 release root、可能被封裝攜帶的證據來源風險。

## Runtime state isolation
- 以下可變資料預設全部移到版本外私有目錄：
  - `.binance_api_keys.json`
  - `.market_sync_cache.json`
  - `.audit_truth_cache.json`
  - `.roll_engine_state.json`
  - `.roll_engine_parameters.json`
  - `formal_live_evidence.json`
- 預設目錄：`$XDG_STATE_HOME/auto-snowball`；未設定 XDG 時使用 `~/.local/state/auto-snowball`。
- 可用 `AUTO_SNOWBALL_STATE_HOME` 或各檔案專用環境變數覆寫。
- release root 的舊 runtime 檔預設完全忽略；只有操作員明確設定 `AUTO_SNOWBALL_IMPORT_LEGACY_RUNTIME=1` 才會一次性導入到版本外狀態檔。
- JSON 寫入改為唯一暫存檔 + flush/fsync + atomic replace，檔案權限 0600、父目錄 0700。

## A/B and mode isolation
- virtual / real 行情快取按 mode 隔離；模式不符時回傳空候選與 `mode_mismatch=true`，等待該模式重新同步。
- 排行榜、WebSocket 訂閱、實時頁、執行計劃市場資料路徑同步使用同一個 mode-aware cache helper。
- 滾倉狀態改為 `.roll_engine_state.virtual.json` / `.roll_engine_state.real.json` 分離；舊版外部單檔只會在其內嵌 mode 相符時遷移。
- 模式切換會先保存來源模式、停止舊模式 WebSocket、清空記憶體計劃，再只載入目標模式狀態。

## Unchanged
- 中線觸及 → ARMED_L1 → 後續突破密集區才開 L1 的交易規則不改。
- ARMED_L1 排名輪替保留規則不改。
- 密集區、成交量、波動、回測分、L1-L10、止損、保盈與排行榜權重不改。
- 未切換真實模式，未下真實訂單。
