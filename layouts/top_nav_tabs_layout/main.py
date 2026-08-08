"""
  UI布局预设 - 顶部导航栏 + 多标签页内容区布局
"""

import os
import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class TopNavTabsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("顶部导航+多标签页布局模板")
        # 默认窗口大小 + 最小尺寸约束
        self.resize(900, 600)
        self.setMinimumSize(QSize(800, 520))

        # 全局尺寸常量
        self.nav_btn_height = 34
        self.nav_btn_min_w = 88
        self.add_btn_size = QSize(32, 32)
        self.tab_min_w = 120
        self.tab_max_w = 240
        # 模块导航（按钮文字即模块名，也是标签页标题）
        self.module_names = ["首页", "工作台", "数据管理", "关于"]
        # 标签页占位背景色（循环取用）
        self.page_colors = ["#eef4ff", "#e8f7ef", "#fff7e8", "#fdeeee", "#f0eefe"]

        # 本地SVG图标路径（适配当前模板子目录结构）
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.add_icon_path = os.path.join(base_dir, "assets", "GriddyIconsAdd.svg")
        add_icon = QIcon(self.add_icon_path)

        # ========== 中央整体：顶部导航栏 + 内容区 ==========
        central = QWidget()
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        self.setCentralWidget(central)

        # ========== 顶部导航栏（深色） ==========
        nav_bar = QWidget()
        nav_bar.setStyleSheet("background:#1f2329;")
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(16, 8, 16, 8)
        nav_layout.setSpacing(8)

        nav_title = QLabel("顶部导航模板")
        nav_title.setStyleSheet(
            "color:#ffffff;font-size:15px;font-weight:600;padding-right:10px;"
        )
        nav_layout.addWidget(nav_title)

        self.nav_btns = []
        for name in self.module_names:
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.setFixedHeight(self.nav_btn_height)
            btn.setMinimumWidth(self.nav_btn_min_w)
            btn.setStyleSheet(
                """
                QPushButton {
                    color: #c8ccd4;
                    background: transparent;
                    border: none;
                    border-radius: 6px;
                    padding: 0 14px;
                    outline: none;
                }
                QPushButton:hover {
                    background: #2f343c;
                    color: #ffffff;
                }
                QPushButton:checked {
                    background: #4070f4;
                    color: #ffffff;
                }
                """
            )
            btn.clicked.connect(lambda _, n=name: self.open_module(n))
            self.nav_btns.append(btn)
            nav_layout.addWidget(btn)

        nav_layout.addStretch()

        # 新建标签按钮（+）
        btn_add_tab = QPushButton()
        btn_add_tab.setFixedSize(self.add_btn_size)
        btn_add_tab.setIcon(add_icon)
        btn_add_tab.setIconSize(QSize(18, 18))
        btn_add_tab.setToolTip("新建空白标签页")
        btn_add_tab.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #2f343c;
            }
            QPushButton:pressed {
                background: #3a4048;
            }
            """
        )
        btn_add_tab.clicked.connect(self.add_blank_tab)
        nav_layout.addWidget(btn_add_tab)

        # ========== 多标签页内容区 ==========
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setMinimumWidth(200)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.sync_nav_highlight)
        self.tab_widget.setStyleSheet(
            """
            QTabWidget::pane {
                border: none;
                background: #ffffff;
            }
            QTabBar::tab {
                min-width: 120px;
                max-width: 240px;
                padding: 6px 14px;
                color: #555555;
                background: #f2f3f5;
                border: none;
                border-right: 1px solid #e2e3e5;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:hover {
                background: #e8e9eb;
            }
            QTabBar::tab:selected {
                color: #1f2329;
                background: #ffffff;
            }
            """
        )
        root_layout.addWidget(nav_bar)
        root_layout.addWidget(self.tab_widget, 1)

        # 初始打开首页模块
        self.open_module(self.module_names[0])

    # ---------- 标签页构建 ----------
    def _build_tab_page(self, module_name, bg_color):
        """构建一个占位标签页：顶部模块标题 + 白色占位卡片。"""
        page = QWidget()
        page.setStyleSheet(f"background:{bg_color};")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel(module_name)
        title.setStyleSheet("font-size:18px;font-weight:600;color:#1f2329;")
        layout.addWidget(title)

        card = QFrame()
        card.setStyleSheet("background:#ffffff;border-radius:10px;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        tip = QLabel(
            f"这里是「{module_name}」模块的占位内容区\n"
            "可在 _build_tab_page() 中替换为业务界面\n\n"
            "顶部导航按钮 = 打开/切换模块页\n"
            "右上角 + 按钮 = 新建空白标签\n"
            "标签可拖动排序、点击关闭"
        )
        tip.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tip.setStyleSheet("font-size:14px;color:#555555;line-height:1.6;")
        card_layout.addWidget(tip)
        layout.addWidget(card, 1)

        return page

    # ---------- 标签页操作 ----------
    def open_module(self, module_name):
        """打开模块页：同名标签已存在则切换，否则新建。"""
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == module_name:
                self.tab_widget.setCurrentIndex(i)
                return
        bg = self.page_colors[self.tab_widget.count() % len(self.page_colors)]
        page = self._build_tab_page(module_name, bg)
        self.tab_widget.addTab(page, module_name)
        self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)

    def add_blank_tab(self):
        """新建一个不关联导航按钮的空白标签页。"""
        index = self.tab_widget.count() + 1
        bg = self.page_colors[self.tab_widget.count() % len(self.page_colors)]
        page = self._build_tab_page(f"新标签 {index}", bg)
        self.tab_widget.addTab(page, f"新标签 {index}")
        self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)

    def close_tab(self, index):
        """关闭指定标签；全部关闭后自动补一个首页，避免空内容区。"""
        self.tab_widget.removeTab(index)
        if self.tab_widget.count() == 0:
            self.open_module(self.module_names[0])

    # ---------- 状态同步 ----------
    def sync_nav_highlight(self, current_index):
        """切换标签时，同步高亮对应顶部导航按钮（空白标签不高亮任何按钮）。"""
        if current_index < 0:
            return
        tab_name = self.tab_widget.tabText(current_index)
        for btn, name in zip(self.nav_btns, self.module_names):
            btn.setChecked(name == tab_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TopNavTabsWindow()
    window.show()
    sys.exit(app.exec())
