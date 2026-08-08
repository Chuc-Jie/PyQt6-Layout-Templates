"""
 组装层 MainWindow（对应 qfluentwidget 的 view/main_window.py）
 职责：导入页面类 -> 通过 addInterface 注册（自动生成导航按钮 + 堆栈映射）-> 绑定折叠。
 页面业务逻辑不在此层，新增页面 = 一行 addInterface。
"""

import os

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.view.data_interface import DataInterface
from app.view.home_interface import HomeInterface
from app.view.setting_interface import SettingInterface


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fluent透明图标按钮适配版（gallery式分层）")
        # 默认窗口大小 + 最小尺寸约束
        self.resize(900, 600)
        self.setMinimumSize(QSize(800, 520))

        # 全局尺寸常量
        self.side_expand_w = 220
        self.side_max_w = 220
        self.func_btn_size = QSize(36, 36)
        self.menu_btn_height = 38
        self.menu_btn_mini_w = 160
        self.menu_btn_max_w = 180
        self.side_collapsed = False

        # 本地SVG图标路径
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "..", "..", "assets", "GriddyIconsSidebar.svg")
        sidebar_icon = QIcon(os.path.normpath(icon_path))

        # ========== 左右分栏 ==========
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(self.splitter)

        # ========== 左侧侧边栏（导航骨架） ==========
        self.side_widget = QWidget()
        self.side_widget.setStyleSheet("background:#f0f2f5;")
        self.side_widget.setMaximumWidth(self.side_max_w)
        self.side_layout = QVBoxLayout(self.side_widget)
        self.side_layout.setContentsMargins(12, 12, 12, 12)
        self.side_layout.setSpacing(10)

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
        self.side_layout.addLayout(side_top_row)

        # 中部菜单区（TOP 导航按钮，注册式自动填充）
        self.menu_area = QVBoxLayout()
        self.menu_area.setSpacing(10)
        self.side_layout.addLayout(self.menu_area)

        # 弹性留白：挤压底部按钮贴底
        self.side_layout.addStretch()

        # 底部区（BOTTOM 导航按钮，对应设置类入口）
        self.bottom_area = QVBoxLayout()
        self.bottom_area.setSpacing(10)
        self.side_layout.addLayout(self.bottom_area)

        # ========== 右侧页面区（顶部行 + QStackedWidget） ==========
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
        right_layout.addWidget(self.stacked, 1)

        # ========== 注册页面（对应 addSubInterface：先存实例属性，再注册） ==========
        self.homeInterface = HomeInterface()
        self.dataInterface = DataInterface()
        self.settingInterface = SettingInterface()
        self.interface_btns = []
        self.addInterface("首页", self.homeInterface)
        self.addInterface("数据管理", self.dataInterface)
        self.addInterface("设置", self.settingInterface, position="bottom")
        self.stacked.setCurrentIndex(0)

        # ========== 分栏与折叠 ==========
        self.splitter.addWidget(self.side_widget)
        self.splitter.addWidget(right_widget)
        self.splitter.setSizes([self.side_expand_w, self.width() - self.side_expand_w])

        self.splitter.splitterMoved.connect(self.refresh_btn_status)
        self.btn_collapse.clicked.connect(self.collapse_by_btn)
        self.btn_expand.clicked.connect(self.expand_by_btn)

    # ---------- 注册式导航（仿 qfluentwidget addSubInterface） ----------
    def addInterface(self, text: str, widget: QWidget, position: str = "top"):
        """注册一个页面：加入 QStackedWidget + 自动生成侧边导航按钮并绑定切换。

        参数:
            text: 导航按钮文字
            widget: 页面实例（QWidget）
            position: 'top' 中部菜单区 / 'bottom' 底部区（蓝色强调样式）
        """
        index = self.stacked.addWidget(widget)
        btn = QPushButton(text)
        btn.setFixedHeight(self.menu_btn_height)
        btn.setMinimumWidth(self.menu_btn_mini_w)
        btn.setMaximumWidth(self.menu_btn_max_w)
        if position == "bottom":
            btn.setStyleSheet(
                """
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
            )
            self.bottom_area.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        else:
            btn.setStyleSheet(
                """
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
            )
            self.menu_area.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        btn.clicked.connect(lambda _, i=index: self.stacked.setCurrentIndex(i))
        self.interface_btns.append(btn)
        return index

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
