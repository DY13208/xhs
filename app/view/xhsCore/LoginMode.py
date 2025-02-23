from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QMessageBox, QSizePolicy, QTextEdit, QSpacerItem
)

from config.config_loader import ConfigLoader
from qfluentwidgets import (
    LineEdit, PushButton, FluentIcon, BodyLabel, TextEdit
)
import json

from .LoginWidget import SendCodeThread, LoginThread
from .login_manager import LoginManager
# 初始化配置加载器
loader = ConfigLoader()
loader.load_config()
class LoginMode(QWidget):
    def __init__(self, xhs_client, input_validator,login_manager, parent=None):
        super().__init__(parent)
        self.xhs_client = xhs_client
        self.input_validator = input_validator
        self.login_manager = login_manager
        self.init_ui()

    def init_ui(self):
        """ 初始化UI组件 """
        widget = self
        v_layout = QVBoxLayout(widget)
        v_layout.setSpacing(15)
        v_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # 添加一行布局，包含标签、输入框和按钮
        def addRow(label_text, input_widget=None, button_text=None, button_callback=None):
            """ 添加标签、输入框和按钮的一行布局 """
            row = QHBoxLayout()
            row.setSpacing(10)
            row.setAlignment(Qt.AlignLeft)

            # 标签
            label = BodyLabel(self.tr(label_text), widget)
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            label.setStyleSheet("background: none; border: none;")
            row.addWidget(label)

            if input_widget:
                input_widget.setFixedWidth(250)
                row.addWidget(input_widget)

            if button_text:
                btn = PushButton(self.tr(button_text), widget)
                btn.setFixedWidth(160)
                btn.clicked.connect(button_callback)
                row.addWidget(btn)

            v_layout.addLayout(row)

        def create_phone_input_and_buttons(widget, v_layout, is_phone_set=False):
            # 行1：手机号输入
            self.phoneLineEdit = LineEdit(widget)
            self.phoneLineEdit.setPlaceholderText(self.tr("请输入手机号"))
            addRow("手机号：", self.phoneLineEdit)

            # 行2：如果手机号未设置，添加验证码输入框和发送验证码按钮
            if not is_phone_set:
                self.codeLineEdit = LineEdit(widget)
                self.codeLineEdit.setPlaceholderText(self.tr("请输入验证码"))
                addRow("验证码：", self.codeLineEdit)

                self.sendCodeButton = PushButton(self.tr("发送验证码"), widget)
                self.sendCodeButton.setIcon(FluentIcon.MESSAGE)
                self.sendCodeButton.setFixedWidth(160)
                self.sendCodeButton.clicked.connect(self.send_code)

            # 行3：登录按钮
            self.loginButton = PushButton(self.tr("登录"), widget)
            self.loginButton.setIcon(FluentIcon.UP)
            self.loginButton.setFixedWidth(160)
            self.loginButton.clicked.connect(lambda: self.login(is_phone_set))

            # 创建按钮布局
            row = QHBoxLayout()
            row.setSpacing(10)
            row.setAlignment(Qt.AlignLeft)

            if not is_phone_set:
                self.phoneLineEdit = is_phone_set
                row.addWidget(self.sendCodeButton)

            # 如果手机号已配置，按钮居中显示
            if is_phone_set:
                self.phoneLineEdit.setText(loader.get_value("accounts[0].phone"))
                row.addItem(QSpacerItem(100, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))

            row.addWidget(self.loginButton)
            v_layout.addLayout(row)

        if loader.get_value("accounts[0].phone") is None:
            # 手机号未设置，显示验证码输入框等
            create_phone_input_and_buttons(widget, v_layout, is_phone_set=False)
        else:
            # 手机号已设置，省略验证码部分并让登录按钮居中显示
            create_phone_input_and_buttons(widget, v_layout, is_phone_set=True)



        # 行4：状态显示
        self.loginStatusText = TextEdit(widget)
        self.loginStatusText.setReadOnly(True)
        self.loginStatusText.setFixedWidth(400)
        self.loginStatusText.setPlaceholderText(self.tr("登录状态显示在这里..."))
        addRow("状态：", self.loginStatusText)

    # 通用方法：创建手机号输入框和按钮

    def send_code(self):

        phone = self.phoneLineEdit.text().strip()
        if not phone:
            # QMessageBox.warning(self, self.tr("提示"), self.tr("请输入手机号"))
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入手机号和验证码"
            )
            return
        self.sendCodeButton.setEnabled(False)
        self.loginStatusText.append(self.tr("正在发送验证码..."))
        self.sendThread = SendCodeThread(phone, self.xhs_client)
        self.sendThread.send_finished.connect(self.on_send_finished)
        self.sendThread.error_occurred.connect(self.on_send_error)
        self.sendThread.start()

    def on_send_finished(self, message):
        self.loginStatusText.append(message)
        self.sendCodeButton.setEnabled(True)

    def on_send_error(self, error):
        self.loginStatusText.append(self.tr("发送验证码失败: ") + error)
        self.sendCodeButton.setEnabled(True)

    def login(self, is_phone_set) -> None:
        phone = self.phoneLineEdit.text().strip()

        if is_phone_set:
            code = 666
            if not phone:
                self.input_validator.show_empty_input_dialog(
                    title='警告',
                    content="请输入手机号"
                )
                return
        else:
            code = self.codeLineEdit.text().strip()
            if not phone and not code:
                self.input_validator.show_empty_input_dialog(
                    title='警告',
                    content="请输入手机号和验证码"
                )
                return
        # 使用 LoginThread 进行登录，传递手机号输入框
        self.loginButton.setEnabled(False)
        self.loginStatusText.append(self.tr("正在登录..."))
        self.loginThread = LoginThread(phone, code, self.xhs_client,self.phoneLineEdit)
        self.loginThread.login_finished.connect(self.on_login_finished)
        self.loginThread.error_occurred.connect(self.on_login_error)
        self.loginThread.start()

    def on_login_finished(self, result):
        self.loginStatusText.append(self.tr("登录成功！"))
        self.loginStatusText.append(self.tr("当前 cookie: ") + result.get("cookie", ""))
        self.login_manager.login_successful()
        self.loginStatusText.append(self.tr("用户信息: ") + json.dumps(result.get("self_info", {}), ensure_ascii=False, indent=4))
        self.loginButton.setEnabled(False)

    def on_login_error(self, error):
        self.loginStatusText.append(self.tr("登录失败: ") + error)
        self.login_manager.logout()
        self.loginButton.setEnabled(True)
