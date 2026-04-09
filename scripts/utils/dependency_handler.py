import subprocess
import sys
import pkg_resources
import os

def check_and_install_dependencies():
    """
    檢查 requirements.txt 檔案，並自動安裝缺失的套件。
    """
    script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    req_file = os.path.join(script_dir, "requirements.txt")
    
    if not os.path.exists(req_file):
        print(f"警告: 找不到 {req_file}，跳過相依性檢查。")
        return

    print("正在執行相依性檢查...")
    with open(req_file, "r") as f:
        dependencies = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    missing = []
    for dep in dependencies:
        # 處理帶有版本號的情況 (例如 selenium>=4.0.0)
        package_name = dep.split(">=")[0].split("==")[0].split("<")[0].strip()
        try:
            pkg_resources.require(dep)
        except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
            missing.append(dep)

    if missing:
        print(f"偵測到缺失或版本不符的套件: {', '.join(missing)}")
        print("正在嘗試自動安裝...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
            print("安裝完成！")
        except subprocess.CalledProcessError as e:
            print(f"安裝失敗: {e}")
            sys.exit(1)
    else:
        print("所有必要套件均已安裝。")

if __name__ == "__main__":
    check_and_install_dependencies()
