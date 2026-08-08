"""
 页面层 - 首页 HomePage
 页面自治：本页面的布局、控件与交互逻辑全部在类内实现，不依赖主窗口。
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background:#eef4ff;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("首页")
        title.setStyleSheet("font-size:18px;font-weight:600;color:#1f2329;")
        layout.addWidget(title)

        card = QFrame()
        card.setStyleSheet("background:#ffffff;border-radius:10px;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(12)

        tip = QLabel(
            "这是「首页」页面：控件与交互逻辑都在 HomePage 类内实现\n"
            "下方的计数器演示页面自治——状态与逻辑不依赖主窗口\n"
            "主窗口（main.py）只负责把本页面注册进 QStackedWidget"
        )
        tip.setAlignment(Qt.AlignmentFlag.AlignLeft)
        tip.setStyleSheet("font-size:14px;color:#555555;line-height:1.6;")
        card_layout.addWidget(tip)

        # 页面内部交互演示：计数器（逻辑在本类内）
        self.count = 0
        self.lbl_count = QLabel("点击次数：0")
        self.lbl_count.setStyleSheet("font-size:14px;color:#4070f4;font-weight:600;")
        self.btn_click = QPushButton("点我 +1")
        self.btn_click.setFixedSize(110, 36)
        self.btn_click.setStyleSheet(
            """
            QPushButton {
                color: #ffffff;
                background: #4070f4;
                border: none;
                border-radius: 6px;
                outline: none;
            }
            QPushButton:hover { background: #2b5cd8; }
            QPushButton:pressed { background: #224bb8; }
            """
        )
        self.btn_click.clicked.connect(self._on_click)

        row = QHBoxLayout()
        row.setSpacing(12)
        row.addWidget(self.lbl_count)
        row.addWidget(self.btn_click)
        row.addStretch()
        card_layout.addLayout(row)

        layout.addWidget(card, 1)

    def _on_click(self):
        self.count += 1
        self.lbl_count.setText(f"点击次数：{self.count}")
