"""
 UI 定义层 - 首页（Ui_HomeInterface）
 只描述界面长什么样，零业务逻辑；逻辑由 home_interface.py 实现。
"""

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from app.common.constants import (
    ACCENT_BLUE,
    ACCENT_BLUE_HOVER,
    ACCENT_BLUE_PRESSED,
    SUBTITLE_STYLE,
    TITLE_STYLE,
)
from app.components.example_card import ExampleCard


class Ui_HomeInterface(object):
    def setupUi(self, HomeInterface: QWidget):
        HomeInterface.setObjectName("HomeInterface")
        HomeInterface.resize(760, 520)

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

        # 卡片1：操作说明
        self.tipCard = ExampleCard("操作说明（纯 PyQt6 无边框窗口）", HomeInterface)
        self.tipLabel = QLabel(self.tipCard)
        self.tipLabel.setStyleSheet("font-size:13px;color:#555555;line-height:1.8;")
        self.tipCard.content_layout.addWidget(self.tipLabel)
        self.verticalLayout.addWidget(self.tipCard)

        # 卡片2：窗口状态检测
        self.stateCard = ExampleCard("窗口状态检测", HomeInterface)
        self.lblState = QLabel(self.stateCard)
        self.lblState.setStyleSheet(
            f"font-size:14px;color:{ACCENT_BLUE};font-weight:600;"
        )
        self.btnRefresh = QPushButton("刷新状态", self.stateCard)
        self.btnRefresh.setFixedSize(110, 34)
        self.btnRefresh.setStyleSheet(
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
        state_row = QHBoxLayout()
        state_row.setSpacing(12)
        state_row.addWidget(self.lblState)
        state_row.addWidget(self.btnRefresh)
        state_row.addStretch()
        self.stateCard.content_layout.addLayout(state_row)
        self.verticalLayout.addWidget(self.stateCard)

        # 卡片3：计数器（页面内部交互演示）
        self.countCard = ExampleCard("计数器（页面内部交互）", HomeInterface)
        self.lblCount = QLabel(self.countCard)
        self.lblCount.setStyleSheet(
            f"font-size:14px;color:{ACCENT_BLUE};font-weight:600;"
        )
        self.btnClick = QPushButton("点我 +1", self.countCard)
        self.btnClick.setFixedSize(110, 34)
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
        count_row = QHBoxLayout()
        count_row.setSpacing(12)
        count_row.addWidget(self.lblCount)
        count_row.addWidget(self.btnClick)
        count_row.addStretch()
        self.countCard.content_layout.addLayout(count_row)
        self.verticalLayout.addWidget(self.countCard)

        self.verticalLayout.addStretch()
        self.retranslateUi(HomeInterface)

    def retranslateUi(self, HomeInterface: QWidget):
        self.titleLabel.setText("无边框窗口模板")
        self.subtitleLabel.setText("纯 PyQt6 实现：无边框 + 自绘标题栏 + 边缘缩放 + 圆角")
        self.tipLabel.setText(
            "・标题栏左键按住拖拽移动窗口（Qt6 原生 startSystemMove）\n"
            "・双击标题栏最大化/还原\n"
            "・窗口四边/四角拖动缩放（Qt6 原生 startSystemResize，自动处理高 DPI）\n"
            "・最大化时自动去掉圆角，避免留出透明角"
        )
        self.lblState.setText("窗口状态：（点击刷新查看）")
        self.btnRefresh.setText("刷新状态")
        self.lblCount.setText("点击次数：0")
        self.btnClick.setText("点我 +1")
