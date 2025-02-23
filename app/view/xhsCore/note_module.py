# note_widget.py
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QTextEdit, QFileDialog
)
from qfluentwidgets import (
    LineEdit, PushButton, FluentIcon, BodyLabel, TextEdit
)

from app.view.xhsCore.login_manager import LoginManager


class NoteWidget(QWidget):
    def __init__(self, input_validator,login_manager, parent=None):
        super().__init__(parent)
        self.input_validator = input_validator
        self.login_manager = login_manager
        self.init_ui()

    def init_ui(self):
        """ 初始化UI组件 """
        widget = self
        v_layout = QVBoxLayout(widget)
        v_layout.setSpacing(15)
        v_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        def addRow(label_text, input_widget=None, button_text=None, button_callback=None):
            """ 添加标签、输入框和按钮的一行布局 """
            row = QHBoxLayout()
            row.setSpacing(10)
            row.setAlignment(Qt.AlignLeft)

            # 标签
            label = BodyLabel(self.tr(label_text), widget)
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            label.setStyleSheet("background: none; border: none;")  # 移除背景和边框
            row.addWidget(label)

            if input_widget:
                input_widget.setFixedWidth(300)
                row.addWidget(input_widget)

            if button_text:
                btn = PushButton(self.tr(button_text), widget)
                btn.setFixedWidth(160)
                btn.clicked.connect(button_callback)
                row.addWidget(btn)

            v_layout.addLayout(row)

        # 行1：笔记标题输入
        self.titleLineEdit = LineEdit(widget)
        addRow("标题：", self.titleLineEdit)

        # 行2：笔记描述输入
        self.descTextEdit = TextEdit(widget)
        self.descTextEdit.setFixedHeight(100)
        addRow("描述：", self.descTextEdit)

        # 行3：图片路径输入 + 选择图片按钮
        self.imageLineEdit = LineEdit(widget)
        addRow("图片路径：", self.imageLineEdit, "选择图片", self.select_image)

        # 行4：发布笔记按钮
        row = QHBoxLayout()
        row.setAlignment(Qt.AlignLeft)
        self.publishNoteButton = PushButton(self.tr("发布笔记"), widget)
        self.publishNoteButton.setIcon(FluentIcon.SEND)
        self.publishNoteButton.setFixedWidth(160)
        self.publishNoteButton.clicked.connect(self.publish_note)  # 绑定发布笔记函数
        row.addWidget(self.publishNoteButton)

        # 自动填充笔记按钮
        self.autoFillButton = PushButton(self.tr("自动填充笔记"), widget)
        self.autoFillButton.setFixedWidth(160)
        self.autoFillButton.clicked.connect(self.auto_fill_note)  # 绑定自动填充笔记函数
        row.addWidget(self.autoFillButton)

        v_layout.addLayout(row)

    def publish_note(self):
        """ 发布笔记 """
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        # 获取输入框内容
        title = self.titleLineEdit.text().strip()
        description = self.descTextEdit.toPlainText().strip()

        # 空值检查
        if not title or not description:
            self.input_validator.show_empty_input_dialog(
                title='输入错误',
                content="标题和描述不能为空！"
            )
            return  # 如果有空值，返回不执行发布操作

        # 如果没有空值，执行发布操作
        # 在这里你可以加入发布笔记的代码，例如：
        # result = self.xhs_client.publish_note(title, description)
        # self.display_publish_result(result)

        self.input_validator.show_empty_input_dialog(
            title='发布成功',
            content="笔记已成功发布"
        )

    def auto_fill_note(self):
        """ 自动填充笔记标题和描述 """
        # 自动填充标题和描述
        self.titleLineEdit.setText("自动生成的标题")
        self.descTextEdit.setText("这是自动填充的描述内容。")
        self.imageLineEdit.setText("这是自动填充的图片路径")
        # 可选：显示提示信息
        # self.input_validator.show_empty_input_dialog(
        #     title='自动填充成功',
        #     content="标题和描述已成功自动填充！"
        # )

    def select_image(self):
        """ 选择图片并设置路径 """
        if not LoginManager().is_logged_in():  # 检查登录状态
            LoginManager.show_login_prompt(self)  # 提示用户登录
            return
        file_path, _ = QFileDialog.getOpenFileName(self, self.tr("选择图片"), "", self.tr("Image Files (*.png *.jpg *.jpeg *.bmp)"))
        if file_path:
            self.imageLineEdit.setText(file_path)
