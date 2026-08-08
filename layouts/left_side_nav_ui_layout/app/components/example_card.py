"""
 通用组件：ExampleCard 示例卡片（仿 qfluentwidget 的 sample_card 思路）
 圆角白底卡片 + 标题 + 内容区，供各页面复用，避免重复写卡片样式。
"""

from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout


class ExampleCard(QFrame):
    """白色圆角卡片：标题 + 可填充的内容区"""

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background:#ffffff;border-radius:10px;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(
            "font-size:14px;font-weight:600;color:#1f2329;"
        )
        layout.addWidget(self.title_label)

        # 内容区：页面往里 addWidget / addLayout
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(12)
        layout.addLayout(self.content_layout)
