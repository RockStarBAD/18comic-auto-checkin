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
    
    # 解析 Cookie 字符串，格式为 "key1=value1; key2=value2; ..."
    cookies = [item.strip() for item in cookie_str.split(';') if item.strip()]
    for item in cookies:
        if '=' in item:
            name, value = item.split('=', 1)
            cookie_dict = {
                "name": name.strip(),
                "value": value.strip(),
                # 根据实际情况设置域名，通常为 ".18comic.vip"
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
    使用账号和密码登录（如果页面有验证码则可能需要手动解决）
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
        
        # 根据实际页面情况定位登录按钮，这里示例使用 XPath
        login_button = driver.find_element(By.XPATH, "//input[@type='submit' or @value='登录']")
        login_button.click()
    except Exception as e:
        print("账号密码登录时发生错误：", e)
    # 如果遇到验证码，请确保给足时间进行手动处理
    time.sleep(10)

def perform_checkin(driver):
    """
    执行每日签到操作
    """
    driver.get("https://18comic.vip/")
    time.sleep(3)
    try:
        # 假设签到按钮的文本包含“签到”，根据实际情况调整 XPath
        sign_button = driver.find_element(By.XPATH, "//button[contains(text(), '签到')]")
        sign_button.click()
        print("签到操作成功提交。")
    except Exception as e:
        print("签到操作未找到或执行时出错：", e)

def main():
    # 从环境变量中获取登录信息和自定义 User-Agent
    cookie = os.environ.get("COOKIE")
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    user_agent = os.environ.get("USER_AGENT", 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    
    # 配置 Selenium Chrome 驱动
    chrome_options = Options()
    # 如需要无头模式，可取消下一行的注释
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(f"user-agent={user_agent}")
    # 指定唯一的用户数据目录，避免和其他进程冲突
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-profile")
    
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
