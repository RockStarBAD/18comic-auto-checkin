import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

# 从环境变量中获取配置
USER_AGENT = os.getenv('USER_AGENT')
COOKIE = os.getenv('COOKIE')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

# 检查必要的配置是否存在
if not USER_AGENT:
    print("Error: USER_AGENT is not set.")
    exit(1)

if not COOKIE and (not USERNAME or not PASSWORD):
    print("Error: Either COOKIE or both USERNAME and PASSWORD must be set.")
    exit(1)

# 配置 Chrome 浏览器选项
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument(f"user-agent={USER_AGENT}")

# 设置浏览器的默认下载路径
prefs = {"profile.default_content_settings.popups": 0,
         "download.default_directory": os.getcwd(),
         "directory_upgrade": True}
chrome_options.add_experimental_option("prefs", prefs)

# 启动浏览器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # 打开网站
    driver.get("https://18comic.vip/")

    # 如果提供了 COOKIE，则使用 COOKIE 登录
    if COOKIE:
        cookies = COOKIE.split('; ')
        for cookie in cookies:
            name, value = cookie.split('=', 1)
            driver.add_cookie({'name': name, 'value': value, 'domain': '.18comic.vip'})
        driver.refresh()
    else:
        # 使用用户名和密码登录
        login_button = driver.find_element(By.LINK_TEXT, "登入")
        login_button.click()
        time.sleep(2)

        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")

        username_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.RETURN)

        # 等待登录完成
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "簽到")))

    # 查找并点击签到按钮
    checkin_button = driver.find_element(By.LINK_TEXT, "簽到")
    checkin_button.click()

    # 等待签到完成
    WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "alert-success"), "成功"))

    print("签到成功！")

except Exception as e:
    print(f"签到失败: {e}")

finally:
    driver.quit()
