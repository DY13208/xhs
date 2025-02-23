# coding:utf-8

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout,
    QScrollArea,  QLabel
)
from qfluentwidgets import (CardWidget)


from .xhsCore.LoginWidget import *
from .xhsCore.Message import InputValidator
from xhs import XhsClient
from .xhsCore.LoginMode import LoginMode
from .xhsCore.api_widget import APIWidget
from .xhsCore.login_manager import LoginManager
from .xhsCore.note_module import NoteWidget


# -------------------- HomeInterface 定义 --------------------
class HomeInterface(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("homeInterface")

        # 创建 LoginManager 的单例实例
        self.login_manager = LoginManager()

        self.xhs_client = XhsClient(sign=sign)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)
        self.vBoxLayout.setSpacing(20)
        self.vBoxLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.input_validator = InputValidator(self)
        self.login_manager.set_input_validator(self.input_validator)

        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;  /* 设置所有控件的背景为白色 */
                border: none;  
                border-radius: 10px;
            }
        """)

        self.initUI()
        self.setWidget(self.view)
        self.setWidgetResizable(True)

    def initUI(self):
        # 外部标题和卡片紧密连接
        self.addSection(self.tr("登录"), self.createLoginWidget())
        self.addSection(self.tr("发布笔记"), self.createNoteWidget())
        self.addSection(self.tr("API 操作"), self.createAPIWidget())
        # API 操作区域直接添加，不使用 addSection() 包装
        # self.vBoxLayout.addWidget(self.createAPIWidget())
        self.vBoxLayout.addStretch()
        self.vBoxLayout.addStretch()
        # self.input_validator = InputValidator(self)

    def addSection(self, title: str, content: QWidget):
        # 使用 CardWidget 包装标题和内容
        card = CardWidget(self)
        card.setStyleSheet("""
            CardWidget {
                background-color: #F9F9F9;  /* 设置卡片背景为浅灰色 */
                border: 1px solid #D3D3D3; 
                border-radius: 8px;
            }
        """)
        cardLayout = QVBoxLayout(card)
        cardLayout.setContentsMargins(20, 10, 20, 20)
        cardLayout.setSpacing(10)
        cardLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # 标题
        titleLabel = QLabel(title, self)
        titleLabel.setStyleSheet("""
            background-color: #F9F9F9;  /* 设置标题背景为浅灰色 */
            font-size: 22px;
            font-weight: bold;
            color: #333333;
            padding-left: 10px;
            margin-bottom: 5px;
        """)
        titleLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        cardLayout.addWidget(titleLabel)

        # 内容
        cardLayout.addWidget(content)
        self.vBoxLayout.addWidget(card)

    # ---------------- 登录模块 ----------------
    def createLoginWidget(self):
        """ 创建登录界面并返回其部件 """
        # 这里我们将 `xhs_client` 和 `input_validator` 传递给 LoginWidget
        return LoginMode(self.xhs_client, self.input_validator,self.login_manager, self)

    # ---------------- 发布笔记模块 ----------------

    def createNoteWidget(self):
        """ 创建并返回发布笔记模块 """
        # 这里将 `input_validator` 传递给 NoteWidget
        return NoteWidget(self.input_validator,self.login_manager, self)
    # ---------------- API 操作模块 ----------------
    def createAPIWidget(self):
        """ 创建并返回API操作模块 """
        # 传递 input_validator 作为参数
        return APIWidget(self.xhs_client,self.input_validator,self.login_manager,self)
