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
TASK_NAME   = "github_download_macro"

SKILL_DIR       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(SKILL_DIR, "screenshots", TASK_NAME)
START_CHROME_BAT = os.path.join(SKILL_DIR, "scripts", "start_chrome_debug.bat")
TARGET_URL = "https://github.com/Mark850409/20260221_browser_recorder_Agent_Skills"
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

def click_element(ws, selector, cmd_id):
    """Click an element using JavaScript."""
    script = f"document.querySelector('{selector}').click()"
    print(f"  → Clicking: {selector}")
    _, cmd_id = evaluate(ws, script, cmd_id)
    time.sleep(2)
    return cmd_id

def run():
    print(f"Starting Macro: {TASK_NAME}")
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    ensure_chrome()

    try:
        ws = websocket.create_connection(get_ws_url())
    except Exception as e:
        print(f"\nFailed to connect to Chrome: {e}")
        exit(1)

    cmd_id = 1

    try:
        # Step 1: Navigate to GitHub Repo
        print("Step 1: Navigate to GitHub Repository")
        cmd_id = navigate(ws, TARGET_URL, cmd_id)
        cmd_id = screenshot(ws, "01_github_repo_loaded.png", cmd_id)

        # Step 2: Click 'Code' button
        # Selector for the green 'Code' or 'get-repo' component
        print("Step 2: Click 'Code' button")
        # GitHub uses <get-repo> for the code button or summary with specific classes
        code_selector = "summary.btn-primary, get-repo summary, .js-get-repo-select-menu"
        # We'll use a script to find and click the most likely one
        click_script = """
        (() => {
            const btn = document.querySelector('get-repo summary') || 
                        document.querySelector('.js-get-repo-select-menu') ||
                        document.querySelector('summary.btn-primary');
            if (btn) {
                btn.click();
                return true;
            }
            return false;
        })()
        """
        success, cmd_id = evaluate(ws, click_script, cmd_id)
        if success:
            print("  Successfully clicked 'Code' button.")
        else:
            print("  FAILED to click 'Code' button.")
        
        time.sleep(2)
        cmd_id = screenshot(ws, "02_code_menu_opened.png", cmd_id)

        # Step 3: Click 'Download ZIP'
        print("Step 3: Click 'Download ZIP' button")
        download_script = """
        (() => {
            const links = Array.from(document.querySelectorAll('a'));
            const zipLink = links.find(a => a.innerText.includes('Download ZIP') || a.href.includes('zipball'));
            if (zipLink) {
                zipLink.click();
                return true;
            }
            return false;
        })()
        """
        success, cmd_id = evaluate(ws, download_script, cmd_id)
        if success:
            print("  Successfully clicked 'Download ZIP' button.")
        else:
            print("  FAILED to click 'Download ZIP' button.")
        
        time.sleep(3) # Wait for download to trigger
        cmd_id = screenshot(ws, "03_download_triggered.png", cmd_id)

    finally:
        ws.close()
        print(f"\nDone! Macro completed! Screenshots saved in: {SCREENSHOTS_DIR}")

if __name__ == "__main__":
    run()
