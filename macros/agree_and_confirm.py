#!/usr/bin/env python3
import os
import time
import subprocess
import socket
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 匯入依賴檢查
try:
    from utils.dependency_handler import check_and_install_dependencies
    check_and_install_dependencies()
except ImportError:
    pass

# ─── Configuration ──────────────────────────────────────────────────────────
TASK_NAME   = "agree_and_confirm"
SKILL_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(SKILL_DIR, "screenshots", TASK_NAME)
SCRIPTS_DIR = os.path.join(SKILL_DIR, "scripts")
TARGET_URL = "file:///E:/Project/AI/AgentSkills/20260221_browser_recorder_Agent_Skills/scripts/index.html"
DEBUG_PORT = 9222
# ────────────────────────────────────────────────────────────────────────────

def is_chrome_debugging_running():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', DEBUG_PORT)) == 0

def ensure_chrome_debugging():
    if is_chrome_debugging_running():
        return True
    bat_path = os.path.join(SCRIPTS_DIR, "start_chrome_debug.bat")
    if os.path.exists(bat_path):
        subprocess.Popen([bat_path], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        for _ in range(10):
            time.sleep(2)
            if is_chrome_debugging_running():
                return True
    return False

def run():
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    if not ensure_chrome_debugging():
        print("❌ 無法啟動 Chrome 偵錯模式。")
        return

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{DEBUG_PORT}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        print(f"步驟 1: 導覽至 {TARGET_URL}")
        driver.get(TARGET_URL)
        time.sleep(2)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "01_page_loaded.png"))

        print("步驟 2: 點擊「同意」按鈕")
        agree_btn = driver.find_element(By.ID, "agree-btn")
        agree_btn.click()
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "02_alert_detected.png"))

        print("步驟 3: 處理對話框")
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except:
            pass
        
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "03_final_status.png"))
        print(f"最終狀態: {driver.find_element(By.ID, 'status').text}")

    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
    finally:
        print(f"\n✅ 完成！截圖儲存於: {SCREENSHOTS_DIR}")

if __name__ == "__main__":
    run()
