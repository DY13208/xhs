import json
import os

from config.config_loader import ConfigLoader

COOKIE_FILE = 'cookies.json'

# 初始化配置加载器
loader = ConfigLoader()
loader.load_config()
def save_cookie(cookie):
    """ 保存 cookie 到文件 """
    print("保存 cookie 到文件")
    cookiePath="./"+COOKIE_FILE
    loader.set_value("accounts[0].cookies", cookiePath)
    with open(COOKIE_FILE, 'w') as f:
        json.dump(cookie, f)

def load_cookie():
    """ 加载存储的 cookie """
    print("加载存储的 cookie")
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, 'r') as f:
            return json.load(f)
    return None
def clear_invalid_cookie(self):
    """ 清除无效的 cookie """
    try:
        os.remove(COOKIE_FILE)  # 删除存储的 cookie 文件
        print("已清除无效的 cookie，重新登录")
    except Exception as e:
        print(f"清除无效 cookie 时发生错误: {e}")