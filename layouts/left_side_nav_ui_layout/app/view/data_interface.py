"""
 页面逻辑层 - 数据管理页 DataInterface（clock 式 UI 分离）
 UI 由 Ui_DataInterface 定义，本类多重继承后 setupUi 安装界面，再实现业务逻辑。
"""

from PyQt6.QtWidgets import QListWidgetItem, QMessageBox, QWidget

from app.common.signal_bus import signalBus
from app.view.Ui_DataInterface import Ui_DataInterface


class DataInterface(Ui_DataInterface, QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.editInput.returnPressed.connect(self._add_item)
        self.btnAdd.clicked.connect(self._add_item)
        self.listItems.itemDoubleClicked.connect(self._remove_item)

    def _add_item(self):
        text = self.editInput.text().strip()
        if not text:
            return
        self.listItems.addItem(text)
        self.editInput.clear()
        # 信号总线：广播给其他页面（首页接收展示）
        signalBus.data_added.emit(text)

    def _remove_item(self, item: QListWidgetItem):
        self.listItems.takeItem(self.listItems.row(item))
        if self.listItems.count() == 0:
            QMessageBox.information(self, "提示", "所有待办已清空")
            signalBus.data_cleared.emit()
