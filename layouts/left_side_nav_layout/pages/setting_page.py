"""
 页面层 - 设置页 SettingPage
 页面自治：本页面的布局、控件与交互逻辑全部在类内实现。
 演示：选项开关 + 恢复默认，逻辑均在页面内部。
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCheckBox, QFrame, QLabel, QPushButton, QVBoxLayout, QWidget


class SettingPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background:#fdeeee;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("设置")
        title.setStyleSheet("font-size:18px;font-weight:600;color:#1f2329;")
        layout.addWidget(title)

        card = QFrame()
        card.setStyleSheet("background:#ffffff;border-radius:10px;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(14)

        tip = QLabel(
            "「设置」页面：选项状态与「恢复默认」逻辑都在 SettingPage 类内实现\n"
            "勾选选项后点击恢复默认，将重置为初始状态"
        )
        tip.setStyleSheet("font-size:14px;color:#555555;line-height:1.6;")
        card_layout.addWidget(tip)

        # 选项开关（页面内部状态）
        self.cb_auto_save = QCheckBox("自动保存")
        self.cb_notify = QCheckBox("启用通知")
        self.cb_dark = QCheckBox("深色模式")
        for cb in (self.cb_auto_save, self.cb_notify, self.cb_dark):
            cb.setStyleSheet(
                "font-size:14px;color:#333333;spacing:8px;"
                "QCheckBox::indicator { width:16px; height:16px; }"
            )
            cb.toggled.connect(self._on_option_changed)

        card_layout.addWidget(self.cb_auto_save)
        card_layout.addWidget(self.cb_notify)
        card_layout.addWidget(self.cb_dark)

        self.lbl_status = QLabel("当前状态：自动保存已开启")
        self.lbl_status.setStyleSheet("font-size:13px;color:#888888;")
        card_layout.addWidget(self.lbl_status)

        self.btn_reset = QPushButton("恢复默认")
        self.btn_reset.setFixedSize(120, 36)
        self.btn_reset.setStyleSheet(
            """
            QPushButton {
                color: #ffffff;
                background: #c94f4f;
                border: none;
                border-radius: 6px;
                outline: none;
            }
            QPushButton:hover { background: #ad4141; }
            QPushButton:pressed { background: #8f3434; }
            """
        )
        self.btn_reset.clicked.connect(self._reset_defaults)
        card_layout.addWidget(self.btn_reset, alignment=Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(card, 1)

        # 初始状态：触发 toggled 信号时上方控件已全部创建完毕
        self.cb_auto_save.setChecked(True)

    def _on_option_changed(self):
        # 防御：控件尚未初始化完成时直接忽略（避免槽内异常）
        if not hasattr(self, "lbl_status"):
            return
        parts = []
        if self.cb_auto_save.isChecked():
            parts.append("自动保存")
        if self.cb_notify.isChecked():
            parts.append("通知")
        if self.cb_dark.isChecked():
            parts.append("深色")
        self.lbl_status.setText(
            "当前状态：" + ("、".join(parts) if parts else "全部关闭")
        )

    def _reset_defaults(self):
        self.cb_auto_save.setChecked(True)
        self.cb_notify.setChecked(False)
        self.cb_dark.setChecked(False)
        self.lbl_status.setText("当前状态：已恢复默认（自动保存）")
