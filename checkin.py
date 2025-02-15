import os
import sys
import re
import requests

# 设置请求头（可根据需要调整）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    # Cookie 将在调用时动态添加
}

def get_daily_id(cookie):
    """
    访问主页获取签到所需的 daily_id
    """
    headers = HEADERS.copy()
    headers["Cookie"] = cookie
    url = "https://18comic.vip/"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            html = resp.text
            # 假设页面中存在类似：data-dailyid="xxxx" 的属性
            match = re.search(r'data-dailyid="([^"]+)"', html)
            if match:
                daily_id = match.group(1)
                print("提取到 daily_id:", daily_id)
                return daily_id
            else:
                print("未能从主页提取 daily_id，请检查页面结构是否发生变化")
                return None
        else:
            print(f"获取主页失败，状态码：{resp.status_code}")
            return None
    except Exception as e:
        print("获取 daily_id 异常：", e)
        return None

def daily_sign(cookie):
    """
    使用 Cookie 完成签到
    """
    daily_id = get_daily_id(cookie)
    if not daily_id:
        print("无法获取 daily_id，签到终止")
        return

    headers = HEADERS.copy()
    headers["Cookie"] = cookie
    sign_url = "https://18comic.vip/ajax/user_daily_sign"
    # 部分签到接口可能需要传递 daily_id 参数
    data = {
        "daily_id": daily_id,
        "oldStep": "1"
    }
    try:
        resp = requests.post(sign_url, headers=headers, data=data, timeout=10)
        resp.raise_for_status()
        result = resp.json()
        # 根据接口返回结果判断签到是否成功
        if "成功" in result.get("msg", ""):
            print("签到成功：", result.get("msg"))
        else:
            print("签到返回信息：", result)
    except Exception as e:
        print("签到请求异常：", e)

def login_with_credentials(username, password):
    """
    尝试使用账号和密码登录（注意：18comic.vip 登录时可能要求验证码，此处无法自动处理验证码）
    若登录成功，应返回登录后的 Cookie 字符串
    """
    login_url = "https://18comic.vip/login"
    # 构造登录请求的参数（根据实际抓包信息调整）
    data = {
        "username": username,
        "password": password,
        "login_remember": "on",
        "submit_login": ""  # 根据实际情况可能需要调整
    }
    headers = HEADERS.copy()
    try:
        resp = requests.post(login_url, headers=headers, data=data, timeout=10)
        # 如果遇到验证码问题，可能返回 301 或 403 等状态码
        if resp.status_code != 200:
            print(f"登录请求失败，状态码：{resp.status_code}")
            return None

        # 登录后通常会在响应的 Cookie 中返回登录信息
        if resp.cookies:
            cookie = "; ".join([f"{c.name}={c.value}" for c in resp.cookies])
            print("登录成功，获取到 Cookie")
            return cookie
        else:
            print("登录后未获取到 Cookie，请检查是否需要验证码处理")
            return None
    except Exception as e:
        print("登录异常：", e)
        return None

def main():
    # 从环境变量中获取 Secrets
    cookie = os.environ.get("COMIC_COOKIE")
    username = os.environ.get("COMIC_USERNAME")
    password = os.environ.get("COMIC_PASSWORD")
    
    if cookie:
        print("使用提供的 Cookie 进行签到")
        daily_sign(cookie)
    elif username and password:
        print("未检测到 Cookie，尝试使用用户名密码登录")
        cookie = login_with_credentials(username, password)
        if cookie:
            daily_sign(cookie)
        else:
            print("账号密码登录失败，请检查是否存在验证码问题，建议手动获取 Cookie 后使用")
            sys.exit(1)
    else:
        print("请在 Secrets 中配置 COMIC_COOKIE 或 COMIC_USERNAME/COMIC_PASSWORD")
        sys.exit(1)

if __name__ == "__main__":
    main()
