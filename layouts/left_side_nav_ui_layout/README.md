# left_side_nav_ui_layout 布局模板说明
## 模板概述
基于PyQt6实现的**左侧可折叠常驻导航 + 右侧 QStackedWidget 多页面布局**，页面采用 **Ui/Interface 分离**模式（仿 qfluentwidget `examples/window/clock`）：每个页面拆成两个文件——`Ui_XxxInterface.py`（只描述界面：控件+布局，对应 Qt Designer/pyuic 生成的 UI 类）与 `xxx_interface.py`（只实现逻辑：多重继承 UI 类后 `setupUi` 安装界面，再挂业务）。整体沿 gallery 式分层：入口 `main.py` → 组装层 `main_window.py`（注册式导航）→ 页面层（Ui+Interface）→ 公共层/组件层。

## 目录结构
```
left_side_nav_ui_layout/
├─ main.py                    # ④ 启动入口：导入组装层 MainWindow -> show
├─ app/
│  ├─ view/
│  │  ├─ main_window.py       # ③ 组装层：注册式 addInterface + 折叠逻辑
│  │  ├─ Ui_HomeInterface.py      # ① 首页 UI 定义（控件+布局，零逻辑）
│  │  ├─ Ui_DataInterface.py      # ① 数据管理 UI 定义
│  │  ├─ Ui_SettingInterface.py   # ① 设置 UI 定义
│  │  ├─ home_interface.py        # ② 首页逻辑：class HomeInterface(Ui_HomeInterface, QWidget)
│  │  ├─ data_interface.py        # ② 数据管理逻辑
│  │  └─ setting_interface.py     # ② 设置逻辑
│  ├─ common/                 # 信号总线 + 公共常量
│  │  ├─ signal_bus.py
│  │  └─ constants.py
│  └─ components/             # 可复用组件
│     └─ example_card.py
└─ assets/                    # 图标资源
```

## Ui/Interface 分离模式（重点，仿 clock 示例）
```
Ui_XxxInterface.py（UI 定义）        xxx_interface.py（逻辑）
┌──────────────────────────┐   ┌────────────────────────────────────┐
│ class Ui_XxxInterface:   │   │ class XxxInterface(Ui_XxxInterface, │
│   def setupUi(self, w):  │──▶│                    QWidget):        │
│     self.lbl = QLabel(w) │   │   def __init__(self, parent=None):  │
│     ...创建控件/布局...    │   │       super().__init__(parent=parent)│
│     self.retranslateUi(w)│   │       self.setupUi(self)  # 安装界面 │
└──────────────────────────┘   │       # 之后直接操作 UI 控件+加逻辑  │
                               │       self.btnClick.clicked.connect(...)│
                               └────────────────────────────────────┘
```
- **UI 定义文件**：只描述"长什么样"，结构与 pyuic6 从 `.ui` 生成的代码一致（`object` 基类 + `setupUi`），可用 Qt Designer 可视化编辑后 `pyuic6 -x xxx.ui -o Ui_xxx.py` 重新生成；
- **逻辑文件**：`class XxxInterface(Ui_XxxInterface, QWidget)` 多重继承，`super().__init__(parent=parent)` 会沿 MRO 自动调用 `QWidget.__init__`（`Ui_` 类无 `__init__`，被跳过），再 `self.setupUi(self)` 把界面装到自己身上，之后用 `self.控件名` 直接访问（控件名为 Ui 定义中的属性名，camelCase）；
- **导入链路**：`Ui_*` → `*_interface` → `main_window.py`（组装注册）→ `main.py`（启动入口），逐层向上，方向单一。

## 核心特性
1. **UI 与逻辑完全分离**：改界面不动逻辑、改逻辑不动界面，两者通过约定好的控件名（`self.xxx`）对接；
2. **注册式导航**：`addInterface(text, 页面实例, position)` 一行完成"入堆栈+导航按钮+切换"；
3. **双栏弹性分栏**：QSplitter 拖拽调节、侧边栏 220px 上限、一键折叠/展开；
4. **信号总线解耦**：数据管理页 `signalBus.data_added.emit()` → 首页实时接收展示；
5. **组件复用**：`ExampleCard` 卡片在 Ui 定义层直接复用；
6. **窗口适配保护**：默认 900×600，最小 800×520。

## 运行前置依赖
### 环境要求
Python 3.8+
### 安装依赖
```bash
pip install PyQt6
```

## 启动方式
1. 将图标文件放入`assets`目录；
2. 在模板根目录执行（入口是 main.py，勿运行 app/ 内文件）：
```bash
python main.py
```

## 常用可调参数（app/view/main_window.py 顶部常量）
| 参数名 | 默认值 | 作用 |
| ---- | ---- | ---- |
| side_expand_w | 220px | 侧边栏展开默认宽度 |
| side_max_w | 220px | 侧边栏可拖拽最大宽度 |
| menu_btn_mini_w | 160px | 导航按钮最小宽度 |
| menu_btn_max_w | 180px | 导航按钮最大宽度 |
| menu_btn_height | 38px | 导航按钮固定高度 |

## 适配软件场景
- 需要"界面设计器改 UI、开发者写逻辑"分工协作的桌面工具；
- 多页面管理型客户端：进销存、素材库、离线题库、数据采集；
- 想从 Qt Designer（.ui）工作流迁入的 PyQt6 项目。

## 拓展修改指引
1. **新增页面**：新建 `Ui_XxxInterface.py`（UI 定义）+ `xxx_interface.py`（`class XxxInterface(Ui_XxxInterface, QWidget)` + 逻辑），再在 `main_window.py` 加一行 `self.addInterface('标题', XxxInterface())`；
2. **可视化改界面**：在 Qt Designer 中画好 `xxx.ui`，`pyuic6 xxx.ui -o Ui_XxxInterface.py` 覆盖生成 UI 文件（逻辑文件不动）；
3. **修改逻辑**：只编辑 `xxx_interface.py`，用 `self.控件名` 访问 Ui 定义中的控件；
4. **跨页面通信**：在 `common/signal_bus.py` 新增信号，`emit`/`connect` 解耦；
5. **公共配色**：改 `common/constants.py`。

## 注意事项
运行前保证`assets`存在目标SVG图标，否则折叠按钮空白；必须从模板根目录执行`python main.py`（app 是包）。Ui 定义中控件属性名（camelCase）与逻辑层引用要保持一致；若用 pyuic 重新生成 Ui 文件，注意对比属性名是否变化。
