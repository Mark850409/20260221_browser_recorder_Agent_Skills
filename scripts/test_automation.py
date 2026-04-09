import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 匯入依賴檢查工具
from utils.dependency_handler import check_and_install_dependencies
check_and_install_dependencies()

def run_test():
    # 設定 Chrome 選項
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 如果需要背景執行可以取消註解
    
    # 初始化 WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # 取得 index.html 的絕對路徑
        file_path = os.path.abspath("index.html")
        driver.get(f"file:///{file_path}")
        
        print(f"已打開頁面: {file_path}")
        time.sleep(1) # 稍微等待載入
        
        # 尋找「同意」按鈕並點擊
        agree_button = driver.find_element(By.ID, "agree-btn")
        agree_button.click()
        print("已點擊「同意」按鈕")
        
        time.sleep(1) # 等待對話框彈出
        
        # 切換到 Alert 對話框並點擊確定 (Accept)
        try:
            alert = driver.switch_to.alert
            print(f"偵測到對話框文字: {alert.text}")
            alert.accept()
            print("已點擊對話框中的「確定」")
        except Exception as alert_err:
            print(f"處理對話框時發生錯誤 (可能對話框未出現): {alert_err}")
        
        # 檢查頁面狀態文字是否更新
        time.sleep(1)
        status_text = driver.find_element(By.ID, "status").text
        print(f"頁面狀態: {status_text}")
        
        if "您點擊了確定" in status_text:
            print("測試成功！")
        else:
            print("測試失敗：狀態文字不符合預期")
            
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        # 等待幾秒後關閉瀏覽器
        time.sleep(3)
        driver.quit()
        print("瀏覽器已關閉")

if __name__ == "__main__":
    run_test()
