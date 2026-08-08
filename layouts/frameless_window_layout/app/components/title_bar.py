"""
 通用组件：TitleBar 自绘标题栏（Win11 风格）
 提供：标题文字、最小化/最大化(还原)/关闭按钮、左键拖拽移动、双击最大化。
 拖拽使用 Qt 6 原生 startSystemMove()，自动处理多屏与高 DPI，无需手算坐标。
"""

import os

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from app.common.constants import TITLE_BAR_BG, TITLE_BAR_HEIGHT


class TitleBar(QWidget):
    """无边框窗口的自绘标题栏"""

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setFixedHeight(TITLE_BAR_HEIGHT)
        self.setStyleSheet(f"background:{TITLE_BAR_BG};")

        # 窗口控制图标
        base_dir = os.path.dirname(os.path.abspath(__file__))
        assets = os.path.join(base_dir, "..", "..", "assets")
        self.icon_min = QIcon(os.path.normpath(os.path.join(assets, "icon_min.svg")))
        self.icon_max = QIcon(os.path.normpath(os.path.join(assets, "icon_max.svg")))
        self.icon_restore = QIcon(os.path.normpath(os.path.join(assets, "icon_restore.svg")))
        self.icon_close = QIcon(os.path.normpath(os.path.join(assets, "icon_close.svg")))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 0, 0)
        layout.setSpacing(0)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(
            "color:#ffffff;font-size:13px;background:transparent;"
        )
        layout.addWidget(self.title_label)
        layout.addStretch()

        self.btn_min = self._make_btn(self.icon_min, "最小化")
        self.btn_max = self._make_btn(self.icon_max, "最大化")
        self.btn_close = self._make_btn(self.icon_close, "关闭")
        # 关闭按钮：hover 变红（Win11 惯例）
        self.btn_close.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background: #e81123;
            }
            QPushButton:pressed {
                background: #f1707a;
            }
            """
        )

        layout.addWidget(self.btn_min)
        layout.addWidget(self.btn_max)
        layout.addWidget(self.btn_close)

        self.btn_min.clicked.connect(self._on_minimize)
        self.btn_max.clicked.connect(self._on_toggle_maximize)
        self.btn_close.clicked.connect(self._on_close)

    def _make_btn(self, icon: QIcon, tooltip: str) -> QPushButton:
        btn = QPushButton(self)
        btn.setFixedSize(46, 32)
        btn.setIcon(icon)
        btn.setIconSize(QSize(14, 14))
        btn.setToolTip(tooltip)
        btn.setCursor(Qt.CursorShape.ArrowCursor)
        btn.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.16);
            }
            """
        )
        return btn

    # ---------- 拖拽移动 ----------
    def _win(self) -> QWidget:
        """所属主窗口（QWidget.window() 返回 Optional，统一断言非 None）"""
        w = self.window()
        if w is None:
            raise RuntimeError("TitleBar 尚未挂载到窗口")
        return w

    def mousePressEvent(self, event: QMouseEvent):  # pyright: ignore[reportIncompatibleMethodOverride]
        if event.button() == Qt.MouseButton.LeftButton:
            handle = self._win().windowHandle()
            if handle is not None:
                handle.startSystemMove()  # Qt6 原生系统级拖拽
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent):  # pyright: ignore[reportIncompatibleMethodOverride]
        # 双击标题栏：最大化 / 还原
        w = self._win()
        if w.isMaximized():
            w.showNormal()
        else:
            w.showMaximized()
        event.accept()

    # ---------- 窗口控制 ----------
    def _on_minimize(self):
        self._win().showMinimized()

    def _on_toggle_maximize(self):
        w = self._win()
        if w.isMaximized():
            w.showNormal()
        else:
            w.showMaximized()

    def _on_close(self):
        self._win().close()

    # ---------- 状态同步 ----------
    def setMaximized(self, maximized: bool):
        """由主窗口在 windowStateChanged 时调用：切换最大化/还原图标与提示"""
        if maximized:
            self.btn_max.setIcon(self.icon_restore)
            self.btn_max.setToolTip("还原")
        else:
            self.btn_max.setIcon(self.icon_max)
            self.btn_max.setToolTip("最大化")
