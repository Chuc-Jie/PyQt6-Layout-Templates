# PyQt6-Layout-Templates 架构速查手册

> 写代码前翻 3 分钟，防止"忘了写法乱来"。本手册总结仓库三个模板共同遵循的架构手法（分层 + 关注点分离 + UI/Interface 分离 + 事件总线），以及写代码时必须遵守的规范红线。

---

## 1. 这套手法一句话

**分层架构 + 关注点分离**：入口 → 组装层 → 页面逻辑层 → UI 定义层，依赖单向向下；页面自治互不引用；跨页面通信走信号总线；UI（长什么样）与逻辑（怎么干活）完全分离。

```
依赖方向（只许向下，禁止回头/平级乱连）
┌────────────────────────────────────────────────┐
│ main.py                启动入口：创建 MainWindow │
│   ↓                                              │
│ app/view/main_window.py  组装层：addInterface 注册│
│   ↓                                              │
│ app/view/xxx_interface.py  页面逻辑层（Presenter）│
│   ↓                                              │
│ app/view/Ui_XxxInterface.py  页面 UI 定义（View）│
│                                                  │
│ app/common/signal_bus.py  事件总线（跨页面通信）  │
│ app/common/constants.py   公共常量               │
│ app/components/           可复用组件             │
└────────────────────────────────────────────────┘
```

对应 qfluentwidget：`demo.py`=main.py；`view/main_window.py`=组装层；`view/*_interface.py`=页面；`view/Ui_*`=pyuic 生成的 UI 类；`common/`=公共层；`components/`=组件层。

---

## 2. 各文件职责与写法模板

### 2.1 入口 `main.py`（最薄，只启动）

```python
import sys

from PyQt6.QtWidgets import QApplication

from app.view.main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
```

### 2.2 组装层 `app/view/main_window.py`（只组装，零业务）

```python
from app.view.home_interface import HomeInterface
from app.view.setting_interface import SettingInterface


class MainWindow(QMainWindow):
    def __init__(self):
        ...
        self.homeInterface = HomeInterface()      # ① 先存实例属性
        self.settingInterface = SettingInterface()
        self.interface_btns: list[QPushButton] = []
        self.addInterface("首页", self.homeInterface)                  # ② 再注册
        self.addInterface("设置", self.settingInterface, position="bottom")
        self.stacked.setCurrentIndex(0)

    def addInterface(self, text: str, widget: QWidget, position: str = "top"):
        """注册：入 QStackedWidget + 生成导航按钮 + 绑定切换"""
        index = self.stacked.addWidget(widget)
        btn = QPushButton(text)
        ...
        btn.clicked.connect(lambda _, i=index: self.stacked.setCurrentIndex(i))
        self.interface_btns.append(btn)
        return index
```

**铁律：main_window 里不写任何页面业务逻辑**（不 setText、不操作列表、不弹窗）。它只做三件事：建页面实例、注册、折叠展开。

### 2.3 UI 定义层 `app/view/Ui_XxxInterface.py`（只画界面，零逻辑）

pyuic 风格：`object` 基类 + `setupUi`/`retranslateUi`。控件名 **camelCase**。

```python
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from app.common.constants import PAGE_BACKGROUNDS, SUBTITLE_STYLE, TITLE_STYLE


class Ui_HomeInterface(object):
    def setupUi(self, HomeInterface: QWidget):          # 参数必须注解
        HomeInterface.setObjectName("HomeInterface")
        HomeInterface.setStyleSheet(f"background:{PAGE_BACKGROUNDS[0]};")

        self.verticalLayout = QVBoxLayout(HomeInterface)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)

        self.titleLabel = QLabel(HomeInterface)
        self.titleLabel.setStyleSheet(TITLE_STYLE)
        self.verticalLayout.addWidget(self.titleLabel)

        self.btnClick = QPushButton(HomeInterface)
        self.verticalLayout.addWidget(self.btnClick)

        self.verticalLayout.addStretch()
        self.retranslateUi(HomeInterface)

    def retranslateUi(self, HomeInterface: QWidget):
        self.titleLabel.setText("首页")
        self.btnClick.setText("点我")
```

**铁律：Ui_ 文件里禁止出现** `clicked.connect`、`if` 业务判断、`signalBus`、任何"动作"。它只创建控件 + 摆放 + 设置初始文本。

### 2.4 页面逻辑层 `app/view/xxx_interface.py`（多重继承 + 逻辑）

```python
from PyQt6.QtWidgets import QWidget

from app.view.Ui_HomeInterface import Ui_HomeInterface


class HomeInterface(Ui_HomeInterface, QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent=parent)   # MRO 自动跳过 Ui_，直达 QWidget
        self.setupUi(self)                # 安装界面

        # 之后用 self.控件名 访问 UI 控件，写逻辑
        self.count = 0
        self.btnClick.clicked.connect(self._on_click)

    def _on_click(self):
        self.count += 1
        self.lblCount.setText(f"点击次数：{self.count}")
```

**铁律：页面不 import 其他页面、不 import 组装层**。只依赖：自己的 Ui_、`app.common.*`、`app.components.*`。

### 2.5 事件总线 `app/common/signal_bus.py`（跨页面通信唯一通道）

```python
from PyQt6.QtCore import QObject, pyqtSignal


class SignalBus(QObject):
    data_added = pyqtSignal(str)     # 新增信号：发送方 emit，接收方 connect


signalBus = SignalBus()              # 全局单例
```

发送：`signalBus.data_added.emit(text)`
接收：`signalBus.data_added.connect(self._on_data_added)`

**铁律：页面 A 想让页面 B 做事，必须走 signalBus，禁止 `from app.view.b_interface import BInterface` 直接引用。**

---

## 3. 新增一个页面的完整步骤（Checklist）

```
□ 1. 建 Ui_XxxInterface.py —— 画界面（setupUi + retranslateUi，零逻辑）
□ 2. 建 xxx_interface.py —— class XxxInterface(Ui_XxxInterface, QWidget)
□ 3. 逻辑里 super().__init__(parent=parent) + self.setupUi(self) + 挂逻辑
□ 4. main_window.py 顶部 import XxxInterface
□ 5. main_window.py __init__ 里：self.xxxInterface = XxxInterface()
□ 6. self.addInterface("标题", self.xxxInterface)  （底部入口加 position="bottom"）
□ 7. 运行 .venv\Scripts\basedpyright.exe layouts/ 确认 0 error / 0 warning
□ 8. python main.py 冒烟验证
```

新增页面**不需要改任何旧页面**——这就是开闭原则。

---

## 4. 命名约定

| 对象 | 规则 | 示例 |
| ---- | ---- | ---- |
| 页面 UI 定义文件 | `Ui_` + 页面名 + `.py` | `Ui_HomeInterface.py` |
| 页面逻辑文件 | 小写蛇形 | `home_interface.py` |
| UI 定义类 | `Ui_` + 页面类名 | `class Ui_HomeInterface` |
| 逻辑类 | 页面名 + `Interface` | `class HomeInterface` |
| UI 控件属性 | camelCase | `titleLabel`、`btnClick`、`lblCount` |
| 方法 | snake_case，私有 `_` 前缀 | `_on_click`、`_add_item` |
| 信号 | snake_case | `data_added` |

控件名是 Ui_ 与逻辑层的**唯一约定接口**：改了 Ui_ 里的属性名，必须同步改逻辑层的引用。

---

## 5. 反模式（"乱来"的样子，见到就改）

| ❌ 乱来 | ✅ 正确做法 |
| ---- | ---- |
| 逻辑写进 Ui_ 文件（connect/if/emit 出现在 Ui_ 里） | Ui_ 只画界面，逻辑全部进 `*_interface.py` |
| 页面直接 import 另一个页面拿数据 | 走 `signalBus` 信号 |
| `main_window.py` 里 setText / 操作业务控件 | 业务全在页面类，组装层只注册 |
| 页面继承 `QMainWindow` 或自建窗口 | 页面都是 `QWidget`，窗口只有组装层一个 |
| 一个页面一个文件里堆 500 行 | 拆 Ui_ + interface，每个职责一个小文件 |
| 忘记 `self.setupUi(self)` | 构造里必须 `super().__init__` 后立即 `setupUi` |
| 手写 Ui_ 时漏 `: QWidget` 参数注解 | basedpyright 会报 Unknown，保持注解 |
| 空列表不加类型：`self.btns = []` | `self.btns: list[QPushButton] = []` |
| 新增页面后 main_window 里手写一堆按钮代码 | 用 `addInterface` 一行注册 |

---

## 6. 写代码规范红线（basedpyright，0 error / 0 warning）

1. 不留未使用的 import（error 级）；
2. 函数/方法参数全部注解：`parent: QWidget | None = None`、`index: int`、`item: QListWidgetItem`、信号槽 `*_args: object`；
3. 空集合带类型注解：`list[QPushButton] = []`、`list[str] = []`；
4. 手写 Ui_ 的 `setupUi`/`retranslateUi` 参数注解 `QWidget`；pyuic 生成的 Ui_ 用文件级 `# pyright:` 豁免，不手改；
5. 提交前验证：`.venv\Scripts\basedpyright.exe layouts/` → `0 errors, 0 warnings`。

配置在根目录 `pyproject.toml` 的 `[tool.basedpyright]`。

---

## 7. 本环境注意事项（踩过的坑）

- **PyQt6 6.11 + Python 3.14.6：信号槽内抛 Python 异常会原生崩溃**（退出码 -1073740791，无报错）。槽函数里先 `hasattr`/`try-except` 防御；构造期间触发信号的方法（`setChecked(True)` 等）放在所有依赖控件创建之后。
- 运行/验证一律用 `D:\Programme\Python314Code\FramelessWindow\.venv\Scripts\python.exe`（已装 PyQt6 + PyQt6-stubs）；`py` 只用于语法检查。
- 入口文件在模板根目录运行：`python main.py` / `python demo.py`，勿直接运行 `app/` 内文件（`import app` 会失败）。

---

## 8. 模板速查

| 模板 | 页面组织方式 | 入口 |
| ---- | ---- | ---- |
| `left_side_nav_layout` | 页面继承 `BaseInterface`（基类给骨架） | `demo.py` |
| `left_side_nav_ui_layout` | **Ui_ 定义 + Interface 逻辑分离（本手册主推）** | `main.py` |
| `top_nav_tabs_layout` | 单文件 + QTabWidget | `main.py` |

> 推荐新页面一律按第 3 节 Checklist 走 Ui/Interface 分离，最省心。
