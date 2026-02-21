#!/usr/bin/env python3
import subprocess
import time
import json
import os
import base64
import requests
import websocket

# ─── Configuration ──────────────────────────────────────────────────────────
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DEBUG_PORT  = 9222
TASK_NAME   = "tsmc_stock_search_macro"

SKILL_DIR       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(SKILL_DIR, "screenshots", TASK_NAME)
START_CHROME_BAT = os.path.join(SKILL_DIR, "scripts", "start_chrome_debug.bat")
# ────────────────────────────────────────────────────────────────────────────

def start_chrome():
    """Start Chrome with remote debugging using the batch script."""
    print("Starting Chrome with remote debugging...")
    if not os.path.exists(START_CHROME_BAT):
        print(f"Error: {START_CHROME_BAT} not found!")
        exit(1)
    
    # Execute the batch script
    subprocess.Popen([START_CHROME_BAT], shell=True)
    print("Waiting for Chrome to start...")
    time.sleep(6)

def ensure_chrome():
    """Check if Chrome is already running with debug port, start if not."""
    try:
        requests.get(f"http://127.0.0.1:{DEBUG_PORT}/json/version", timeout=2)
        print("Chrome is running and accessible via debug port.")
    except Exception:
        print("Chrome is not running. Starting Chrome...")
        start_chrome()

def get_ws_url():
    """Get WebSocket URL of the first open page."""
    resp = requests.get(f"http://127.0.0.1:{DEBUG_PORT}/json", timeout=5)
    pages = resp.json()
    if not pages:
        # Create a new page if none exists
        requests.put(f"http://127.0.0.1:{DEBUG_PORT}/json/new")
        time.sleep(1)
        resp = requests.get(f"http://127.0.0.1:{DEBUG_PORT}/json", timeout=5)
        pages = resp.json()
    
    # Filter for standard pages
    for page in pages:
        if page.get("type") == "page" and "webSocketDebuggerUrl" in page:
            return page["webSocketDebuggerUrl"]
    
    raise RuntimeError("No suitable open pages found in Chrome.")

def send_command(ws, method, params=None, cmd_id=1):
    """Send a CDP command and wait for its response."""
    msg = json.dumps({"id": cmd_id, "method": method, "params": params or {}})
    ws.send(msg)
    for _ in range(100):
        resp = json.loads(ws.recv())
        if resp.get("id") == cmd_id:
            return resp
    raise TimeoutError(f"No response for CDP command: {method}")

def navigate(ws, url, cmd_id):
    """Navigate to URL and wait for page load."""
    print(f"  → Navigating to {url}")
    send_command(ws, "Page.navigate", {"url": url}, cmd_id)
    time.sleep(5) # Wait for page to load
    return cmd_id + 1

def screenshot(ws, filename, cmd_id):
    """Take a screenshot and save to SCREENSHOTS_DIR."""
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    resp = send_command(ws, "Page.captureScreenshot", {"format": "png"}, cmd_id)
    path = os.path.join(SCREENSHOTS_DIR, filename)
    with open(path, "wb") as f:
        f.write(base64.b64decode(resp["result"]["data"]))
    print(f"  Screenshot saved: browser-recorder/screenshots/{TASK_NAME}/{filename}")
    return cmd_id + 1

def evaluate(ws, js_expression, cmd_id):
    """Execute JavaScript in the page and return the result."""
    resp = send_command(ws, "Runtime.evaluate", {"expression": js_expression}, cmd_id)
    result = resp.get("result", {}).get("result", {}).get("value")
    return result, cmd_id + 1

def run():
    print(f"Starting Macro: {TASK_NAME}")
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    ensure_chrome()

    try:
        ws = websocket.create_connection(get_ws_url())
    except websocket.WebSocketBadStatusException as e:
        if e.status_code == 403:
            print("\nError: WebSocket connection 403 Forbidden.")
            print("Chrome security policy rejected the connection.")
            print("Ensure Chrome is started with: --remote-allow-origins=*")
            print("Try running the updated start_chrome_debug.bat.")
        else:
            print(f"\nWebSocket Error: {e}")
        exit(1)
    except Exception as e:
        print(f"\nFailed to connect to Chrome: {e}")
        exit(1)

    cmd_id = 1

    try:
        # Step 1: Navigate to TSMC Finance Page
        print("Step 1: Navigate to TSMC Finance Page")
        cmd_id = navigate(ws, "https://www.google.com/finance/quote/2330:TPE", cmd_id)
        cmd_id = screenshot(ws, "01_finance_home.png", cmd_id)

        # Step 2: Extract Result
        print("Step 2: Extract current stock price")
        # Wait a bit more for dynamic content
        time.sleep(2)
        
        # Extract price using multiple possible selectors for Google Finance
        price_script = """
        (() => {
            const selectors = ['.YMlS1d', '.fxKb9e', '[data-last-price]'];
            for (const s of selectors) {
                const el = document.querySelector(s);
                if (el && el.textContent) return el.textContent;
            }
            return null;
        })()
        """
        price, cmd_id = evaluate(ws, price_script, cmd_id)
        
        if price:
            print(f"  Current TSMC Stock Price: {price}")
        else:
            print("  Could not find price element. The page structure might have changed.")

        cmd_id = screenshot(ws, "02_price_loaded.png", cmd_id)

    finally:
        ws.close()
        print(f"\nDone! Macro completed! Screenshots saved in: {SCREENSHOTS_DIR}")

if __name__ == "__main__":
    run()
