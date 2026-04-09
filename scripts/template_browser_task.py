#!/usr/bin/env python3
"""
Browser Task Template - Reusable Chrome Automation Script (Selenium Version)

Usage:
    python template_browser_task.py
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 匯入並執行依賴檢查
from utils.dependency_handler import check_and_install_dependencies
check_and_install_dependencies()

# ─── Configuration ──────────────────────────────────────────────────────────
TASK_NAME   = "template_task"          # Change to your task name

SKILL_DIR       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(SKILL_DIR, "screenshots", TASK_NAME)
# ────────────────────────────────────────────────────────────────────────────

def run():
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    
    # 設定 Chrome 選項
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 如需無頭模式請取消註解
    
    # 初始化 WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # ─── Task Steps ─────────────────────────────────────────────────────────
        # TODO: 使用 Selenium 語法實作您的任務

        # 步驟 1: 導覽至目標網址
        print("步驟 1: 導覽至 Google")
        driver.get("https://www.google.com")
        time.sleep(2)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "01_start.png"))
        print(f"  📸 截圖已儲存: 01_start.png")

        # 步驟 2: 互動示範
        print("步驟 2: 執行動作 (範例：查詢)")
        # search_box = driver.find_element(By.NAME, "q")
        # search_box.send_keys("Selenium automation")
        # search_box.submit()
        print("  (此處為範例，暫不執行實際互動)")
        time.sleep(2)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "02_after_action.png"))
        print(f"  📸 截圖已儲存: 02_after_action.png")

        # 步驟 3: 提取結果
        print("步驟 3: 提取結果")
        print(f"  頁面標題: {driver.title}")
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "03_final.png"))
        print(f"  📸 截圖已儲存: 03_final.png")
        
        # 範例：如何處理原生 JS 對話框
        # try:
        #     alert = driver.switch_to.alert
        #     print(f"偵測到對話框: {alert.text}")
        #     alert.accept()
        # except:
        #     pass

        # ─────────────────────────────────────────────────────────────────────────

    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
    finally:
        time.sleep(2)
        driver.quit()
        print(f"\n✅ 完成！截圖儲存於: {SCREENSHOTS_DIR}")

if __name__ == "__main__":
    run()
