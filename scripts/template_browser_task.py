#!/usr/bin/env python3
"""
Browser Task Template - Reusable Chrome Automation Script

Usage:
    python template_browser_task.py

Requirements:
    pip install requests websocket-client
"""

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
TASK_NAME   = "template_task"          # Change to your task name

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
    """Start Chrome if not already running with debug port."""
    try:
        requests.get(f"http://127.0.0.1:{DEBUG_PORT}/json/version", timeout=2)
        print("Chrome already running with debug port.")
    except Exception:
        print("Chrome is not running. Starting Chrome...")
        start_chrome()


def get_ws_url():
    """Get WebSocket URL of the first open page."""
    resp = requests.get(f"http://127.0.0.1:{DEBUG_PORT}/json", timeout=5)
    pages = resp.json()
    if not pages:
        raise RuntimeError("No open pages found in Chrome.")
    return pages[0]["webSocketDebuggerUrl"]


def send_command(ws, method, params=None, cmd_id=1):
    """Send a CDP command and wait for its response."""
    msg = json.dumps({"id": cmd_id, "method": method, "params": params or {}})
    ws.send(msg)
    for _ in range(100):  # wait up to 10s
        resp = json.loads(ws.recv())
        if resp.get("id") == cmd_id:
            return resp
    raise TimeoutError(f"No response for CDP command: {method}")


def navigate(ws, url, cmd_id):
    """Navigate to URL and wait for page load."""
    print(f"  → Navigating to {url}")
    send_command(ws, "Page.navigate", {"url": url}, cmd_id)
    time.sleep(2)
    return cmd_id + 1


def screenshot(ws, filename, cmd_id):
    """Take a screenshot and save to SCREENSHOTS_DIR."""
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    resp = send_command(ws, "Page.captureScreenshot", {"format": "png"}, cmd_id)
    path = os.path.join(SCREENSHOTS_DIR, filename)
    with open(path, "wb") as f:
        f.write(base64.b64decode(resp["result"]["data"]))
    print(f"  📸 Screenshot saved: screenshots/{TASK_NAME}/{filename}")
    return cmd_id + 1


def evaluate(ws, js_expression, cmd_id):
    """Execute JavaScript in the page and return the result."""
    resp = send_command(ws, "Runtime.evaluate", {"expression": js_expression}, cmd_id)
    result = resp.get("result", {}).get("result", {}).get("value")
    return result, cmd_id + 1


def run():
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    ensure_chrome()

    ws = websocket.create_connection(get_ws_url())
    cmd_id = 1

    # ─── Task Steps ─────────────────────────────────────────────────────────
    # TODO: Replace with your actual task steps

    # Step 1: Navigate
    print("Step 1: Navigate to target URL")
    cmd_id = navigate(ws, "https://www.google.com", cmd_id)
    cmd_id = screenshot(ws, "01_start.png", cmd_id)

    # Step 2: Interact
    print("Step 2: Perform actions")
    _, cmd_id = evaluate(ws, """
        // Example: fill search box
        // document.querySelector('input[name=q]').value = 'search query';
        // document.querySelector('form').submit();
        'TODO: replace with actual interaction'
    """, cmd_id)
    time.sleep(2)
    cmd_id = screenshot(ws, "02_after_action.png", cmd_id)

    # Step 3: Extract result
    print("Step 3: Extract result")
    result, cmd_id = evaluate(ws, "document.title", cmd_id)
    print(f"  Result: {result}")
    cmd_id = screenshot(ws, "03_final.png", cmd_id)
    # ─────────────────────────────────────────────────────────────────────────

    ws.close()
    print(f"\n✅ Done! Screenshots: {SCREENSHOTS_DIR}")


if __name__ == "__main__":
    run()
