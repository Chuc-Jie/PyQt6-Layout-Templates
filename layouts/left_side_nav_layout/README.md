# left_side_nav_layout 布局模板说明
## 模板概述
基于PyQt6实现的**左侧可折叠常驻导航 + 右侧 QStackedWidget 多页面布局**，采用**分层架构**（参考 qfluentwidget 的组织方式）：右侧每个页面是独立的 `QWidget` 类，页面的布局、控件与交互逻辑在页面类内部自治实现；`main.py` 作为组装层只负责导入页面、注册进 `QStackedWidget` 并绑定侧边栏导航切换。依靠 QSplitter 实现左右区域拖拽调节宽度，侧边栏支持一键折叠，整体适配中小型桌面工具、轻量化管理系统，开箱即可二次开发。

## 目录结构
```
left_side_nav_layout/
├─ main.py          # 组装层：导入页面 -> 实例化 -> 注册进 QStackedWidget -> 绑定导航
├─ pages/           # 页面层：每个页面一个 QWidget 类，页面自治
│  ├─ __init__.py
│  ├─ home_page.py      # HomePage：首页（计数器交互演示）
│  ├─ data_page.py      # DataPage：数据管理（待办列表增删演示）
│  └─ setting_page.py   # SettingPage：设置（选项开关+恢复默认演示）
├─ assets/
│  └─ GriddyIconsSidebar.svg  # 侧边折叠/展开图标
└─ README.md        # 当前说明文档
```

## 分层架构（重点）
```
┌─────────────────────────────────────────────┐
│ 组装层 main.py（SideBarWindow）                │
│  - 导入页面类 → 实例化 → 注册进 QStackedWidget │
│  - 侧边栏按钮 → stacked.setCurrentIndex(i)     │
├─────────────────────────────────────────────┤
│ 页面层 pages/（每个文件一个 QWidget 类）        │
│  - HomePage / DataPage / SettingPage          │
│  - 各自的布局、控件、槽函数、业务逻辑全部在类内  │
└─────────────────────────────────────────────┘
```
对应 qfluentwidget 的约定：页面类自管自身交互，主窗口只做组装；新增页面 = 新建一个页面文件 + 组装层加两行注册代码，不动任何旧页面。

## 核心特性
1. **双栏弹性分栏**：横向分割侧边导航栏、右侧页面区，支持手动拖拽调整宽度，侧边栏最大宽度锁定为220px；
2. **QStackedWidget 多页面**：右侧所有页面共存于堆栈中，同一时间只显示一个，`setCurrentIndex` 即时切换；
3. **一键折叠展开**：顶部图标按钮收起侧边栏、右侧唤起展开按钮，最大化内容展示空间；
4. **侧边栏分层布局**：顶部标题+折叠控件、中部导航按钮区、弹性留白、底部设置按钮锚定贴底；
5. **页面自治演示**：计数器（HomePage）、待办列表增删（DataPage）、选项开关+恢复默认（SettingPage），交互逻辑均不依赖主窗口；
6. **窗口适配保护**：默认窗口尺寸900×600，最小缩放限制800×520，防止小窗口控件挤压错乱。

## 运行前置依赖
### 环境要求
Python 3.8+
### 安装依赖
```bash
pip install PyQt6
```

## 启动方式
1. 将图标文件放入`assets`目录；
2. 在当前目录执行命令：
```bash
python main.py
```

## 常用可调参数（main.py内全局常量）
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
1. **新增页面**：在`pages/`新建`xxx_page.py`，类继承`QWidget`并实现页面自己的布局与交互；在`main.py`顶部`from pages.xxx_page import XxxPage`，实例化后`stacked.addWidget(xxx_page)`，再给侧边栏加一个绑定`setCurrentIndex(新索引)`的按钮；
2. **修改页面内容**：直接编辑对应页面类，无需改动`main.py`——这是分层架构的核心收益；
3. **跨页面通信**：可仿照 qfluentwidget 引入信号总线（SignalBus）集中管理，或通过自定义信号在页面间解耦通信；
4. **修改配色**：分别调整页面类内的QSS代码段；
5. **解锁最大窗口限制**：取消注释`setMaximumSize`即可自定义窗口上限尺寸。

## 注意事项
运行前务必保证`assets`文件夹存在目标SVG图标，图标缺失会导致折叠按钮空白；可自行替换同名图标文件，无需改动代码路径。`pages`包必须与`main.py`同级，否则导入失败。
