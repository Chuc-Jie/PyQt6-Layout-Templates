"""
 UI 定义层 - 首页（Ui_HomeInterface）
 只描述界面长什么样：控件创建 + 布局，零业务逻辑（仿 qfluentwidget clock 示例的 pyuic 生成模式）。
 逻辑由 home_interface.py 的 HomeInterface 多重继承本类后实现。
"""

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from app.common.constants import (
    ACCENT_BLUE,
    ACCENT_BLUE_HOVER,
    ACCENT_BLUE_PRESSED,
    PAGE_BACKGROUNDS,
    SUBTITLE_STYLE,
    TITLE_STYLE,
)
from app.components.example_card import ExampleCard


class Ui_HomeInterface(object):
    def setupUi(self, HomeInterface: QWidget):
        HomeInterface.setObjectName("HomeInterface")
        HomeInterface.resize(700, 560)
        HomeInterface.setStyleSheet(f"background:{PAGE_BACKGROUNDS[0]};")

        self.verticalLayout = QVBoxLayout(HomeInterface)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(12)

        # 标题 + 副标题
        self.titleLabel = QLabel(HomeInterface)
        self.titleLabel.setStyleSheet(TITLE_STYLE)
        self.verticalLayout.addWidget(self.titleLabel)

        self.subtitleLabel = QLabel(HomeInterface)
        self.subtitleLabel.setStyleSheet(SUBTITLE_STYLE)
        self.verticalLayout.addWidget(self.subtitleLabel)

        # 卡片1：计数器
        self.counterCard = ExampleCard("计数器（交互逻辑在 Interface 类内）", HomeInterface)
        self.counterTip = QLabel(self.counterCard)
        self.counterTip.setStyleSheet("font-size:13px;color:#555555;line-height:1.6;")
        self.counterCard.content_layout.addWidget(self.counterTip)

        self.countRow = QHBoxLayout()
        self.countRow.setSpacing(12)
        self.lblCount = QLabel(self.counterCard)
        self.lblCount.setStyleSheet(f"font-size:14px;color:{ACCENT_BLUE};font-weight:600;")
        self.btnClick = QPushButton(self.counterCard)
        self.btnClick.setFixedSize(110, 36)
        self.btnClick.setStyleSheet(
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
        self.countRow.addWidget(self.lblCount)
        self.countRow.addWidget(self.btnClick)
        self.countRow.addStretch()
        self.counterCard.content_layout.addLayout(self.countRow)
        self.verticalLayout.addWidget(self.counterCard)

        # 卡片2：信号总线接收
        self.signalCard = ExampleCard("信号总线接收（跨页面通信）", HomeInterface)
        self.signalTip = QLabel(self.signalCard)
        self.signalTip.setStyleSheet("font-size:13px;color:#555555;line-height:1.6;")
        self.signalCard.content_layout.addWidget(self.signalTip)

        self.lblLast = QLabel(self.signalCard)
        self.lblLast.setStyleSheet("font-size:13px;color:#888888;")
        self.signalCard.content_layout.addWidget(self.lblLast)
        self.verticalLayout.addWidget(self.signalCard)

        self.verticalLayout.addStretch()
        self.retranslateUi(HomeInterface)

    def retranslateUi(self, HomeInterface: QWidget):
        self.titleLabel.setText("首页")
        self.subtitleLabel.setText("页面自治演示：计数器 + 信号总线接收")
        self.counterTip.setText(
            "点击按钮计数。本页面拆为两部分：\n"
            "UI 由 Ui_HomeInterface 定义（本文件），逻辑由 HomeInterface 实现（home_interface.py）。"
        )
        self.lblCount.setText("点击次数：0")
        self.btnClick.setText("点我 +1")
        self.signalTip.setText(
            "到「数据管理」页面添加一条待办，这里会实时显示最近一条。\n"
            "两个页面互不引用，通过 app/common/signal_bus.py 的全局单例通信。"
        )
        self.lblLast.setText("最近添加：（暂无）")
