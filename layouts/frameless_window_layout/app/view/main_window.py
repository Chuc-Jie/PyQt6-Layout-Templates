"""
 组装层 FramelessWindow（无边框主窗口）
 纯 PyQt6 实现，不依赖任何外部库：
 - FramelessWindowHint + WA_TranslucentBackground 去系统边框、开透明背景
 - 中央圆角容器 + 阴影（最大化时去掉，避免留透明角）
 - 标题栏组件（拖拽/双击最大化/窗口控制按钮）
 - 四边/四角边缘缩放：Qt 6 原生 startSystemResize（自动处理高 DPI）
 - 窗口状态监听：标题栏最大化图标同步、容器圆角切换
"""

from PyQt6.QtCore import QEvent, QPoint, QSize, Qt
from PyQt6.QtGui import QCursor, QMouseEvent
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
)

from app.common.constants import EDGE_MARGIN, WINDOW_BG, WINDOW_RADIUS
from app.components.title_bar import TitleBar
from app.view.home_interface import HomeInterface


class FramelessWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("无边框窗口模板")
        # 无边框 + 透明背景（圆角/阴影的前提）
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # 默认窗口大小 + 最小尺寸约束
        self.resize(900, 600)
        self.setMinimumSize(QSize(600, 400))

        # ========== 中央圆角容器 ==========
        self.container = QFrame()
        self.container.setObjectName("windowContainer")
        root = QVBoxLayout(self.container)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        self.setCentralWidget(self.container)
        self._apply_rounded_style()

        # 容器阴影（透明窗口四周留 12px 边距显示阴影）
        shadow = QGraphicsDropShadowEffect(self.container)
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 0)
        shadow.setColor(Qt.GlobalColor.black)
        self.container.setGraphicsEffect(shadow)
        self.setContentsMargins(12, 12, 12, 12)

        # ========== 标题栏 + 内容区 ==========
        self.title_bar = TitleBar("无边框窗口模板", self.container)
        root.addWidget(self.title_bar)

        self.stacked = QStackedWidget()
        self.homeInterface = HomeInterface()
        self.stacked.addWidget(self.homeInterface)
        root.addWidget(self.stacked, 1)

    # ---------- 窗口状态（用 changeEvent 监听，QWidget 无 windowStateChanged 信号） ----------
    def changeEvent(self, event: QEvent):  # pyright: ignore[reportIncompatibleMethodOverride]
        if event.type() == QEvent.Type.WindowStateChange:
            maximized = bool(self.windowState() & Qt.WindowState.WindowMaximized)
            self._apply_window_state(maximized)
        super().changeEvent(event)

    def _apply_window_state(self, maximized: bool):
        self.title_bar.setMaximized(maximized)
        if maximized:
            # 最大化：占满屏幕，去掉阴影与圆角，边距归零
            self.setContentsMargins(0, 0, 0, 0)
            self.container.setGraphicsEffect(None)
            self.container.setStyleSheet(
                f"#windowContainer {{ background: {WINDOW_BG}; border: none; }}"
            )
        else:
            self.setContentsMargins(12, 12, 12, 12)
            shadow = QGraphicsDropShadowEffect(self.container)
            shadow.setBlurRadius(24)
            shadow.setOffset(0, 0)
            shadow.setColor(Qt.GlobalColor.black)
            self.container.setGraphicsEffect(shadow)
            self._apply_rounded_style()

    def _apply_rounded_style(self):
        self.container.setStyleSheet(
            f"""
            #windowContainer {{
                background: {WINDOW_BG};
                border-radius: {WINDOW_RADIUS}px;
                border: 1px solid rgba(0, 0, 0, 0.08);
            }}
            """
        )

    # ---------- 边缘缩放（Qt 6 原生） ----------
    def mousePressEvent(self, event: QMouseEvent):  # pyright: ignore[reportIncompatibleMethodOverride]
        if event.button() == Qt.MouseButton.LeftButton and not self.isMaximized():
            handle = self.windowHandle()
            if handle is not None:
                edges = self._hit_test(event.position().toPoint())
                if edges:
                    handle.startSystemResize(edges)
                    event.accept()
                    return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):  # pyright: ignore[reportIncompatibleMethodOverride]
        # 边缘 hover 时切换光标形状
        if not self.isMaximized():
            edges = self._hit_test(event.position().toPoint())
            cursor = self._cursor_for(edges)
            if cursor is not None:
                self.setCursor(cursor)
            else:
                self.unsetCursor()
        super().mouseMoveEvent(event)

    def _hit_test(self, pos: QPoint) -> Qt.Edge | None:
        """边缘命中检测：返回命中的边组合（四边/四角），未命中返回 None"""
        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()
        hit: list[Qt.Edge] = []
        if x <= EDGE_MARGIN:
            hit.append(Qt.Edge.LeftEdge)
        if x >= w - EDGE_MARGIN:
            hit.append(Qt.Edge.RightEdge)
        if y <= EDGE_MARGIN:
            hit.append(Qt.Edge.TopEdge)
        if y >= h - EDGE_MARGIN:
            hit.append(Qt.Edge.BottomEdge)
        if not hit:
            return None
        edges = hit[0]
        for e in hit[1:]:
            edges |= e
        return edges

    @staticmethod
    def _cursor_for(edges: Qt.Edge | None) -> QCursor | None:
        """按命中的边返回对应缩放光标；None 表示默认光标"""
        if edges is None:
            return None
        if edges == (Qt.Edge.LeftEdge | Qt.Edge.TopEdge) or edges == (
            Qt.Edge.RightEdge | Qt.Edge.BottomEdge
        ):
            return QCursor(Qt.CursorShape.SizeFDiagCursor)
        if edges == (Qt.Edge.LeftEdge | Qt.Edge.BottomEdge) or edges == (
            Qt.Edge.RightEdge | Qt.Edge.TopEdge
        ):
            return QCursor(Qt.CursorShape.SizeBDiagCursor)
        if edges in (Qt.Edge.LeftEdge, Qt.Edge.RightEdge):
            return QCursor(Qt.CursorShape.SizeHorCursor)
        if edges in (Qt.Edge.TopEdge, Qt.Edge.BottomEdge):
            return QCursor(Qt.CursorShape.SizeVerCursor)
        return None
