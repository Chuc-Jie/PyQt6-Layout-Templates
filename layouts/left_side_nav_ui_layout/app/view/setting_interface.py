"""
 页面逻辑层 - 设置页 SettingInterface（clock 式 UI 分离）
 UI 由 Ui_SettingInterface 定义，本类多重继承后 setupUi 安装界面，再实现业务逻辑。
"""

from PyQt6.QtWidgets import QWidget

from app.view.Ui_SettingInterface import Ui_SettingInterface


class SettingInterface(Ui_SettingInterface, QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent=parent)
        self.setupUi(self)

        for cb in (self.cbAutoSave, self.cbNotify, self.cbDark):
            cb.toggled.connect(self._on_option_changed)
        self.btnReset.clicked.connect(self._reset_defaults)

        # 初始状态：触发 toggled 信号时 setupUi 已创建全部控件
        self.cbAutoSave.setChecked(True)

    def _on_option_changed(self):
        # 防御：控件尚未初始化完成时直接忽略（避免槽内异常）
        if not hasattr(self, "lblStatus"):
            return
        parts: list[str] = []
        if self.cbAutoSave.isChecked():
            parts.append("自动保存")
        if self.cbNotify.isChecked():
            parts.append("通知")
        if self.cbDark.isChecked():
            parts.append("深色")
        self.lblStatus.setText(
            "当前状态：" + ("、".join(parts) if parts else "全部关闭")
        )

    def _reset_defaults(self):
        self.cbAutoSave.setChecked(True)
        self.cbNotify.setChecked(False)
        self.cbDark.setChecked(False)
        self.lblStatus.setText("当前状态：已恢复默认（自动保存）")
