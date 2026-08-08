"""
 页面基类 BaseInterface（仿 qfluentwidget 的 gallery_interface.py）
 提供统一页面骨架：标题 + 副标题 + 滚动内容区。
 具体页面继承本类，把自身内容填入 self.content_layout 即可，外观自动统一。
"""

from PyQt6.QtWidgets import QFrame, QLabel, QScrollArea, QVBoxLayout, QWidget

from app.common.constants import SUBTITLE_STYLE, TITLE_STYLE


class BaseInterface(QWidget):
    def __init__(self, title: str, subtitle: str, bg_color: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.setStyleSheet(f"background:{bg_color};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title_label = QLabel(title)
        title_label.setStyleSheet(TITLE_STYLE)
        layout.addWidget(title_label)

        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet(SUBTITLE_STYLE)
        layout.addWidget(subtitle_label)

        # 滚动内容区：子类往里填充内容
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
            "QScrollArea > QWidget > QWidget { background: transparent; }"
        )
        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(0, 8, 0, 0)
        self.content_layout.setSpacing(12)
        self.content_layout.addStretch()  # 底部留白，卡片贴顶
        scroll.setWidget(content)
        layout.addWidget(scroll, 1)

    def add_card(self, card: QWidget):
        """子类把卡片/控件加入内容区（插在底部留白之前）"""
        self.content_layout.insertWidget(self.content_layout.count() - 1, card)
