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
TASK_NAME   = "kiro_download"
SKILL_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(SKILL_DIR, "screenshots", TASK_NAME)
SCRIPTS_DIR = os.path.join(SKILL_DIR, "scripts")
TARGET_URL = "https://kiro.dev/downloads/"
DEBUG_PORT = 9222
# ────────────────────────────────────────────────────────────────────────────

def is_chrome_debugging_running():
    """檢查 9222 埠是否已開啟"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', DEBUG_PORT)) == 0

def ensure_chrome_debugging():
    """確保 Chrome 偵錯模式已啟動"""
    if is_chrome_debugging_running():
        print(f"✅ Chrome 偵錯模式已在埠 {DEBUG_PORT} 運行。")
        return True
    
    print("🚀 Chrome 偵錯模式未運行，正在啟動...")
    bat_path = os.path.join(SCRIPTS_DIR, "start_chrome_debug.bat")
    if os.path.exists(bat_path):
        subprocess.Popen([bat_path], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        # 等待 Chrome 啟動
        for _ in range(10):
            time.sleep(2)
            if is_chrome_debugging_running():
                print("✅ Chrome 啟動成功。")
                return True
        print("❌ 等待 Chrome 啟動超時。")
    else:
        print(f"❌ 找不到啟動腳本: {bat_path}")
    return False

def run():
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    
    # 確保 Chrome 偵錯模式已開啟
    if not ensure_chrome_debugging():
        print("❌ 無法建立 Chrome 偵錯環境，退出。")
        return

    # 設定位連接到現有的 Chrome 實例
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{DEBUG_PORT}")
    
    # 初始化 WebDriver (連接到已運行的 Chrome)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # 步驟 1: 導覽至下載頁面
        print(f"步驟 1: 導覽至 {TARGET_URL}")
        driver.get(TARGET_URL)
        time.sleep(3)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "01_page_loaded.png"))
        print(f"  📸 截圖已儲存: 01_page_loaded.png")

        # 步驟 2: 點擊 Download for Windows (x64)
        print("步驟 2: 尋找並點擊「Download for Windows (x64)」按鈕")
        
        try:
            # 優先嘗試精確文字匹配
            download_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Download for Windows (x64)')]")
            download_btn.click()
            print("  ✅ 已點擊下載按鈕")
        except Exception:
            # 備案：部分文字匹配
            download_btn = driver.find_element(By.PARTIAL_LINK_TEXT, "Windows (x64)")
            download_btn.click()
            print("  ✅ 已透過部分文字點擊下載按鈕")

        time.sleep(2)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "02_after_click.png"))
        print(f"  📸 截圖已儲存: 02_after_click.png")

    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
    finally:
        # 按照習慣，連接到偵錯模式時通常不關閉瀏覽器，以便用戶查看結果
        # 但我們可以釋放驅動程式資源
        # driver.quit() 
        print(f"\n✅ 完成！截圖儲存於: {SCREENSHOTS_DIR}")

if __name__ == "__main__":
    run()
