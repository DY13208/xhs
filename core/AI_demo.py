# ai_demo.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from qfluentwidgets import TitleLabel, TextEdit, PushButton

class AIDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI 自动填充示例")
        self.initUI()

    def initUI(self):
        # 使用垂直布局
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 标题，使用 qfluentwidgets 的 TitleLabel（大字号，左对齐）
        title = TitleLabel("AI 自动填充示例", self)
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(title)

        # 多行文本编辑框，用于显示文章内容
        self.textEdit = TextEdit(self)
        self.textEdit.setPlaceholderText("文章内容将在此处显示...")
        layout.addWidget(self.textEdit)

        # 自动填充按钮，点击后填充假数据
        self.fillButton = PushButton("自动填充内容", self)
        self.fillButton.clicked.connect(self.fillContent)
        layout.addWidget(self.fillButton)

        self.resize(600, 400)

    def fillContent(self):
        # 假数据示例
        fake_text = (
            "这是一篇由 AI 自动生成的示例文章。\n\n"
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
            "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
            "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
            "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n\n"
            "以上内容仅为示例，不代表实际 AI 输出。"
        )
        self.textEdit.setPlainText(fake_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = AIDemo()
    demo.show()
    sys.exit(app.exec_())
