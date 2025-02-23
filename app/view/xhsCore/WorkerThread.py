from PyQt5.QtCore import QThread, pyqtSignal

class WorkerThread(QThread):
    finished = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, func, *args, parent=None):
        super().__init__(parent)
        self.func = func
        self.args = args

    def run(self):
        try:
            # 执行实际的操作
            result = self.func(*self.args)
            # 如果操作成功，则触发 finished 信号
            self.finished.emit(str(result))
        except Exception as e:
            # 捕获异常并传递给主线程
            self.error_occurred.emit(f"错误: {str(e)}")
