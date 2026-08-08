"""
 启动入口：创建无边框主窗口并显示。
"""

import sys

from PyQt6.QtWidgets import QApplication

from app.view.main_window import FramelessWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = FramelessWindow()
    w.show()
    sys.exit(app.exec())
