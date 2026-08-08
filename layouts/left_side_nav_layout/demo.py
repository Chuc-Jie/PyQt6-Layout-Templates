"""
 入口层（对应 qfluentwidget 的 demo.py）
 只负责启动配置，创建组装层窗口 MainWindow 并显示。
 组装与注册逻辑全部在 app/view/main_window.py 中。
"""

import sys

from PyQt6.QtWidgets import QApplication

from app.view.main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
