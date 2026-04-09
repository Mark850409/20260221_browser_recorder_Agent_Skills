# 瀏覽器錄製器 Agent Skills（20260221_browser_recorder_Agent_Skills）

以 **Chrome DevTools 偵錯連線** 驅動瀏覽器操作，於過程中**截圖記錄步驟**，並產出可重複執行的 **Python 巨集腳本**的專案／技能素材庫。

Agent 端依 [`SKILL.md`](SKILL.md) 使用 **chrome-devtools MCP** 導覽、點擊、填表與截圖；**最終交付物**為 `macros/` 內的 Python 腳本（非僅截圖拼貼）。

---

## 核心產出規範

| 項目 | 說明 |
|------|------|
| **巨集腳本** | 必須在 **`macros/`** 目錄產出 `{名稱}.py`，重現完整操作流程。 |
| **截圖** | 強制路徑：**`screenshots/{task_name}/`**，檔名建議 `01_`、`02_` 前綴依序編號。 |
| **禁止** | 除非使用者明確要求，**不要**產出 GIF、影片或其他媒體轉檔；「錄製」＝產出可執行程式碼。 |

詳細流程與 MCP 操作範例見 [`SKILL.md`](SKILL.md)、[`references/recording_workflow.md`](references/recording_workflow.md)。

---

## 環境與前置作業

- **Google Chrome**（預設路徑見 `scripts/start_chrome_debug.bat`，可依環境修改）。  
- **Windows**：透過 `scripts/start_chrome_debug.bat` 以 **9222** 埠啟動遠端偵錯，並使用獨立 **`chrome_profile`**，不影響日常使用的 Chrome。  
- 巨集腳本會先檢查偵錯埠是否可用，必要時自動呼叫上述批次檔。

**Python 依賴**（本機執行巨集時）：

```bash
pip install -r requirements.txt
```

`requirements.txt` 內含 `selenium`、`webdriver-manager`、`requests`、`websocket-client` 等；實際巨集可能以 **Chrome DevTools Protocol（HTTP／WebSocket）** 實作，請以各腳本為準。

---

## 目錄結構（摘要）

```
20260221_browser_recorder_Agent_Skills/
├── README.md
├── SKILL.md                          # 技能主規格（觸發條件、流程、禁止事項）
├── requirements.txt
├── macros/                           # 可重複執行的 Python 巨集（核心產出）
├── scripts/
│   ├── start_chrome_debug.bat        # 啟動 Chrome 偵錯模式
│   ├── template_browser_task.py
│   ├── test_automation.py
│   └── utils/
├── references/
│   ├── chrome_devtools_tools.md      # MCP 工具與參數
│   └── recording_workflow.md         # 錄製模式、截圖命名、範例
└── screenshots/                      # 執行巨集時依 task 名稱分子目錄（執行後產生）
```

`SKILL.md` 中若出現泛用路徑 `browser-recorder/`，對應本儲存庫根目錄下的上述結構。

---

## 參考文件

| 檔案 | 用途 |
|------|------|
| [`SKILL.md`](SKILL.md) | 前置作業、錄製流程、常見 MCP 操作片段 |
| [`references/chrome_devtools_tools.md`](references/chrome_devtools_tools.md) | DevTools MCP 工具清單與參數 |
| [`references/recording_workflow.md`](references/recording_workflow.md) | 標準錄製步驟、截圖規則、疑難排解 |

---

## 何時啟用此技能

例如：開啟網站、導覽、搜尋、點擊、填表；「錄製」或「記錄」瀏覽器操作；需要可重複執行的 Python 自動化腳本。完整觸發語句見 [`SKILL.md`](SKILL.md) 的 frontmatter `description`。

---

## 授權與貢獻

若本專案隸屬於上層儲存庫，請依該儲存庫的授權與貢獻指南為準。
