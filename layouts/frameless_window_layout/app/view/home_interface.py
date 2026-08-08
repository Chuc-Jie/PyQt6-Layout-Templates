"""
 页面逻辑层 - 首页 HomeInterface（Ui/Interface 分离）
 UI 由 Ui_HomeInterface 定义，本类多重继承后 setupUi 安装界面，再实现业务逻辑。
"""

from PyQt6.QtWidgets import QWidget

from app.view.Ui_HomeInterface import Ui_HomeInterface


class HomeInterface(Ui_HomeInterface, QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.count = 0
        self.btnRefresh.clicked.connect(self._refresh_state)
        self.btnClick.clicked.connect(self._on_click)

    def _refresh_state(self):
        w = self.window()
        if w is None:
            return
        if w.isMaximized():
            state = "最大化"
        elif w.isMinimized():
            state = "最小化"
        else:
            state = "正常"
        geo = w.geometry()
        self.lblState.setText(f"窗口状态：{state}  尺寸：{geo.width()}×{geo.height()}")

    def _on_click(self):
        self.count += 1
        self.lblCount.setText(f"点击次数：{self.count}")
