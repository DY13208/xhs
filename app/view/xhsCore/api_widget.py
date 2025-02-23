from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QMessageBox, QSizePolicy
)
from qfluentwidgets import (
    LineEdit, PushButton, BodyLabel, TextEdit, InfoBar, SegmentedWidget
)
from .WorkerThread import WorkerThread
from .login_manager import LoginManager

def addRow(v_layout, label_text1, input_widget1=None, label_text2=None, input_widget2=None, button_text=None,
           button_callback=None, fixed_width=150):
    """ 添加一行布局，包含标签、输入框和按钮 """
    row = QHBoxLayout()
    row.setSpacing(10)
    row.setAlignment(Qt.AlignLeft)

    # 标签1
    label1 = BodyLabel(label_text1, v_layout.parentWidget())
    label1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    label1.setStyleSheet("background: none; border: none;")
    row.addWidget(label1)

    if input_widget1:
        input_widget1.setFixedWidth(fixed_width)
        row.addWidget(input_widget1)

    # 标签2 (第二个标签)
    if label_text2:
        label2 = BodyLabel(label_text2, v_layout.parentWidget())
        label2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        label2.setStyleSheet("background: none; border: none;")
        row.addWidget(label2)

    if input_widget2:
        input_widget2.setFixedWidth(fixed_width)
        row.addWidget(input_widget2)

    if button_text:
        btn = PushButton(button_text, v_layout.parentWidget())
        btn.setFixedWidth(160)
        if button_callback and callable(button_callback):
            btn.clicked.connect(button_callback)
        row.addWidget(btn)
    v_layout.addLayout(row)

class APIWidget(QWidget):
    def __init__(self,xhs_client , input_validator,login_manager, parent=None):
        super().__init__(parent)
        self.xhs_client = xhs_client
        self.input_validator = input_validator
        self.login_manager = login_manager
        self.init_ui()

    def init_ui(self):
        """ 初始化UI组件 """
        widget = self
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignLeft)


        # 使用 SegmentedToolWidget 作为分段导航控件
        sw = SegmentedWidget()
        sw.addItem(
            routeKey="fetch",
            text="获取数据",
            onClick=lambda: self.showFetchTab()
        )
        sw.addItem(
            routeKey="operation",
            text="操作功能",
            onClick=lambda: self.showOperationTab()
        )
        sw.setCurrentItem("fetch")
        sw.setFixedWidth(300)  # 固定宽度，不占满全屏
        layout.addWidget(sw, alignment=Qt.AlignLeft)

        # 内容容器：固定宽度，左对齐
        self.apiContentWidget = QWidget(widget)
        self.apiContentLayout = QVBoxLayout(self.apiContentWidget)
        self.apiContentLayout.setSpacing(10)
        self.apiContentLayout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.apiContentWidget, alignment=Qt.AlignLeft)

        # API 调用结果显示区域
        self.apiResultText = TextEdit(widget)
        self.apiResultText.setReadOnly(True)
        self.apiResultText.setPlaceholderText(self.tr("API 调用结果显示在这里..."))
        self.apiResultText.setFixedWidth(600)
        layout.addWidget(self.apiResultText, alignment=Qt.AlignLeft)

        # 加载默认内容：数据获取部分
        self.showFetchTab()

    def showFetchTab(self):
        """ 切换到数据获取分段内容 """
        self.clearApiContent()
        self.apiContentLayout.addWidget(self.createFetchTab())

    def showOperationTab(self):
        """ 切换到操作功能分段内容 """
        self.clearApiContent()
        self.apiContentLayout.addWidget(self.createOperationTab())

    def clearApiContent(self):
        """ 清空 API 内容容器 """
        for i in reversed(range(self.apiContentLayout.count())):
            self.apiContentLayout.itemAt(i).widget().setParent(None)

    def createFetchTab(self) -> QWidget:
        widget = QWidget(self)
        v_layout = QVBoxLayout(widget)
        v_layout.setSpacing(15)
        v_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # 行1：获取笔记信息
        self.fetchNoteId = LineEdit(widget)
        addRow(v_layout, "笔记ID:", self.fetchNoteId, button_text="获取笔记信息",
               button_callback=self.fetch_note_by_id)

        # 行2：获取当前用户信息
        addRow(v_layout, "", None, button_text="获取当前用户信息",
               button_callback=self.fetch_self_info)

        # 行3：获取用户信息
        self.fetchUserId = LineEdit(widget)
        addRow(v_layout, "用户ID:", self.fetchUserId, button_text="获取用户信息",
               button_callback=self.fetch_user_info)

        # 行4：获取主页推荐
        addRow(v_layout, "", None, button_text="获取主页推荐",
               button_callback=self.fetch_home_feed)

        # 行5：搜索笔记
        self.searchKeyword = LineEdit(widget)
        addRow(v_layout, "关键字:", self.searchKeyword, button_text="搜索笔记",
               button_callback=self.fetch_note_by_keyword)

        # 行6：获取用户笔记
        self.fetchUserNotesId = LineEdit(widget)
        addRow(v_layout, "用户ID:", self.fetchUserNotesId, button_text="获取用户笔记",
               button_callback=self.fetch_user_notes)

        # 行7：获取用户收藏
        self.fetchUserCollectId = LineEdit(widget)
        addRow(v_layout, "用户ID:", self.fetchUserCollectId, button_text="获取用户收藏",
               button_callback=self.fetch_user_collect_notes)

        # 行8：获取用户点赞
        self.fetchUserLikeId = LineEdit(widget)
        addRow(v_layout, "用户ID:", self.fetchUserLikeId, button_text="获取用户点赞",
               button_callback=self.fetch_user_like_notes)

        # 行9：获取笔记评论
        self.fetchNoteCommentsId = LineEdit(widget)
        addRow(v_layout, "笔记ID:", self.fetchNoteCommentsId, button_text="获取笔记评论",
               button_callback=self.fetch_note_comments)

        # 行10：获取子评论（笔记ID 和 父评论ID 在同一行内显示）
        row = QHBoxLayout()
        row.setSpacing(10)
        row.setAlignment(Qt.AlignLeft)

        # 标签
        label1 = BodyLabel(self.tr("笔记ID:"), widget)
        label1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        label1.setStyleSheet("background: none; border: none;")
        row.addWidget(label1)

        # 输入框：笔记ID
        self.fetchNoteSubId = LineEdit(widget)
        self.fetchNoteSubId.setFixedWidth(200)
        row.addWidget(self.fetchNoteSubId)

        # 标签
        label2 = BodyLabel(self.tr("父评论ID:"), widget)
        label2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        label2.setStyleSheet("background: none; border: none;")
        row.addWidget(label2)

        # 输入框：父评论ID
        self.fetchParentCommentId = LineEdit(widget)
        self.fetchParentCommentId.setFixedWidth(200)
        row.addWidget(self.fetchParentCommentId)

        # 按钮：获取子评论
        btn = PushButton(self.tr("获取子评论"), widget)
        btn.setFixedWidth(160)
        btn.clicked.connect(self.fetch_note_sub_comments)
        row.addWidget(btn)

        v_layout.addLayout(row)

        # 行11：获取二维码和检查二维码状态
        self.checkQrcodeId = LineEdit(widget)
        self.checkQrcodeCode = LineEdit(widget)
        addRow(v_layout, "二维码ID:", self.checkQrcodeId, button_text="获取二维码",
               button_callback=self.fetch_qrcode)
        addRow(v_layout, "二维码编码:", self.checkQrcodeCode, button_text="检查二维码状态",
               button_callback=self.check_qrcode)

        return widget

    def createOperationTab(self) -> QWidget:
        widget = QWidget(self)
        v_layout = QVBoxLayout(widget)
        v_layout.setSpacing(15)
        v_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # 行1：评论笔记
        self.opCommentNoteId = LineEdit(widget)
        self.opCommentContent = LineEdit(widget)
        addRow(v_layout, "笔记ID:", self.opCommentNoteId, "评论内容:", self.opCommentContent,
               button_text="评论笔记", button_callback=self.op_comment_note)

        # 行2：删除评论
        self.opDelNoteId = LineEdit(widget)
        self.opDelCommentId = LineEdit(widget)
        addRow(v_layout, "笔记ID:", self.opDelNoteId, "评论ID:", self.opDelCommentId,
               button_text="删除评论", button_callback=self.op_delete_comment)

        # 行3：评论用户
        self.opCommentUserNoteId = LineEdit(widget)
        self.opCommentUserContent = LineEdit(widget)
        addRow(v_layout, "笔记ID:", self.opCommentUserNoteId, "评论内容:", self.opCommentUserContent,
               button_text="评论用户", button_callback=self.op_comment_user)

        # 行4：点赞评论
        self.opLikeCommentNoteId = LineEdit(widget)
        self.opLikeCommentId = LineEdit(widget)
        addRow(v_layout, "笔记ID:", self.opLikeCommentNoteId, "评论ID:", self.opLikeCommentId,
               button_text="点赞评论", button_callback=self.op_like_comment)

        # 行5：取消点赞评论
        self.opDislikeCommentId = LineEdit(widget)
        addRow(v_layout, "评论ID:", self.opDislikeCommentId, button_text="取消点赞评论",
               button_callback=self.op_dislike_comment)

        return widget
 # ------------- “操作功能” 页签 API 调用 -------------
    def op_comment_note(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        note_id = self.opCommentNoteId.text().strip()
        comment = self.opCommentContent.text().strip()

        # 空值检查
        if not note_id or not comment:
            # InfoBar.warning(self, self.tr("提示"), self.tr("请输入笔记ID和评论内容"), duration=2000)
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入笔记ID和评论内容"
            )
            return

        try:
            self.worker_thread = WorkerThread(self.xhs_client.comment_note, note_id, comment)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def op_delete_comment(self):

        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        note_id = self.opDelNoteId.text().strip()
        comment_id = self.opDelCommentId.text().strip()

        if not note_id or not comment_id:
            # InfoBar.warning(self, self.tr("提示"), self.tr("请输入笔记ID和评论ID"), duration=2000)
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入笔记ID和评论ID"
            )
            return

        try:
            self.worker_thread = WorkerThread(self.xhs_client.delete_note_comment, note_id, comment_id)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def op_comment_user(self):

        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        note_id = self.opCommentUserNoteId.text().strip()
        content = self.opCommentUserContent.text().strip()

        if not note_id or not content:
            # InfoBar.warning(self, self.tr("提示"), self.tr("请输入笔记ID和评论内容"), duration=2000)
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入笔记ID和评论内容"
            )
            return

        try:
            self.worker_thread = WorkerThread(self.xhs_client.comment_user, note_id, content)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def op_follow_user(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        user_id = self.opFollowUserId.text().strip()

        if not user_id:
            # InfoBar.warning(self, self.tr("提示"), self.tr("请输入用户ID"), duration=2000)
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入用户ID"
            )
            return

        try:
            self.worker_thread = WorkerThread(self.xhs_client.follow_user, user_id)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def op_unfollow_user(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        user_id = self.opFollowUserId.text().strip()

        if not user_id:
            # InfoBar.warning(self, self.tr("提示"), self.tr("请输入用户ID"), duration=2000)
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入用户ID"
            )
            return

        try:
            self.worker_thread = WorkerThread(self.xhs_client.unfollow_user, user_id)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def op_collect_note(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        note_id = self.opCollectNoteId.text().strip()

        if not note_id:
            # InfoBar.warning(self, self.tr("提示"), self.tr("请输入笔记ID"), duration=2000)
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入笔记ID"
            )
            return

        try:
            self.worker_thread = WorkerThread(self.xhs_client.collect_note, note_id)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def op_uncollect_note(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        note_id = self.opCollectNoteId.text().strip()

        if not note_id:
            # InfoBar.warning(self, self.tr("提示"), self.tr("请输入笔记ID"), duration=2000)
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入笔记ID"
            )
            return

        try:
            self.worker_thread = WorkerThread(self.xhs_client.uncollect_note, note_id)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def op_like_note(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        note_id = self.opLikeNoteId.text().strip()

        if not note_id:
            # InfoBar.warning(self, self.tr("提示"), self.tr("请输入笔记ID"), duration=2000)
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入笔记ID"
            )
            return

        try:
            self.worker_thread = WorkerThread(self.xhs_client.like_note, note_id)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def op_dislike_note(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        note_id = self.opLikeNoteId.text().strip()

        if not note_id:
            # InfoBar.warning(self, self.tr("提示"), self.tr("请输入笔记ID"), duration=2000)
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入笔记ID"
            )
            return

        try:
            self.worker_thread = WorkerThread(self.xhs_client.dislike_note, note_id)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def op_like_comment(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        note_id = self.opLikeCommentNoteId.text().strip()
        comment_id = self.opLikeCommentId.text().strip()

        if not note_id or not comment_id:
            # InfoBar.warning(self, self.tr("提示"), self.tr("请输入笔记ID和评论ID"), duration=2000)
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入笔记ID和评论ID"
            )
            return

        try:
            self.worker_thread = WorkerThread(self.xhs_client.like_comment, note_id, comment_id)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def op_dislike_comment(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        comment_id = self.opDislikeCommentId.text().strip()

        if not comment_id:
            # InfoBar.warning(self, self.tr("提示"), self.tr("请输入评论ID"), duration=2000)
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入评论ID"
            )
            return

        try:
            self.worker_thread = WorkerThread(self.xhs_client.dislike_comment, comment_id)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def display_api_result(self, result):
        """ 显示 API 调用结果 """
        self.apiResultText.append(str(result))

    def display_error(self, error_message):
        """ 显示错误信息到 UI """
        self.apiResultText.append(f"错误: {error_message}")
        # QMessageBox.critical(self, "错误", error_message)

    # ------------- “数据获取” 页签 API 调用 -------------
    def fetch_note_by_id(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        note_id = self.fetchNoteId.text().strip()

        if not note_id:
            # InfoBar.warning(self, self.tr("提示"), self.tr("请输入笔记ID"), duration=2000)
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入笔记ID"
            )
            return

        try:
            self.worker_thread = WorkerThread(self.xhs_client.get_note_by_id, note_id)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def fetch_self_info(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        """ 获取当前用户信息 """
        try:

            self.worker_thread = WorkerThread(self.xhs_client.get_self_info)
            self.worker_thread.finished.connect(self.display_user_info)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def display_user_info(self, result):
        print("display_user_info")
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        """ 更新UI显示获取到的用户信息 """

        self.apiResultText.append(f"用户信息: {result}")

    def fetch_user_info(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        user_id = self.fetchUserId.text().strip()

        if not user_id:
            # InfoBar.warning(self, self.tr("提示"), self.tr("请输入用户ID"), duration=2000)
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入用户ID"
            )
            return

        try:
            self.worker_thread = WorkerThread(self.xhs_client.get_user_info, user_id)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def fetch_home_feed(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        try:
            self.worker_thread = WorkerThread(self.xhs_client.get_home_feed)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def fetch_note_by_keyword(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        keyword = self.searchKeyword.text().strip()

        if not keyword:
            # InfoBar.warning(self, self.tr("提示"), self.tr("请输入搜索关键字"), duration=2000)
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入搜索关键字"
            )
            return

        try:
            self.worker_thread = WorkerThread(self.xhs_client.get_note_by_keyword, keyword)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def fetch_user_notes(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        user_id = self.fetchUserNotesId.text().strip()

        if not user_id:
            # InfoBar.warning(self, self.tr("提示"), self.tr("请输入用户ID"), duration=2000)
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入用户ID"
            )
            return

        try:
            self.worker_thread = WorkerThread(self.xhs_client.get_user_notes, user_id)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def fetch_user_collect_notes(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        user_id = self.fetchUserCollectId.text().strip()

        if not user_id:
            # InfoBar.warning(self, self.tr("提示"), self.tr("请输入用户ID"), duration=2000)
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入用户ID"
            )
            return

        try:
            self.worker_thread = WorkerThread(self.xhs_client.get_user_collect_notes, user_id)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def fetch_user_like_notes(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        user_id = self.fetchUserLikeId.text().strip()

        if not user_id:
            # InfoBar.warning(self, self.tr("提示"), self.tr("请输入用户ID"), duration=2000)
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入用户ID"
            )
            return

        try:
            self.worker_thread = WorkerThread(self.xhs_client.get_user_like_notes, user_id)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def fetch_note_comments(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        note_id = self.fetchNoteCommentsId.text().strip()

        if not note_id:
            # InfoBar.warning(self, self.tr("提示"), self.tr("请输入笔记ID"), duration=2000)
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入笔记ID"
            )
            return

        try:
            self.worker_thread = WorkerThread(self.xhs_client.get_note_comments, note_id)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def fetch_note_sub_comments(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        note_id = self.fetchNoteSubId.text().strip()
        parent_id = self.fetchParentCommentId.text().strip()

        if not note_id or not parent_id:
            # InfoBar.warning(self, self.tr("提示"), self.tr("请输入笔记ID和父评论ID"), duration=2000)
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入笔记ID和父评论ID"
            )
            return

        try:
            self.worker_thread = WorkerThread(self.xhs_client.get_note_sub_comments, note_id, parent_id)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def fetch_qrcode(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        try:
            self.worker_thread = WorkerThread(self.xhs_client.get_qrcode)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")

    def check_qrcode(self):
        if not self.login_manager.is_logged_in():  # 检查登录状态
            self.login_manager.show_login_prompt(self)  # 提示用户登录
            return
        qrcode_id = self.checkQrcodeId.text().strip()
        qrcode_code = self.checkQrcodeCode.text().strip()

        if not qrcode_id or not qrcode_code:
            # InfoBar.warning(self, self.tr("提示"), self.tr("请输入二维码ID和二维码编码"), duration=2000)
            self.input_validator.show_empty_input_dialog(
                title='警告',
                content="请输入二维码ID和二维码编码"
            )
            return

        try:
            self.worker_thread = WorkerThread(self.xhs_client.check_qrcode, qrcode_id, qrcode_code)
            self.worker_thread.finished.connect(self.display_api_result)
            self.worker_thread.error_occurred.connect(self.display_error)
            self.worker_thread.start()
        except Exception as e:
            self.display_error(f"启动线程时出现错误: {str(e)}")