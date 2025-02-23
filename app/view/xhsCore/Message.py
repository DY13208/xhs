# coding:utf-8
from qfluentwidgets import MessageBox
from PyQt5.QtWidgets import (
    QWidget
)

class InputValidator:
    def __init__(self, parent: QWidget):
        self.parent = parent

    def show_empty_input_dialog(self, title: str, content: str):
        """ 显示空值提示框 """
        w = MessageBox(title, content, self.parent)
        w.setClosableOnMaskClicked(True)  # 允许点击遮罩关闭
        if w.exec():  # 显示消息框并处理点击
            print('User acknowledged the message.')
        else:
            print('Message box closed without action.')


