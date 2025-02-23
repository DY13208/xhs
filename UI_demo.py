# coding:utf-8
import sys
import os
from PyQt5.QtCore import Qt, QRect, QUrl
from PyQt5.QtGui import QIcon, QPainter, QImage, QBrush, QColor, QFont
from PyQt5.QtWidgets import QApplication, QFrame, QStackedWidget, QHBoxLayout, QLabel
from qfluentwidgets import (
    NavigationInterface, NavigationItemPosition, NavigationWidget, InfoBar, InfoBarIcon,
    isDarkTheme, qrouter, FluentIcon
)
from qframelesswindow import FramelessWindow, TitleBar
from UI.homeUI import HomeUI  # 使用上面优化后的 homeUI

class Widget(QFrame):
    """ 通用页面组件，用于占位 """
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text.replace(' ', '-'))
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.hBoxLayout.setContentsMargins(0, 32, 0, 0)  # 为标题栏留出顶部空间

class AvatarWidget(NavigationWidget):
    """ 带悬停效果的头像控件 """
    def __init__(self, parent=None):
        super().__init__(isSelectable=False, parent=parent)
        self.avatar = QImage('resource/shoko.png').scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        if self.isPressed:
            painter.setOpacity(0.7)
        if self.isEnter:
            c = 255 if isDarkTheme() else 0
            painter.setBrush(QColor(c, c, c, 10))
            painter.drawRoundedRect(self.rect(), 5, 5)
        painter.setBrush(QBrush(self.avatar))
        painter.translate(8, 6)
        painter.drawEllipse(0, 0, 24, 24)
        painter.translate(-8, -6)
        if not self.isCompacted:
            painter.setPen(Qt.white if isDarkTheme() else Qt.black)
            font = QFont('Segoe UI')
            font.setPixelSize(14)
            painter.setFont(font)
            painter.drawText(QRect(44, 0, 255, 36), Qt.AlignVCenter, '余光')

class CustomTitleBar(TitleBar):
    """ 自定义标题栏，带图标和标题 """
    def __init__(self, parent):
        super().__init__(parent)
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertSpacing(0, 10)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignBottom)
        self.window().windowIconChanged.connect(self.setIcon)
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(2, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignBottom)
        self.titleLabel.setObjectName('titleLabel')
        self.window().windowTitleChanged.connect(self.setTitle)
    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()
    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))

class Window(FramelessWindow):
    """ 主窗口，包含导航和堆叠控件 """
    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))
        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(self, showMenuButton=True, showReturnButton=True)
        self.stackWidget = QStackedWidget(self)
        self.homeInterface = HomeUI()
        self.homeInterface.setObjectName('homeInterface')
        self.chatInterface = Widget('Chat', self)
        self.toolInterface = Widget('Tool', self)
        self.settingInterface = Widget('Setting', self)
        self.initLayout()
        self.initNavigation()
        self.initWindow()
    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)
        self.titleBar.raise_()
        self.navigationInterface.displayModeChanged.connect(self.titleBar.raise_)
    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, 'Home')
        self.addSubInterface(self.chatInterface, FluentIcon.CHAT, 'Chat')
        self.addSubInterface(self.toolInterface, FluentIcon.ERASE_TOOL, 'Tool')
        self.navigationInterface.addSeparator()
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=AvatarWidget(),
            onClick=self.showMessageBox,
            position=NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(self.settingInterface, FluentIcon.SETTING, 'Settings', NavigationItemPosition.BOTTOM)
        qrouter.setDefaultRouteKey(self.stackWidget, self.homeInterface.objectName())
        self.navigationInterface.setExpandWidth(150)
        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.stackWidget.setCurrentIndex(0)
    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('resource/logo.png'))
        self.setWindowTitle('余光')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)
        screen = QApplication.primaryScreen().availableGeometry()
        w, h = screen.width(), screen.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.setQss()
    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP):
        self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text
        )
    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        qss_path = f'resource/{color}/demo.qss'
        if os.path.exists(qss_path):
            with open(qss_path, encoding='utf-8') as f:
                self.setStyleSheet(f.read())
    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)
    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())
        qrouter.push(self.stackWidget, widget.objectName())
    def showMessageBox(self):
        InfoBar.info(
            parent=self,
            title='Message',
            content='This is a modern message box!',
            icon=InfoBarIcon.INFO,
            duration=3000
        )

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
