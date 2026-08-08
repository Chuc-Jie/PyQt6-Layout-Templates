# left_side_nav_layout 布局模板说明
## 模板概述
基于PyQt6实现的**左侧可折叠常驻导航 + 右侧 QStackedWidget 多页面布局**，工程结构完整仿照 **qfluentwidget gallery** 的分层架构（入口层 / 组装层 / 页面层 / 公共层 / 组件层 / 资源层）。右侧页面继承统一页面基类、页面自治；组装层采用**注册式导航**（仿 `addSubInterface`）：一行 `addInterface()` 自动完成页面入堆栈 + 导航按钮生成 + 点击切换；跨页面通信走**信号总线**单例解耦。开箱即可二次开发。

## 目录结构
```
left_side_nav_layout/
├─ demo.py                   # ① 入口层：启动配置 -> 导入组装层 MainWindow -> show
├─ app/                      # 应用包（仿 qfluentwidget gallery）
│  ├─ view/                  # ④ 视图层
│  │  ├─ main_window.py      # ② 组装层 MainWindow：注册式 addInterface + 折叠逻辑
│  │  ├─ base_interface.py   # 页面基类：统一骨架（标题/副标题/滚动内容区）
│  │  ├─ home_interface.py   # 首页（计数器 + 信号总线接收）
│  │  ├─ data_interface.py   # 数据管理（待办列表，添加时广播信号）
│  │  └─ setting_interface.py # 设置（选项开关 + 恢复默认）
│  ├─ common/                # ⑤ 公共层
│  │  ├─ signal_bus.py       # 信号总线单例（跨页面通信解耦）
│  │  └─ constants.py        # 公共颜色/样式常量
│  ├─ components/            # ⑥ 通用组件层
│  │  └─ example_card.py     # ExampleCard 白色圆角卡片（页面复用）
│  └─ resource/              # （预留）资源层
├─ assets/                   # ⑦ 资源：SVG 图标
└─ README.md                 # 当前说明文档
```

## 分层架构（对应 qfluentwidget gallery）
```
demo.py（入口）
   └─ from app.view.main_window import MainWindow   # 主程序导入组装层
        └─ MainWindow（组装层）
             ├─ from app.view.home_interface import HomeInterface  # 组装层导入页面
             ├─ addInterface('首页', HomeInterface())              # 注册：入堆栈+导航按钮+切换
             └─ 折叠/展开逻辑
                  └─ 页面类（继承 BaseInterface，页面自治）
                       ├─ 布局、控件、槽函数全部在页面类内
                       └─ 跨页面通信：signalBus.emit / signalBus.connect
```
对应官方结构：`demo.py` = 入口；`view/main_window.py` = 组装层；`view/*_interface.py` = 页面层；`common/` = 公共层；`components/` = 组件层；`assets/` = 资源层。

## 核心特性
1. **注册式导航**：`addInterface(text, 页面实例, position)` 一行完成"页面入堆栈 + 生成导航按钮 + 绑定切换"，新增页面无需改任何切换代码（对应 qfluentwidget `addSubInterface`）；
2. **双栏弹性分栏**：QSplitter 左右拖拽调节宽度，侧边栏最大宽度 220px，一键折叠/展开；
3. **页面继承基类**：`BaseInterface` 统一标题/副标题/滚动内容区外观，子类只填内容（对应 `GalleryInterface`）；
4. **页面自治**：计数器（首页）、待办增删（数据管理）、选项开关（设置）交互逻辑均在页面类内，主窗口零业务代码；
5. **信号总线解耦**：数据管理页添加待办 -> `signalBus.data_added.emit()` -> 首页实时展示，两页面互不引用（对应 `common/signal_bus.py`）；
6. **组件复用**：`ExampleCard` 卡片由各页面共用，避免重复样式（对应 `components/`）；
7. **窗口适配保护**：默认 900×600，最小 800×520。

## 运行前置依赖
### 环境要求
Python 3.8+
### 安装依赖
```bash
pip install PyQt6
```

## 启动方式
1. 将图标文件放入`assets`目录；
2. 在模板根目录执行（入口是 demo.py，勿运行 app/ 内文件）：
```bash
python demo.py
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
- 轻量桌面效率工具：格式转换器、文件批量处理工具、本地笔记阅读器；
- 小型业务管理客户端：门店进销存、本地考勤统计、简易数据采集程序；
- 素材管理、离线刷题、小型设备监控类桌面软件。

## 拓展修改指引
1. **新增页面**：在`app/view/`新建`xxx_interface.py`，继承`BaseInterface`，页面内容填进`self.add_card()`；在`main_window.py`顶部`from app.view.xxx_interface import XxxInterface`，再加一行`self.addInterface('标题', XxxInterface(), position='top')`即可，无需其他改动；
2. **修改页面内容**：只编辑对应页面类，不动组装层；
3. **跨页面通信**：在`common/signal_bus.py`的`SignalBus`类中新增信号，发送页`signalBus.xxx.emit(...)`、接收页`signalBus.xxx.connect(...)`，保持页面解耦；
4. **新增可复用组件**：放入`app/components/`，页面 import 复用；
5. **修改配色**：公共颜色改`common/constants.py`，页面专属样式改页面类内QSS；
6. **导航分级**：可在`addInterface`基础上扩展 position 枚举（如 scroll 滚动区）、图标参数、子导航 parent 参数，复刻 qfluentwidget 更完整能力。

## 注意事项
运行前务必保证`assets`文件夹存在目标SVG图标，图标缺失会导致折叠按钮空白；可自行替换同名图标文件，无需改动代码路径。必须从模板根目录执行`python demo.py`（app 是包，入口在根），否则 `import app` 会失败。
