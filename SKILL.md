---
name: browser-recorder
description: |
  使用 chrome-devtools MCP 控制瀏覽器，並透過截圖記錄操作過程，最終產生 Python 巨集腳本。
  使用時機：(1) 用戶要求開啟網站、導覽、搜尋、點擊或填寫表單，
  (2) 用戶要求「錄製」或「記錄」瀏覽器操作流程，
  (3) 用戶希望獲得一個可重複執行的 Python 腳本來自動化特定任務。
  核心產出：必須產生一個位於 `macros/` 目錄下的 Python 巨集腳本，重現所有記錄的操作。
  禁止事項：除非用戶明確要求，否則禁止產生 GIF、影片或其他媒體轉換檔案。
---

# 瀏覽器錄製器 (Browser Recorder)

使用 chrome-devtools MCP 自動化 Chrome 瀏覽器操作，並將每一步記錄為截圖與 Python 巨集腳本。

## 前置作業

所有 macros 腳本會自動檢查並啟動 Chrome 偵錯模式。

- 如果 Chrome 已經在偵錯模式運行，腳本會直接使用現有連線
- 如果 Chrome 未運行，腳本會自動執行 `scripts/start_chrome_debug.bat` 啟動 Chrome
- Chrome 會使用獨立的 profile 目錄（`browser-recorder/chrome_profile`），不影響正常使用的 Chrome

手動啟動方式（可選）：
```
browser-recorder/scripts/start_chrome_debug.bat
```

## 核心流程 (巨集錄製)

每個瀏覽器任務都是一個「巨集錄製工作階段」。目標是執行一段操作順序，並將其產出為一個可獨立執行的腳本。

1. **開始錄制**：初始化任務並設定清晰的 `task_name`。
2. **執行操作**：使用 MCP 工具進行導覽與互動。
3. **擷取流程**：透過截圖記錄每一個重要步驟。
4. **產生巨集**：**強制作業**。在 `macros/` 目錄下產生一個 Python 腳本，精確重現整個流程。

## 可重複使用的巨集腳本

「巨集 (Macro)」是一個獨立的 Python 腳本，無需 AI 指令即可執行特定的瀏覽器任務。

- **儲存位置**：`browser-recorder/macros/{macro_name}.py`
- **執行方式**：使用 `python browser-recorder/macros/{macro_name}.py`
- **獨立性**：包含自動啟動 Chrome、操作邏輯、截圖等所有自足邏輯
- **自動化**：腳本會自動檢查 Chrome 狀態，必要時自動啟動偵錯模式

執行流程：
1. 腳本檢查 Chrome 是否已在偵錯模式運行
2. 如未運行，自動執行 `scripts/start_chrome_debug.bat` 啟動 Chrome
3. 連接到 Chrome 並執行自動化任務
4. 儲存截圖記錄操作過程

> [!IMPORTANT]
> 「錄製」的定義是產生程式碼腳本。除非用戶明確要求，否則**禁止**將截圖合併為 GIF、GIF 動圖或影片。產出媒體檔案而非腳本被視為嚴重的邏輯錯誤。

## 截圖儲存

**強制儲存路徑**：`browser-recorder/screenshots/{macro_name}/`
所有截圖必須依序編號（`01_`, `02_` 等）。


## Common Operations

### Navigate + Search
```
navigate_page(url="https://www.google.com")
take_screenshot()                              # record: homepage loaded
take_snapshot()                                # get search box UID
fill(uid="search-box-uid", value="query")
press_key("Enter")
wait_for("results")
take_screenshot()                              # record: search results
```

### Click a button / link
```
take_snapshot()                                # get UIDs first
click(uid="button-uid")
take_screenshot()                              # record: after click
```

### Fill a form
```
take_snapshot()
fill_form([{uid: field1, value: "..."}, {uid: field2, value: "..."}])
click(uid="submit-uid")
take_screenshot()                              # record: after submit
```

## References

- **Full MCP tool list with parameters**: See [chrome_devtools_tools.md](references/chrome_devtools_tools.md)
- **Detailed recording patterns and examples**: See [recording_workflow.md](references/recording_workflow.md)
