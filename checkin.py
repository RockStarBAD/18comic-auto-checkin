import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def login_with_cookie(driver, cookie_str):
    """
    使用提供的 Cookie 登录
    """
    driver.get("https://18comic.vip/")
    time.sleep(3)
    # 解析 Cookie 字符串，格式为 "key1=value1; key2=value2; ..."
    cookies = [item.strip() for item in cookie_str.split(';') if item.strip()]
    for item in cookies:
        if '=' in item:
            name, value = item.split('=', 1)
            cookie_dict = {
                "name": name.strip(),
                "value": value.strip(),
                # 请根据实际情况设置域名（一般为 ".18comic.vip"）
                "domain": ".18comic.vip"
            }
            try:
                driver.add_cookie(cookie_dict)
            except Exception as e:
                print(f"添加 Cookie {name} 时出错：", e)
    driver.refresh()
    time.sleep(3)

def login_with_credentials(driver, username, password):
    """
    使用账号密码登录（注意：若遇验证码，可能需要手动处理）
    """
    driver.get("https://18comic.vip/login")
    time.sleep(3)
    try:
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        username_field.clear()
        username_field.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)
        # 根据页面实际情况定位登录按钮
        login_button = driver.find_element(By.XPATH, "//input[@type='submit' or @value='登录']")
        login_button.click()
    except Exception as e:
        print("账号密码登录时发生错误：", e)
    # 等待登录完成（如果有验证码，可能需要更长时间或手动介入）
    time.sleep(10)

def perform_checkin(driver):
    """
    签到逻辑：
      1. 进入首页，查找并点击【每日簽到】按钮；
      2. 等待弹出签到窗口出现，在窗口中找到并点击【簽到】按钮完成签到。
    """
    driver.get("https://18comic.vip/")
    time.sleep(3)
    try:
        daily_checkin_btn = driver.find_element(By.XPATH, "//*[contains(text(), '每日簽到')]")
        daily_checkin_btn.click()
        print("成功点击【每日簽到】按钮。")
    except Exception as e:
        print("未找到或无法点击【每日簽到】按钮：", e)
        return

    # 等待弹出窗口加载，并点击弹窗中的【簽到】按钮
    try:
        # 等待弹窗中出现包含“簽到”文本的按钮（注意：该 XPath 可能需根据实际页面微调）
        checkin_btn = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), '簽到')]"))
        )
        checkin_btn.click()
        print("成功点击弹窗中的【簽到】按钮。")
    except Exception as e:
        print("在弹窗中查找或点击【簽到】按钮失败：", e)

def main():
    # 从环境变量中获取 Secrets 配置
    cookie = os.environ.get("COOKIE")
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    user_agent = os.environ.get("USER_AGENT", 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    # 配置 Selenium Chrome 驱动
    chrome_options = Options()
    # 可选：如果需要无头运行，请取消下面注释
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(f"user-agent={user_agent}")
    # 指定独立的用户数据目录，避免冲突
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-profile")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        if cookie:
            print("使用提供的 COOKIE 进行登录")
            login_with_cookie(driver, cookie)
        elif username and password:
            print("使用账号密码登录")
            login_with_credentials(driver, username, password)
        else:
            print("未提供有效的登录信息（COOKIE 或 USERNAME/PASSWORD）")
            return

        perform_checkin(driver)
    finally:
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    main()
