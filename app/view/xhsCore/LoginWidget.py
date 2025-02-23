from time import sleep

from playwright.sync_api import sync_playwright
from PyQt5.QtCore import QThread, pyqtSignal

from app.view.xhsCore.cookie import load_cookie, save_cookie, clear_invalid_cookie
from config.config_loader import ConfigLoader

# 初始化配置加载器
loader = ConfigLoader()


# 原始代码中的 sign 函数
def sign(uri, data=None, a1="", web_session=""):
    for _ in range(10):
        try:
            with sync_playwright() as playwright:
                stealth_js_path = "./js/stealth.min.js"
                chromium = playwright.chromium
                # headless 为 True 时不显示浏览器窗口，如调试可改为 False
                browser = chromium.launch(headless=True)
                browser_context = browser.new_context()
                browser_context.add_init_script(path=stealth_js_path)
                context_page = browser_context.new_page()
                context_page.goto("https://www.xiaohongshu.com")
                browser_context.add_cookies([
                    {'name': 'a1', 'value': a1, 'domain': ".xiaohongshu.com", 'path': "/"}
                ])
                context_page.reload()
                # 必要时 sleep 一下等待 cookie 生效
                sleep(1)
                encrypt_params = context_page.evaluate("([url, data]) => window._webmsxyw(url, data)", [uri, data])
                return {
                    "x-s": encrypt_params["X-s"],
                    "x-t": str(encrypt_params["X-t"])
                }
        except Exception:
            # 遇到错误时重试
            pass
    raise Exception("重试了这么多次还是无法签名成功，寄寄寄")
# 发送验证码的线程（避免阻塞 UI）
class SendCodeThread(QThread):
    send_finished = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, phone, xhs_client, parent=None):
        super().__init__(parent)
        self.phone = phone
        self.xhs_client = xhs_client

    def run(self):
        try:
            self.xhs_client.send_code(self.phone)
            self.send_finished.emit("验证码发送成功")
        except Exception as e:
            self.error_occurred.emit(str(e))


# 登录的线程
class LoginThread(QThread):
    login_finished = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, phone, code, xhs_client, parent=None):
        super().__init__(parent)
        self.phone = phone
        self.code = code
        self.xhs_client = xhs_client

    def run(self):
        # 尝试加载现有的 cookie
        stored_cookie = load_cookie()
        if stored_cookie:
            # 如果有存储的 cookie，直接使用它进行登录
            try:
                self.xhs_client.cookie = stored_cookie  # 设置已有的 cookie
                self_info = self.xhs_client.get_self_info()  # 获取用户信息
                result = {
                    "self_info": self_info,
                    "cookie": self.xhs_client.cookie,
                }
                self.login_finished.emit(result)  # 返回登录成功的结果
                return  # 直接返回，不需要再执行登录过程
            except Exception as e:
                self.error_occurred.emit(f"使用 cookie 登录失败: {str(e)}")
                clear_invalid_cookie(self)
                return

        # 如果没有 cookie 或 cookie 无效，则执行正常的登录流程
        try:
            check_res = self.xhs_client.check_code(self.phone, self.code)
            token = check_res["mobile_token"]
            login_res = self.xhs_client.login_code(self.phone, token)
            self_info = self.xhs_client.get_self_info()

            # 获取登录成功的 cookie
            result = {
                "login_res": login_res,
                "self_info": self_info,
                "cookie": self.xhs_client.cookie,
            }
            print("验证码方式登录成功！",result)
            # 保存新的 cookie
            save_cookie(self.xhs_client.cookie)
            loader.set_value("accounts[0].phone", self.phone)

            self.login_finished.emit(result)  # 发射登录成功信号
        except Exception as e:
            self.error_occurred.emit(str(e))

# 发布笔记的线程
class PublishNoteThread(QThread):
    publish_finished = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, title, desc, images, post_time, xhs_client, parent=None):
        super().__init__(parent)
        self.title = title
        self.desc = desc
        self.images = images
        self.post_time = post_time
        self.xhs_client = xhs_client

    def run(self):
        try:
            note = self.xhs_client.create_image_note(
                self.title, self.desc, self.images,
                is_private=True, post_time=self.post_time
            )
            self.publish_finished.emit(note)
        except Exception as e:
            self.error_occurred.emit(str(e))
