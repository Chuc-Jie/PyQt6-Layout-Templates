"""
  UI布局预设 - 左侧常驻导航 + 右侧 QStackedWidget 多页面
  分层架构（参考 qfluentwidget 的做法）：
  - 页面层 pages/：每个页面一个 QWidget 类，布局与交互逻辑在页面内部自治实现
  - 组装层 main.py：导入页面类 -> 实例化 -> 注册进 QStackedWidget -> 绑定侧边栏导航
  main.py 只负责组装与导航切换，不掺入页面业务逻辑。
"""

import os
import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from pages.data_page import DataPage
from pages.home_page import HomePage
from pages.setting_page import SettingPage


class SideBarWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fluent透明图标按钮适配版（分层多页面）")
        # 默认窗口大小 + 最小/最大窗口尺寸约束
        self.resize(900, 600)
        self.setMinimumSize(QSize(800, 520))
        # self.setMaximumSize(QSize(1400, 900)) 备用

        # 全局尺寸常量
        self.side_expand_w = 220
        self.side_max_w = 220
        self.func_btn_size = QSize(36, 36)
        self.menu_btn_height = 38
        self.menu_btn_mini_w = 160
        self.menu_btn_max_w = 180
        self.side_collapsed = False

        # 本地SVG图标路径（适配当前模板子目录结构）
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.icon_path = os.path.join(base_dir, "assets", "GriddyIconsSidebar.svg")
        sidebar_icon = QIcon(self.icon_path)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(self.splitter)

        # ========== 左侧侧边栏区域（导航） ==========
        self.side_widget = QWidget()
        self.side_widget.setStyleSheet("background:#f0f2f5;")
        self.side_widget.setMaximumWidth(self.side_max_w)
        side_layout = QVBoxLayout(self.side_widget)
        side_layout.setContentsMargins(12, 12, 12, 12)
        side_layout.setSpacing(10)

        # 顶部标题行
        side_top_row = QHBoxLayout()
        side_top_row.setSpacing(8)
        side_title = QLabel("侧边菜单栏")
        side_title.setStyleSheet("font-size:15px;font-weight:500;")

        fluent_icon_btn_style = """
        QPushButton {
            background-color: transparent;
            border: none;
            border-radius: 18px;
        }
        QPushButton:hover {
            background-color: rgba(0, 0, 0, 9);
        }
        QPushButton:pressed {
            background-color: rgba(0, 0, 0, 6);
        }
        QPushButton:disabled {
            background-color: transparent;
        }
        """
        self.btn_collapse = QPushButton()
        self.btn_collapse.setFixedSize(self.func_btn_size)
        self.btn_collapse.setIcon(sidebar_icon)
        self.btn_collapse.setIconSize(QSize(22, 22))
        self.btn_collapse.setStyleSheet(fluent_icon_btn_style)
        side_top_row.addWidget(side_title)
        side_top_row.addStretch()
        side_top_row.addWidget(self.btn_collapse)
        side_layout.addLayout(side_top_row)

        # 中间菜单按钮组：每个按钮对应右侧一个页面索引
        menu_btn_style = """
        QPushButton {
            color: black;
            background: rgba(255, 255, 255, 0.7);
            border: 1px solid rgba(0, 0, 0, 0.073);
            border-bottom: 1px solid rgba(0, 0, 0, 0.183);
            border-radius: 5px;
            padding: 5px 12px 6px 12px;
            outline: none;
        }
        QPushButton:hover {
            background: rgba(249, 249, 249, 0.5);
        }
        QPushButton:pressed {
            color: rgba(0, 0, 0, 0.63);
            background: rgba(249, 249, 249, 0.3);
            border-bottom: 1px solid rgba(0, 0, 0, 0.073);
        }
        """
        self.menu_btns = []
        for name, index in zip(["首页", "数据管理"], [0, 1]):
            btn = QPushButton(name)
            btn.setFixedHeight(self.menu_btn_height)
            btn.setMinimumWidth(self.menu_btn_mini_w)
            btn.setMaximumWidth(self.menu_btn_max_w)
            btn.setStyleSheet(menu_btn_style)
            btn.clicked.connect(lambda _, i=index: self.stacked.setCurrentIndex(i))
            self.menu_btns.append(btn)
            side_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        # 核心：弹性空白空间，挤压下方按钮贴底
        side_layout.addStretch()

        # 底部独立设置按钮（深色专属样式区分普通导航，对应设置页）
        setting_btn_style = """
        QPushButton {
            color: #fff;
            background: #4070f4;
            border-radius:5px;
            padding: 5px 12px 6px 12px;
            outline: none;
        }
        QPushButton:hover {
            background:#2b5cd8;
        }
        QPushButton:pressed {
            background:#224bb8;
        }
        """
        bottom_setting_btn = QPushButton("设置")
        bottom_setting_btn.setFixedHeight(self.menu_btn_height)
        bottom_setting_btn.setMinimumWidth(self.menu_btn_mini_w)
        bottom_setting_btn.setMaximumWidth(self.menu_btn_max_w)
        bottom_setting_btn.setStyleSheet(setting_btn_style)
        bottom_setting_btn.clicked.connect(lambda: self.stacked.setCurrentIndex(2))
        side_layout.addWidget(
            bottom_setting_btn, alignment=Qt.AlignmentFlag.AlignHCenter
        )

        # ========== 右侧页面区（顶部行 + QStackedWidget） ==========
        # 组装：导入的页面实例注册进堆栈（对应 qfluentwidget 的 addSubInterface 效果）
        right_widget = QWidget()
        right_widget.setStyleSheet("background:#ffffff;")
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # 折叠侧边栏后，右上角出现展开按钮
        self.btn_expand = QPushButton()
        self.btn_expand.setFixedSize(self.func_btn_size)
        self.btn_expand.setIcon(sidebar_icon)
        self.btn_expand.setIconSize(QSize(22, 22))
        self.btn_expand.setStyleSheet(fluent_icon_btn_style)
        self.btn_expand.hide()
        expand_row = QHBoxLayout()
        expand_row.setContentsMargins(8, 8, 8, 0)
        expand_row.addWidget(self.btn_expand)
        expand_row.addStretch()
        right_layout.addLayout(expand_row)

        self.stacked = QStackedWidget()
        self.home_page = HomePage()
        self.data_page = DataPage()
        self.setting_page = SettingPage()
        self.stacked.addWidget(self.home_page)
        self.stacked.addWidget(self.data_page)
        self.stacked.addWidget(self.setting_page)
        right_layout.addWidget(self.stacked, 1)

        self.splitter.addWidget(self.side_widget)
        self.splitter.addWidget(right_widget)
        self.splitter.setSizes([self.side_expand_w, self.width() - self.side_expand_w])

        self.splitter.splitterMoved.connect(self.refresh_btn_status)
        self.btn_collapse.clicked.connect(self.collapse_by_btn)
        self.btn_expand.clicked.connect(self.expand_by_btn)

    # ---------- 侧边栏折叠/展开 ----------
    def refresh_btn_status(self, *_):
        side_w = self.splitter.sizes()[0]
        now_collapsed = side_w <= 0
        if now_collapsed == self.side_collapsed:
            return
        self.side_collapsed = now_collapsed
        if now_collapsed:
            self.btn_collapse.hide()
            self.btn_expand.show()
        else:
            self.btn_collapse.show()
            self.btn_expand.hide()

    def collapse_by_btn(self):
        self.splitter.setSizes([0, self.splitter.width()])
        self.btn_collapse.hide()
        self.btn_expand.show()

    def expand_by_btn(self):
        total_w = self.splitter.width()
        self.splitter.setSizes([self.side_expand_w, total_w - self.side_expand_w])
        self.btn_collapse.show()
        self.btn_expand.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SideBarWindow()
    window.show()
    sys.exit(app.exec())
