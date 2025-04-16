import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def login_with_cookie(driver, cookie_str, domain):
    driver.get(f"https://{domain}/")
    time.sleep(3)

    cookies = [item.strip() for item in cookie_str.split(';') if item.strip()]
    for cookie in cookies:
        if '=' in cookie:
            name, value = cookie.split('=', 1)
            cookie_dict = {
                "name": name.strip(),
                "value": value.strip(),
                "domain": f".{domain}"
            }
            try:
                driver.add_cookie(cookie_dict)
            except Exception as e:
                print(f"添加 Cookie {name} 时出错：", e)
    driver.refresh()
    time.sleep(3)


def xsijishe_checkin(driver):
    driver.get("https://xsijishe.net/k_misign-sign.html")
    time.sleep(3)
    try:
        # 签到按钮，适当调整 XPath
        sign_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and contains(@value, '签到')]"))
        )
        sign_button.click()
        print("已成功完成 xsijishe 签到")
    except Exception as e:
        print("签到失败或找不到签到按钮：", e)


def main():
    # 从 Secrets 中获取
    xsijishe_cookie = os.environ.get("XSIJISHE_COOKIE")
    user_agent = os.environ.get("USER_AGENT", 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--user-data-dir=/tmp/xsijishe-profile")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        if xsijishe_cookie:
            print("使用 xsijishe Cookie 登录")
            login_with_cookie(driver, xsijishe_cookie, "xsijishe.net")
            xsijishe_checkin(driver)
        else:
            print("未提供 XSIJISHE_COOKIE")
    finally:
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    main()
