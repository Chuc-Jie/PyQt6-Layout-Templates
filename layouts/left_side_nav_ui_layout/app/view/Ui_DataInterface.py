"""
 UI 定义层 - 数据管理页（Ui_DataInterface）
 只描述界面长什么样，零业务逻辑；逻辑由 data_interface.py 的 DataInterface 实现。
"""

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QListWidget, QPushButton, QVBoxLayout, QWidget

from app.common.constants import PAGE_BACKGROUNDS, SUBTITLE_STYLE, TITLE_STYLE
from app.components.example_card import ExampleCard


class Ui_DataInterface(object):
    def setupUi(self, DataInterface: QWidget):
        DataInterface.setObjectName("DataInterface")
        DataInterface.resize(700, 560)
        DataInterface.setStyleSheet(f"background:{PAGE_BACKGROUNDS[1]};")

        self.verticalLayout = QVBoxLayout(DataInterface)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(12)

        # 标题 + 副标题
        self.titleLabel = QLabel(DataInterface)
        self.titleLabel.setStyleSheet(TITLE_STYLE)
        self.verticalLayout.addWidget(self.titleLabel)

        self.subtitleLabel = QLabel(DataInterface)
        self.subtitleLabel.setStyleSheet(SUBTITLE_STYLE)
        self.verticalLayout.addWidget(self.subtitleLabel)

        # 待办卡片
        self.dataCard = ExampleCard("待办列表（交互逻辑在 Interface 类内）", DataInterface)
        self.tipLabel = QLabel(self.dataCard)
        self.tipLabel.setStyleSheet("font-size:13px;color:#555555;line-height:1.6;")
        self.dataCard.content_layout.addWidget(self.tipLabel)

        # 输入行
        self.inputRow = QHBoxLayout()
        self.inputRow.setSpacing(10)
        self.editInput = QLineEdit(self.dataCard)
        self.editInput.setFixedHeight(34)
        self.btnAdd = QPushButton(self.dataCard)
        self.btnAdd.setFixedSize(90, 34)
        self.btnAdd.setStyleSheet(
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
        self.inputRow.addWidget(self.editInput, 1)
        self.inputRow.addWidget(self.btnAdd)
        self.dataCard.content_layout.addLayout(self.inputRow)

        # 列表
        self.listItems = QListWidget(self.dataCard)
        self.listItems.setStyleSheet(
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
        self.dataCard.content_layout.addWidget(self.listItems)
        self.verticalLayout.addWidget(self.dataCard)

        self.verticalLayout.addStretch()
        self.retranslateUi(DataInterface)

    def retranslateUi(self, DataInterface: QWidget):
        self.titleLabel.setText("数据管理")
        self.subtitleLabel.setText("页面自治演示：待办列表，添加时经信号总线广播")
        self.tipLabel.setText(
            "输入文字并添加为列表项，双击列表项删除。\n"
            "每次添加都会通过 signalBus.data_added 广播，首页会实时收到。"
        )
        self.editInput.setPlaceholderText("输入待办事项…")
        self.btnAdd.setText("添加")
