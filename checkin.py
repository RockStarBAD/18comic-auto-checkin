import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def login_with_cookie(driver, cookie_str):
    """
    使用提供的 Cookie 登录
    """
    driver.get("https://18comic.vip/")
    time.sleep(3)
    
    # 将 Cookie 字符串解析为多个 Cookie
    cookies = [item.strip() for item in cookie_str.split(';') if item.strip()]
    for cookie in cookies:
        if '=' in cookie:
            name, value = cookie.split('=', 1)
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
    使用账号和密码登录（登录页面若有验证码则可能需要手动介入）
    """
    driver.get("https://18comic.vip/login")
    time.sleep(3)
    try:
        # 定位用户名和密码输入框（请根据实际页面的元素属性调整）
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_field = driver.find_element(By.NAME, "password")
        
        username_field.clear()
        username_field.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)
        
        # 定位并点击登录按钮
        login_button = driver.find_element(By.XPATH, "//input[@type='submit' or @value='登录']")
        login_button.click()
    except Exception as e:
        print("账号密码登录时发生错误：", e)
    # 给足时间处理验证码或完成登录
    time.sleep(10)

def perform_checkin(driver):
    """
    进行每日签到操作：
    1. 打开主页并点击“每日簽到”
    2. 等待弹出模态框，点击模态框中的“簽到”按钮（模态框内还会有“關閉”按钮）
    """
    driver.get("https://18comic.vip/")
    time.sleep(3)
    try:
        # 点击“每日簽到”按钮
        daily_signin_trigger = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '每日簽到')]"))
        )
        daily_signin_trigger.click()
        print("已点击‘每日簽到’按钮")
        
        # 等待模态框出现，假设模态框中包含 class "modal"（请根据实际情况调整 XPath）
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'modal')]//button[contains(text(), '簽到')]"))
        )
        confirm_button.click()
        print("已点击弹出模态框中的‘簽到’按钮")
    except Exception as e:
        print("签到操作未找到或执行时出错：", e)

def main():
    # 从环境变量中获取配置（这些环境变量在 GitHub Secrets 中设置，名称保持不变）
    cookie = os.environ.get("COOKIE")
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    user_agent = os.environ.get("USER_AGENT", 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    
    # 配置 Chrome 浏览器选项
    chrome_options = Options()
    # 如果需要无头模式可以取消下面注释
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(f"user-agent={user_agent}")
    # 指定一个独一无二的用户数据目录，防止因目录冲突导致启动错误
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-profile")
    
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    
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
