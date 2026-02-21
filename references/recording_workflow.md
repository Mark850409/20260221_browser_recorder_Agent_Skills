# Recording Workflow Guide

## Table of Contents
1. [Standard Recording Pattern](#standard-recording-pattern)
2. [Screenshot Naming](#screenshot-naming)
3. [Complete Examples](#complete-examples)
4. [Troubleshooting](#troubleshooting)

---

## Standard Recording Pattern

Use this reusable pattern for every browser task. Screenshots act as the step-by-step record.

```
STEP 1: list_pages()                    → verify Chrome is connected
STEP 2: navigate_page(url=...)          → go to target URL
STEP 3: take_screenshot(filePath=...)   → RECORD initial state
STEP 4: take_snapshot()                 → get element UIDs
STEP 5: [interact]                      → click / fill / press_key
STEP 6: take_screenshot(filePath=...)   → RECORD after action
STEP 7: repeat 4-6 as needed
STEP 8: take_screenshot(fullPage=True, filePath=...) → RECORD final state
STEP 9: Create Python script in `macros/` → **關鍵產出：產生可重複執行的巨集腳本**

> [!WARNING]
> 禁止將截圖轉換為 GIF、APNG 或影片格式，除非用戶特別指示。錄製流程的唯一合法技術產出物是 Python 腳本。
```

---

## Screenshot Storage & Naming

**Mandatory Location**: `browser-recorder/screenshots/{task_name}/`

```python
# Pattern: browser-recorder/screenshots/{task_name}/{step_number}_{description}.png
take_screenshot(filePath="d:/AI_project/20260218_agent_skills/browser-recorder/screenshots/search_tsmc/01_homepage.png")
take_screenshot(filePath="d:/AI_project/20260218_agent_skills/browser-recorder/screenshots/search_tsmc/02_typed_query.png")
```

**Rules:**
- Use the skill's `screenshots/` directory
- Organize by task name
- Use numbered prefixes (`01_`, `02_`) to preserve step order
- Keep names short and descriptive

---

## Complete Examples

### 1. Google Search

```
list_pages()
navigate_page(url="https://www.google.com")
take_screenshot(filePath="d:/screenshots/01_google.png")

take_snapshot()                                     # get search box UID
fill(uid="<search-uid>", value="TSMC stock price")
take_screenshot(filePath="d:/screenshots/02_typed.png")

press_key("Enter")
wait_for("TWD")
take_screenshot(filePath="d:/screenshots/03_results.png")
```

### 2. Login Flow

```
navigate_page(url="https://example.com/login")
take_screenshot(filePath="d:/screenshots/01_login_page.png")

take_snapshot()
fill_form([
    {uid: "<email-uid>", value: "user@example.com"},
    {uid: "<pass-uid>",  value: "password123"}
])
take_screenshot(filePath="d:/screenshots/02_filled.png")

click(uid="<submit-uid>")
wait_for("Dashboard")
take_screenshot(filePath="d:/screenshots/03_logged_in.png")
```

### 3. Data Extraction (no interaction)

```
navigate_page(url="https://finance.yahoo.com/quote/TSM")
wait_for("TSM")
take_screenshot(filePath="d:/screenshots/01_stock_page.png")

evaluate_script(function="() => document.querySelector('[data-field=regularMarketPrice]')?.textContent")
take_screenshot(filePath="d:/screenshots/02_price_visible.png")
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `Could not connect to Chrome` | Run `start_chrome_debug.bat` or launch Chrome with `--remote-debugging-port=9222` |
| Element UID not found | Call `take_snapshot()` again — UIDs refresh after page changes |
| Page not loaded yet | Use `wait_for("expected text")` before interacting |
| Screenshot is blank | Add `wait_for(...)` before `take_screenshot()` |
