"""
 页面层 - 设置页 SettingInterface
 页面自治：布局、控件、交互逻辑全部在类内实现。
 演示：选项开关 + 恢复默认。
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCheckBox, QLabel, QPushButton

from app.common.constants import PAGE_BACKGROUNDS
from app.components.example_card import ExampleCard
from app.view.base_interface import BaseInterface


class SettingInterface(BaseInterface):
    def __init__(self, parent=None):
        super().__init__(
            "设置",
            "页面自治演示：选项开关 + 恢复默认",
            PAGE_BACKGROUNDS[2],
            parent,
        )

        card = ExampleCard("选项（交互逻辑在本页面类内）")
        tip = QLabel("勾选选项后点击恢复默认，将重置为初始状态。")
        tip.setStyleSheet("font-size:13px;color:#555555;line-height:1.6;")
        card.content_layout.addWidget(tip)

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
            card.content_layout.addWidget(cb)

        self.lbl_status = QLabel("当前状态：自动保存已开启")
        self.lbl_status.setStyleSheet("font-size:13px;color:#888888;")
        card.content_layout.addWidget(self.lbl_status)

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
        card.content_layout.addWidget(self.btn_reset, alignment=Qt.AlignmentFlag.AlignLeft)
        self.add_card(card)

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
