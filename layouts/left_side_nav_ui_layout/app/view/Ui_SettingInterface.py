"""
 UI 定义层 - 设置页（Ui_SettingInterface）
 只描述界面长什么样，零业务逻辑；逻辑由 setting_interface.py 的 SettingInterface 实现。
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCheckBox, QLabel, QPushButton, QVBoxLayout, QWidget

from app.common.constants import PAGE_BACKGROUNDS, SUBTITLE_STYLE, TITLE_STYLE
from app.components.example_card import ExampleCard


class Ui_SettingInterface(object):
    def setupUi(self, SettingInterface: QWidget):
        SettingInterface.setObjectName("SettingInterface")
        SettingInterface.resize(700, 560)
        SettingInterface.setStyleSheet(f"background:{PAGE_BACKGROUNDS[2]};")

        self.verticalLayout = QVBoxLayout(SettingInterface)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(12)

        # 标题 + 副标题
        self.titleLabel = QLabel(SettingInterface)
        self.titleLabel.setStyleSheet(TITLE_STYLE)
        self.verticalLayout.addWidget(self.titleLabel)

        self.subtitleLabel = QLabel(SettingInterface)
        self.subtitleLabel.setStyleSheet(SUBTITLE_STYLE)
        self.verticalLayout.addWidget(self.subtitleLabel)

        # 选项卡片
        self.settingCard = ExampleCard("选项（交互逻辑在 Interface 类内）", SettingInterface)
        self.tipLabel = QLabel(self.settingCard)
        self.tipLabel.setStyleSheet("font-size:13px;color:#555555;line-height:1.6;")
        self.settingCard.content_layout.addWidget(self.tipLabel)

        self.cbAutoSave = QCheckBox(self.settingCard)
        self.cbNotify = QCheckBox(self.settingCard)
        self.cbDark = QCheckBox(self.settingCard)
        for cb in (self.cbAutoSave, self.cbNotify, self.cbDark):
            cb.setStyleSheet(
                "font-size:14px;color:#333333;spacing:8px;"
                "QCheckBox::indicator { width:16px; height:16px; }"
            )
            self.settingCard.content_layout.addWidget(cb)

        self.lblStatus = QLabel(self.settingCard)
        self.lblStatus.setStyleSheet("font-size:13px;color:#888888;")
        self.settingCard.content_layout.addWidget(self.lblStatus)

        self.btnReset = QPushButton(self.settingCard)
        self.btnReset.setFixedSize(120, 36)
        self.btnReset.setStyleSheet(
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
        self.settingCard.content_layout.addWidget(self.btnReset, alignment=Qt.AlignmentFlag.AlignLeft)
        self.verticalLayout.addWidget(self.settingCard)

        self.verticalLayout.addStretch()
        self.retranslateUi(SettingInterface)

    def retranslateUi(self, SettingInterface: QWidget):
        self.titleLabel.setText("设置")
        self.subtitleLabel.setText("页面自治演示：选项开关 + 恢复默认")
        self.tipLabel.setText("勾选选项后点击恢复默认，将重置为初始状态。")
        self.cbAutoSave.setText("自动保存")
        self.cbNotify.setText("启用通知")
        self.cbDark.setText("深色模式")
        self.lblStatus.setText("当前状态：自动保存已开启")
        self.btnReset.setText("恢复默认")
