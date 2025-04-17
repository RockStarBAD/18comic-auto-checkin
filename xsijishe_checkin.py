import os
import time
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def main():
    # 创建一个唯一的临时用户数据目录
    user_data_dir = tempfile.mkdtemp()

    # 设置 Chrome 选项
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument("--headless")  # 如果您希望在无头模式下运行
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 初始化 WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 设置 Cookie 登录
        driver.get("https://xsijishe.net")
        cookie_str = os.environ.get("XSIJISHE_COOKIE")
        if not cookie_str:
            print("未找到 XSIJISHE_COOKIE 环境变量。")
            return
        cookies = [item.strip().split("=", 1) for item in cookie_str.split(";") if "=" in item]
        for name, value in cookies:
            driver.add_cookie({"name": name, "value": value})

        # 访问签到页面
        driver.get("https://xsijishe.net/k_misign-sign.html")
        time.sleep(5)  # 等待页面加载

        # 查找并点击“每日签到”按钮
        daily_signin_button = driver.find_element(By.LINK_TEXT, "每日签到")
        daily_signin_button.click()
        time.sleep(2)  # 等待弹出窗口加载

        # 在弹出窗口中查找并点击“签到”按钮
        signin_button = driver.find_element(By.LINK_TEXT, "签到")
        signin_button.click()
        time.sleep(2)  # 等待签到完成

        print("签到成功。")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        driver.quit()
