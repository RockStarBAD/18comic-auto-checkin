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
                # 根据实际情况设置域名（通常为 ".18comic.vip"）
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
    使用账号和密码登录（登录时若遇验证码则可能需要手动处理）
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
        
        # 定位登录按钮（请根据实际页面调整XPath）
        login_button = driver.find_element(By.XPATH, "//input[@type='submit' or @value='登录']")
        login_button.click()
    except Exception as e:
        print("账号密码登录时发生错误：", e)
    # 等待登录过程完成（若有验证码，此处可能需要手动介入）
    time.sleep(10)

def perform_checkin(driver):
    """
    签到逻辑修改：
    1. 在首页点击“每日簽到”按钮；
    2. 等待弹出签到弹窗；
    3. 在弹窗中点击“簽到”按钮（排除“關閉”按钮）。
    """
    driver.get("https://18comic.vip/")
    time.sleep(3)
    
    try:
        # 等待并点击“每日簽到”按钮
        daily_signin_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '每日簽到')]"))
        )
        daily_signin_button.click()
        print("已点击【每日簽到】按钮")
    except Exception as e:
        print("未能找到每日簽到按钮：", e)
        return

    # 等待签到弹窗出现
    try:
        # 等待弹窗中的“簽到”按钮变为可点击状态（确保排除“每日簽到”的重复元素）
        checkin_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '簽到') and not(contains(text(), '每日簽到'))]"))
        )
        checkin_button.click()
        print("已点击弹窗中的【簽到】按钮")
    except Exception as e:
        print("签到弹窗中未找到或点击【簽到】按钮出错：", e)

def main():
    # 从环境变量中获取 Secrets（无需改变名称）
    cookie = os.environ.get("COOKIE")
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    user_agent = os.environ.get("USER_AGENT", 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    
    # 配置 Selenium Chrome 驱动
    chrome_options = Options()
    # 如果需要无头模式，可取消下面注释
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(f"user-agent={user_agent}")
    # 指定一个唯一的用户数据目录，避免冲突
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
