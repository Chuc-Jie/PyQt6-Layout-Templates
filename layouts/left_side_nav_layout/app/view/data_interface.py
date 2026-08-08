"""
 页面层 - 数据管理页 DataInterface
 页面自治：布局、控件、交互逻辑全部在类内实现。
 同时演示信号总线发送：添加待办时广播 signalBus.data_added。
"""

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QListWidget, QMessageBox, QPushButton

from app.common.constants import PAGE_BACKGROUNDS
from app.common.signal_bus import signalBus
from app.components.example_card import ExampleCard
from app.view.base_interface import BaseInterface


class DataInterface(BaseInterface):
    def __init__(self, parent=None):
        super().__init__(
            "数据管理",
            "页面自治演示：待办列表，添加时经信号总线广播",
            PAGE_BACKGROUNDS[1],
            parent,
        )

        card = ExampleCard("待办列表（交互逻辑在本页面类内）")
        tip = QLabel(
            "输入文字并添加为列表项，双击列表项删除。\n"
            "每次添加都会通过 signalBus.data_added 广播，首页会实时收到。"
        )
        tip.setStyleSheet("font-size:13px;color:#555555;line-height:1.6;")
        card.content_layout.addWidget(tip)

        # 输入行
        input_row = QHBoxLayout()
        input_row.setSpacing(10)
        self.edit_input = QLineEdit()
        self.edit_input.setPlaceholderText("输入待办事项…")
        self.edit_input.setFixedHeight(34)
        self.btn_add = QPushButton("添加")
        self.btn_add.setFixedSize(90, 34)
        self.btn_add.setStyleSheet(
            """
            QPushButton {
                color: #ffffff;
                background: #2ea86b;
                border: none;
                border-radius: 6px;
                outline: none;
            }
            QPushButton:hover { background: #268a57; }
            QPushButton:pressed { background: #1f7047; }
            """
        )
        input_row.addWidget(self.edit_input, 1)
        input_row.addWidget(self.btn_add)
        card.content_layout.addLayout(input_row)

        # 列表
        self.list_items = QListWidget()
        self.list_items.setStyleSheet(
            """
            QListWidget {
                border: 1px solid #e2e3e5;
                border-radius: 6px;
                padding: 4px;
                background: #fafbfc;
            }
            QListWidget::item {
                padding: 6px 8px;
                border-radius: 4px;
            }
            QListWidget::item:hover { background: #eef1f4; }
            QListWidget::item:selected { background: #d9e8f7; color: #1f2329; }
            """
        )
        card.content_layout.addWidget(self.list_items)
        self.add_card(card)

        # 页面内部交互
        self.edit_input.returnPressed.connect(self._add_item)
        self.btn_add.clicked.connect(self._add_item)
        self.list_items.itemDoubleClicked.connect(self._remove_item)

    def _add_item(self):
        text = self.edit_input.text().strip()
        if not text:
            return
        self.list_items.addItem(text)
        self.edit_input.clear()
        # 信号总线：广播给其他页面（首页接收展示）
        signalBus.data_added.emit(text)

    def _remove_item(self, item):
        self.list_items.takeItem(self.list_items.row(item))
        if self.list_items.count() == 0:
            QMessageBox.information(self, "提示", "所有待办已清空")
            signalBus.data_cleared.emit()
