"""
 页面逻辑层 - 首页 HomeInterface（clock 式 UI 分离）
 UI 由 Ui_HomeInterface 定义，本类多重继承后 setupUi 安装界面，再实现业务逻辑。
"""

from PyQt6.QtWidgets import QWidget

from app.common.signal_bus import signalBus
from app.view.Ui_HomeInterface import Ui_HomeInterface


class HomeInterface(Ui_HomeInterface, QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.count = 0
        self.btnClick.clicked.connect(self._on_click)
        # 信号总线接收（连接放在最后，确保 setupUi 已创建全部控件）
        signalBus.data_added.connect(self._on_data_added)

    def _on_click(self):
        self.count += 1
        self.lblCount.setText(f"点击次数：{self.count}")

    def _on_data_added(self, text: str):
        # 防御：控件未就绪时忽略（避免 PyQt6 槽内异常崩溃）
        if not hasattr(self, "lblLast"):
            return
        self.lblLast.setText(f"最近添加：{text}")
