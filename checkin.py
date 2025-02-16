import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def login_with_cookie(driver, cookie_str):
    """
    使用提供的 Cookie 登录
    """
    driver.get("https://18comic.vip/")
    time.sleep(3)
    cookies = [item.strip() for item in cookie_str.split(';') if item.strip()]
    for item in cookies:
        if '=' in item:
            name, value = item.split('=', 1)
            cookie_dict = {
                "name": name.strip(),
                "value": value.strip(),
                "domain": ".18comic.vip"  # 请根据实际情况调整域名
            }
            try:
                driver.add_cookie(cookie_dict)
            except Exception as e:
                print(f"添加 Cookie {name} 时出错：", e)
    driver.refresh()
    time.sleep(3)

def login_with_credentials(driver, username, password):
    """
    使用账号和密码登录（若遇验证码则可能需要手动介入）
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
        
        login_button = driver.find_element(By.XPATH, "//input[@type='submit' or @value='登录']")
        login_button.click()
    except Exception as e:
        print("账号密码登录时发生错误：", e)
    time.sleep(10)

def perform_checkin(driver):
    """
    执行签到操作
    """
    driver.get("https://18comic.vip/")
    time.sleep(3)
    try:
        sign_button = driver.find_element(By.XPATH, "//button[contains(text(), '签到')]")
        sign_button.click()
        print("签到操作成功提交。")
    except Exception as e:
        print("签到操作未找到或执行时出错：", e)

def main():
    # 从环境变量中获取登录信息和自定义的 User-Agent
    cookie = os.environ.get("COOKIE")
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    user_agent = os.environ.get("USER_AGENT", 
                                  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    
    # 配置 Selenium Chrome 驱动
    chrome_options = Options()
    # 可选：无头模式（如不需要可视化界面可启用）
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(f"user-agent={user_agent}")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        if cookie:
            print("使用提供的 Cookie 进行登录")
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
