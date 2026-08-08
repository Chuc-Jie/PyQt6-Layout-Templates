"""
 页面层 - 数据管理页 DataPage
 页面自治：本页面的布局、控件与交互逻辑全部在类内实现。
 演示：待办列表——输入、添加、双击删除，均为页面内部逻辑。
"""

from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class DataPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background:#e8f7ef;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("数据管理")
        title.setStyleSheet("font-size:18px;font-weight:600;color:#1f2329;")
        layout.addWidget(title)

        card = QFrame()
        card.setStyleSheet("background:#ffffff;border-radius:10px;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(12)

        tip = QLabel(
            "「数据管理」页面：输入文字并添加为列表项，双击列表项删除\n"
            "所有交互逻辑都在 DataPage 类内实现，主窗口不参与"
        )
        tip.setStyleSheet("font-size:14px;color:#555555;line-height:1.6;")
        card_layout.addWidget(tip)

        # 输入行
        input_row = QHBoxLayout()
        input_row.setSpacing(10)
        self.edit_input = QLineEdit()
        self.edit_input.setPlaceholderText("输入待办事项…")
        self.edit_input.setFixedHeight(34)
        self.edit_input.returnPressed.connect(self._add_item)
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
        self.btn_add.clicked.connect(self._add_item)
        input_row.addWidget(self.edit_input, 1)
        input_row.addWidget(self.btn_add)
        card_layout.addLayout(input_row)

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
        self.list_items.itemDoubleClicked.connect(self._remove_item)
        card_layout.addWidget(self.list_items, 1)

        layout.addWidget(card, 1)

    def _add_item(self):
        text = self.edit_input.text().strip()
        if not text:
            return
        self.list_items.addItem(text)
        self.edit_input.clear()

    def _remove_item(self, item):
        self.list_items.takeItem(self.list_items.row(item))
        if self.list_items.count() == 0:
            QMessageBox.information(self, "提示", "所有待办已清空")
