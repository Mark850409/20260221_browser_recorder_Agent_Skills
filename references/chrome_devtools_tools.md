# Chrome DevTools MCP Tools Reference

## Table of Contents
1. [Navigation](#navigation)
2. [Page Inspection](#page-inspection)
3. [Interaction](#interaction)
4. [Screenshots & Media](#screenshots--media)
5. [Network & Console](#network--console)
6. [Page Management](#page-management)
7. [Performance](#performance)

---

## Navigation

### `mcp_chrome-devtools_navigate_page`
Navigate to a URL, go back/forward in history, or reload.

```python
mcp_chrome-devtools_navigate_page(type="url", url="https://example.com")
mcp_chrome-devtools_navigate_page(type="back")
mcp_chrome-devtools_navigate_page(type="reload", ignoreCache=True)
```

**Parameters:** `type` (url/back/forward/reload), `url` (required for type=url), `ignoreCache`, `timeout`

---

## Page Inspection

### `mcp_chrome-devtools_take_snapshot`
Get accessibility tree (a11y) of the current page. Returns all elements with **uid** identifiers needed for interaction.

```python
mcp_chrome-devtools_take_snapshot()  # Always call this BEFORE clicking/filling
```

**Returns:** List of elements with uid, role, name, and other accessibility properties.

### `mcp_chrome-devtools_wait_for`
Wait for specific text to appear on the page.

```python
mcp_chrome-devtools_wait_for(text="Login successful", timeout=5000)
```

---

## Interaction

### `mcp_chrome-devtools_click`
Click an element by its uid (from snapshot).

```python
mcp_chrome-devtools_click(uid="element-uid-from-snapshot")
mcp_chrome-devtools_click(uid="element-uid", dblClick=True)  # Double click
```

### `mcp_chrome-devtools_fill`
Type into an input, textarea, or select from a `<select>` element.

```python
mcp_chrome-devtools_fill(uid="input-uid", value="search query")
```

### `mcp_chrome-devtools_fill_form`
Fill multiple form fields at once.

```python
mcp_chrome-devtools_fill_form(elements=[
    {"uid": "username-uid", "value": "user@example.com"},
    {"uid": "password-uid", "value": "secret"}
])
```

### `mcp_chrome-devtools_press_key`
Press keyboard keys or combinations.

```python
mcp_chrome-devtools_press_key(key="Enter")
mcp_chrome-devtools_press_key(key="Control+A")
mcp_chrome-devtools_press_key(key="Control+Shift+R")
```

### `mcp_chrome-devtools_hover`
Hover over an element (useful for tooltips or dropdown menus).

```python
mcp_chrome-devtools_hover(uid="menu-item-uid")
```

### `mcp_chrome-devtools_drag`
Drag one element onto another.

```python
mcp_chrome-devtools_drag(from_uid="drag-source-uid", to_uid="drop-target-uid")
```

### `mcp_chrome-devtools_handle_dialog`
Handle browser alert/confirm/prompt dialogs.

```python
mcp_chrome-devtools_handle_dialog(action="accept")
mcp_chrome-devtools_handle_dialog(action="dismiss")
mcp_chrome-devtools_handle_dialog(action="accept", promptText="my input")
```

### `mcp_chrome-devtools_upload_file`
Upload a file through a file input element.

```python
mcp_chrome-devtools_upload_file(uid="file-input-uid", filePath="/absolute/path/to/file.pdf")
```

---

## Screenshots & Media

### `mcp_chrome-devtools_take_screenshot`
Capture the current page or a specific element.

```python
mcp_chrome-devtools_take_screenshot()                          # Viewport only
mcp_chrome-devtools_take_screenshot(fullPage=True)             # Full page
mcp_chrome-devtools_take_screenshot(uid="element-uid")         # Specific element
mcp_chrome-devtools_take_screenshot(filePath="/path/out.png")  # Save to file
mcp_chrome-devtools_take_screenshot(format="jpeg", quality=80) # JPEG format
```

---

## Network & Console

### `mcp_chrome-devtools_list_network_requests`
List all network requests since last navigation.

```python
mcp_chrome-devtools_list_network_requests()
mcp_chrome-devtools_list_network_requests(resourceTypes=["fetch", "xhr"])
```

### `mcp_chrome-devtools_get_network_request`
Get details of a specific request by reqid.

```python
mcp_chrome-devtools_get_network_request(reqid=42)
```

### `mcp_chrome-devtools_list_console_messages`
Get console messages from the current page.

```python
mcp_chrome-devtools_list_console_messages()
mcp_chrome-devtools_list_console_messages(types=["error", "warn"])
```

### `mcp_chrome-devtools_evaluate_script`
Execute JavaScript in the current page.

```python
mcp_chrome-devtools_evaluate_script(function="() => { return document.title }")
mcp_chrome-devtools_evaluate_script(function="() => { return window.scrollY }")
```

---

## Page Management

### `mcp_chrome-devtools_list_pages`
List all open browser pages/tabs.

```python
mcp_chrome-devtools_list_pages()
```

### `mcp_chrome-devtools_select_page`
Switch to a specific page by ID.

```python
mcp_chrome-devtools_select_page(pageId=1, bringToFront=True)
```

### `mcp_chrome-devtools_new_page`
Open a new tab with a URL.

```python
mcp_chrome-devtools_new_page(url="https://example.com")
mcp_chrome-devtools_new_page(url="https://example.com", background=True)
```

### `mcp_chrome-devtools_close_page`
Close a specific tab (cannot close the last tab).

```python
mcp_chrome-devtools_close_page(pageId=2)
```

### `mcp_chrome-devtools_resize_page`
Resize the browser window.

```python
mcp_chrome-devtools_resize_page(width=1280, height=720)
```

---

## Performance

### `mcp_chrome-devtools_performance_start_trace`
Start recording a performance trace.

```python
mcp_chrome-devtools_performance_start_trace(reload=True, autoStop=True)
```

### `mcp_chrome-devtools_performance_stop_trace`
Stop the performance trace and get results.

```python
mcp_chrome-devtools_performance_stop_trace(filePath="trace.json")
```

---

## Common Patterns

### Basic navigation + interaction
```
1. navigate_page(url=...)
2. take_snapshot()             # Get UIDs
3. fill(uid=..., value=...)    # Type in search box
4. press_key("Enter")          # Submit
5. wait_for("results")         # Wait for content
6. take_screenshot()           # Capture result
```

### Login flow
```
1. navigate_page(url="https://example.com/login")
2. take_snapshot()
3. fill_form([{uid: username, value: ...}, {uid: password, value: ...}])
4. click(uid=submit-button-uid)
5. wait_for("Dashboard")
6. take_screenshot()
```
