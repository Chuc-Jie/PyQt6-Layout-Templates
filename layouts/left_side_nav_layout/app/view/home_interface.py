"""
 页面层 - 首页 HomeInterface
 页面自治：布局、控件、交互逻辑全部在类内实现。
 同时演示信号总线接收：数据管理页添加待办时，本页面收到广播并展示。
"""

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from app.common.constants import (
    ACCENT_BLUE,
    ACCENT_BLUE_HOVER,
    ACCENT_BLUE_PRESSED,
    PAGE_BACKGROUNDS,
)
from app.common.signal_bus import signalBus
from app.components.example_card import ExampleCard
from app.view.base_interface import BaseInterface


class HomeInterface(BaseInterface):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(
            "首页",
            "页面自治演示：计数器 + 信号总线接收",
            PAGE_BACKGROUNDS[0],
            parent,
        )

        # 卡片1：计数器（页面内部交互）
        card1 = ExampleCard("计数器（交互逻辑在本页面类内）")
        tip1 = QLabel(
            "点击按钮计数。此页面的控件与状态全部由 HomeInterface 自己管理，\n"
            "主窗口（组装层）不参与任何页面业务逻辑。"
        )
        tip1.setStyleSheet("font-size:13px;color:#555555;line-height:1.6;")
        card1.content_layout.addWidget(tip1)

        self.count = 0
        self.lbl_count = QLabel("点击次数：0")
        self.lbl_count.setStyleSheet(f"font-size:14px;color:{ACCENT_BLUE};font-weight:600;")
        self.btn_click = QPushButton("点我 +1")
        self.btn_click.setFixedSize(110, 36)
        self.btn_click.setStyleSheet(
            f"""
            QPushButton {{
                color: #ffffff;
                background: {ACCENT_BLUE};
                border: none;
                border-radius: 6px;
                outline: none;
            }}
            QPushButton:hover {{ background: {ACCENT_BLUE_HOVER}; }}
            QPushButton:pressed {{ background: {ACCENT_BLUE_PRESSED}; }}
            """
        )
        row = QHBoxLayout()
        row.setSpacing(12)
        row.addWidget(self.lbl_count)
        row.addWidget(self.btn_click)
        row.addStretch()
        card1.content_layout.addLayout(row)
        self.add_card(card1)

        # 卡片2：信号总线接收（跨页面通信演示）
        card2 = ExampleCard("信号总线接收（跨页面通信）")
        tip2 = QLabel(
            "到「数据管理」页面添加一条待办，这里会实时显示最近一条。\n"
            "两个页面互不引用，通过 app/common/signal_bus.py 的全局单例通信。"
        )
        tip2.setStyleSheet("font-size:13px;color:#555555;line-height:1.6;")
        card2.content_layout.addWidget(tip2)
        self.lbl_last = QLabel("最近添加：（暂无）")
        self.lbl_last.setStyleSheet("font-size:13px;color:#888888;")
        card2.content_layout.addWidget(self.lbl_last)
        self.add_card(card2)

        # 页面内部交互：计数器
        self.btn_click.clicked.connect(self._on_click)
        # 信号总线：接收数据管理页广播（连接放在最后，确保自身已完整初始化）
        signalBus.data_added.connect(self._on_data_added)

    def _on_click(self):
        self.count += 1
        self.lbl_count.setText(f"点击次数：{self.count}")

    def _on_data_added(self, text: str):
        # 防御：控件未就绪时忽略（避免 PyQt6 槽内异常崩溃）
        if not hasattr(self, "lbl_last"):
            return
        self.lbl_last.setText(f"最近添加：{text}")
