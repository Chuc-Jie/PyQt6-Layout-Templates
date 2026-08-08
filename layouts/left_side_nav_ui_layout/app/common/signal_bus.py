"""
 信号总线（仿 qfluentwidget 的 common/signal_bus.py 单例模式）
 页面之间不直接引用对方，通过全局唯一的 signalBus 通信，实现解耦。
 例：数据管理页添加条目 -> emit data_added -> 首页接收并展示。
"""

from PyQt6.QtCore import QObject, pyqtSignal


class SignalBus(QObject):
    """跨页面通信信号集合（全局单例）"""

    # 数据管理页添加了一条待办（参数：条目文本）
    data_added = pyqtSignal(str)
    # 数据管理页清空待办
    data_cleared = pyqtSignal()


# 全局唯一实例：页面里 `from app.common.signal_bus import signalBus` 直接使用
signalBus = SignalBus()
