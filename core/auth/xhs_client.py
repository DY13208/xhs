import os
import json
import time
from selenium import webdriver
from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class XHSClient:
    """
    小红书客户端，包含登录和发布文章的自动化操作。
    使用 Selenium 控制 Chrome 浏览器。
    """

    def __init__(self):
        # 启动 Chrome 浏览器（请确保已安装对应版本的 ChromeDriver）
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 15)
        # 当前文件所在目录，用于存储 token 和 cookies 文件
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.token_file = os.path.join(current_dir, "xiaohongshu_token.json")
        self.cookies_file = os.path.join(current_dir, "xiaohongshu_cookies.json")
        self.token = self._load_token()
        self._load_cookies()

    def _load_token(self):
        """从文件加载 token，如果存在且未过期，则返回 token"""
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'r', encoding='utf-8') as f:
                    token_data = json.load(f)
                    if token_data.get('expire_time', 0) > time.time():
                        return token_data.get('token')
            except Exception as e:
                print("加载 token 时出错：", e)
        return None

    def _save_token(self, token):
        """保存 token 到文件，设置有效期为 30 天"""
        token_data = {
            'token': token,
            'expire_time': time.time() + 30 * 24 * 3600
        }
        try:
            with open(self.token_file, 'w', encoding='utf-8') as f:
                json.dump(token_data, f)
        except Exception as e:
            print("保存 token 时出错：", e)

    def _load_cookies(self):
        """从文件加载 cookies 并添加到浏览器"""
        if os.path.exists(self.cookies_file):
            try:
                with open(self.cookies_file, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                    self.driver.get("https://creator.xiaohongshu.com")
                    for cookie in cookies:
                        self.driver.add_cookie(cookie)
            except Exception as e:
                print("加载 cookies 出错：", e)

    def _save_cookies(self):
        """保存当前浏览器 cookies 到文件"""
        try:
            cookies = self.driver.get_cookies()
            with open(self.cookies_file, 'w', encoding='utf-8') as f:
                json.dump(cookies, f)
        except Exception as e:
            print("保存 cookies 出错：", e)

    def login(self, phone, country_code="+86"):
        """
        登录流程：
          1. 若已有有效 token，则直接返回；
          2. 尝试使用 cookies 登录；
          3. 若 cookies 无效，则进入手动登录流程：
             - 选择国家/区号；
             - 输入手机号，发送验证码；
             - 用户手动输入验证码；
             - 点击登录按钮；
          4. 登录成功后保存 cookies，并尝试获取 token。

        注：如果登录过程中需要人工验证（例如滑块验证），
        用户在浏览器中完成验证后请按提示输入验证码继续流程。
        """
        if self.token:
            print("已有有效 token，无需重新登录。")
            return

        # 尝试使用 cookies 登录
        self.driver.get("https://creator.xiaohongshu.com/login")
        self._load_cookies()
        self.driver.refresh()
        time.sleep(3)
        if "login" not in self.driver.current_url.lower():
            print("使用 cookies 登录成功。")
            self._save_cookies()
            self.token = self._load_token()
            return
        else:
            self.driver.delete_all_cookies()
            print("无效的 cookies，进入手动登录流程。")

        self.driver.get("https://creator.xiaohongshu.com/login")
        time.sleep(3)

        # 选择国家/区号
        try:
            country_input = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input[placeholder='请选择选项']")))
            country_input.click()
            time.sleep(1)
            country_selector = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//input[@placeholder='请输入国家或区号']")))
            country_selector.clear()
            country_selector.send_keys(country_code)
            time.sleep(1)
            option = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//div[contains(text(), '{country_code}')]")))
            option.click()
            time.sleep(2)
        except Exception as e:
            print("选择国家/区号时出错：", e)
            self.driver.save_screenshot("error_select_country.png")

        # 输入手机号
        try:
            phone_input = self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='手机号']")))
            phone_input.clear()
            phone_input.send_keys(phone)
        except Exception as e:
            print("手机号输入框加载失败：", e)
            self.driver.save_screenshot("error_phone_input.png")

        # 点击发送验证码按钮
        try:
            send_code_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'发送验证码')]")))
            try:
                send_code_btn.click()
            except Exception as click_e:
                print("常规点击发送验证码失败，尝试 JavaScript 点击...", click_e)
                self.driver.execute_script("arguments[0].click();", send_code_btn)
        except Exception as e:
            print("点击发送验证码按钮失败：", e)
            self.driver.save_screenshot("error_send_code.png")

        # 输入验证码（需人工输入）
        verification_code = input("请输入验证码: ")
        try:
            code_input = self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='验证码']")))
            code_input.clear()
            code_input.send_keys(verification_code)
        except Exception as e:
            print("验证码输入框加载失败：", e)
            self.driver.save_screenshot("error_code_input.png")

        # 点击登录按钮
        try:
            login_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".beer-login-btn")))
            try:
                login_button.click()
            except Exception as click_e:
                print("常规登录按钮点击失败，尝试 JavaScript 点击...", click_e)
                self.driver.execute_script("arguments[0].click();", login_button)
        except Exception as e:
            print("登录按钮点击失败：", e)
            self.driver.save_screenshot("error_login_click.png")

        # 等待登录完成
        time.sleep(5)
        self._save_cookies()
        self.token = self._load_token()
        if self.token:
            print("登录成功，token 已保存。")
        else:
            print("登录完成，但未能获取 token，请检查登录状态。")
            self.driver.save_screenshot("error_after_login.png")

    def post_article(self, title, content, images):
        """
        发布文章流程：
          1. 进入发布页面；
          2. 先切换到“上传图文” tab（因为默认可能是上传视频）；
          3. 上传图片，上传图片后页面会切换到文章编辑状态；
          4. 填写文章标题和内容；
          5. 点击发布按钮完成发布；
          6. 调试时打印当前 URL 以确认页面状态。

        正确的发布页面 URL 为：
          https://creator.xiaohongshu.com/publish/publish?from=menu
        """
        try:
            # 进入发布页面
            self.driver.get("https://creator.xiaohongshu.com/publish/publish?from=menu")
            print("进入发布页面")

            # Step 0: 切换到“上传图文” tab
            try:
                tabs = self.driver.find_elements(By.CSS_SELECTOR, ".creator-tab")
                switched = False
                for tab in tabs:
                    # 查找包含“上传图文”的 tab
                    if "上传图文" in tab.text:
                        # 如果该 tab 没有 active 类，则点击切换
                        if "active" not in tab.get_attribute("class"):
                            tab.click()
                            print("已切换到上传图文 tab")
                            time.sleep(2)  # 等待页面刷新
                        else:
                            print("当前已在上传图文 tab")
                        switched = True
                        break
                if not switched:
                    print("未找到“上传图文” tab，可能页面结构已变更。")
            except Exception as e_tab:
                print("切换到上传图文 tab 时出错：", e_tab)

            # Step 1: 上传图片（必须上传图片后才能进入编辑页面）
            if images:
                print("开始上传图片...")
                upload_input = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".upload-input"))
                )
                upload_input.send_keys(images[0])
                print("图片上传请求已发送，等待页面切换到编辑状态...")

                # 等待编辑页面加载（假设编辑页面出现 .editor-title-input 元素）
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".editor-title-input"))
                )
                print("图片上传成功，进入文章编辑页面。")
            else:
                print("未提供图片，无法上传。")
                return

            # Step 2: 填写文章标题和内容
            title_input = self.driver.find_element(By.CSS_SELECTOR, ".editor-title-input")
            title_input.clear()
            title_input.send_keys(title)

            content_input = self.driver.find_element(By.CSS_SELECTOR, ".editor-content-input")
            content_input.clear()
            content_input.send_keys(content)
            print("文章标题和内容填写完成。")

            # Step 3: 点击发布按钮
            publish_button = self.driver.find_element(By.CSS_SELECTOR, ".publish-button")
            publish_button.click()
            print("点击发布按钮...")

            # Step 4: 等待发布操作完成，打印当前 URL 以供调试
            time.sleep(5)
            current_url = self.driver.current_url
            print(f"发布操作后当前页面URL：{current_url}")
            if "explore" in current_url or "404" in current_url:
                print("页面跳转不正确，请检查发布流程和页面状态。")
            else:
                print("文章发布流程完成。")

        except TimeoutException:
            print("发布文章超时，请检查页面结构或网络状态。")
        except WebDriverException as e:
            print(f"发布文章失败：{e}")
