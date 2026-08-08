# frameless_window_layout 布局模板说明
## 模板概述
基于**纯 PyQt6** 实现的**无边框窗口 + 自绘标题栏**布局预设，不依赖任何外部库（无 qframelesswindow、无平台 API）。提供：无边框窗口（FramelessWindowHint + 透明背景）、Win11 风格自绘标题栏（左键拖拽、双击最大化、最小化/最大化/关闭按钮）、四边/四角边缘缩放（Qt 6 原生 `startSystemResize`）、圆角 + 阴影（最大化时自动收起）。内容区沿用 **Ui/Interface 分离**架构，开箱即可二次开发。

## 目录结构
```
frameless_window_layout/
├─ main.py                    # ④ 启动入口：创建 FramelessWindow -> show
├─ app/
│  ├─ view/
│  │  ├─ main_window.py       # ③ 组装层 FramelessWindow：无边框/缩放/圆角/状态监听
│  │  ├─ Ui_HomeInterface.py  # ① 演示页 UI 定义
│  │  └─ home_interface.py    # ② 演示页逻辑（窗口状态检测 + 计数器）
│  ├─ common/
│  │  └─ constants.py         # 主题常量（标题栏/圆角/边距/配色）
│  └─ components/
│     ├─ title_bar.py         # 自绘标题栏组件（Win11 风格）
│     └─ example_card.py      # 可复用卡片
└─ assets/
   ├─ icon_min.svg            # 最小化图标
   ├─ icon_max.svg            # 最大化图标
   ├─ icon_restore.svg        # 还原图标
   └─ icon_close.svg          # 关闭图标
```

## 核心特性
1. **无边框**：`Qt.WindowType.FramelessWindowHint` 去掉系统标题栏；`WA_TranslucentBackground` 开启透明背景（圆角/阴影的前提）；
2. **自绘标题栏**：深色标题栏 + 三个窗口控制按钮（hover 高亮、关闭按钮 hover 变红）；图标随最大化/还原状态自动切换；
3. **左键拖拽移动**：标题栏 `mousePressEvent` 调 Qt 6 原生 `QWindow.startSystemMove()`——自动处理多屏、高 DPI、系统动画，无需手算坐标；
4. **双击最大化/还原**：标题栏 `mouseDoubleClickEvent`；
5. **四边/四角缩放**：主窗口 `_hit_test()` 检测 6px 边缘，命中后调原生 `QWindow.startSystemResize(edges)`；hover 边缘时光标自动切换（水平/垂直/对角）；
6. **圆角 + 阴影**：中央容器 QFrame 圆角 10px + `QGraphicsDropShadowEffect`（窗口四周留 12px 边距显示阴影）；
7. **最大化自适应**：`changeEvent` 监听 `WindowStateChange`，最大化时去掉圆角/阴影/边距（避免透明角），并同步标题栏图标；
8. **内容区 Ui/Interface 分离**：演示页含窗口状态检测（点击显示当前状态与尺寸）与计数器交互。

## 运行前置依赖
### 环境要求
Python 3.8+（边缘缩放需要 Qt 6.5+ 的 `startSystemResize`，建议 PyQt6 6.5+）
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

## 常用可调参数（app/common/constants.py）
| 参数名 | 默认值 | 作用 |
| ---- | ---- | ---- |
| TITLE_BAR_HEIGHT | 36px | 标题栏高度 |
| TITLE_BAR_BG | #2b2f36 | 标题栏背景色 |
| WINDOW_RADIUS | 10px | 窗口圆角半径 |
| EDGE_MARGIN | 6px | 边缘缩放检测宽度（越大越易命中） |
| ACCENT_BLUE | #4070f4 | 强调色 |

## 适配软件场景
- 需要现代无边框观感的桌面工具：播放器、阅读器、轻量效率工具、个性化客户端；
- 需要完全掌控窗口外观（自定义标题栏/圆角/阴影）的应用；
- 不希望引入第三方无边框库、追求纯 Qt 实现的项目。

## 拓展修改指引
1. **更换主题色**：改 `common/constants.py` 的配色常量；
2. **标题栏布局调整**：改 `components/title_bar.py`（按钮顺序、宽度、hover 效果）；
3. **新增页面**：参照演示页走 Ui/Interface 分离，在 `main_window.py` 里把页面加入 `self.stacked` 并替换根布局的内容区；
4. **去掉阴影**：删除 `FramelessWindow.__init__` 中 `QGraphicsDropShadowEffect` 部分，并把 `setContentsMargins(12,...)` 改 0；
5. **禁用缩放**：注释掉 `mousePressEvent`/`mouseMoveEvent` 中的边缘逻辑即可（保留标题栏拖拽）。

## 注意事项
- 运行前保证`assets`存在 4 个 SVG 图标，缺失会导致标题栏按钮空白；
- 无边框窗口的拖拽/缩放依赖 `windowHandle()`，**offscreen 平台（无真实窗口）下不可测**，冒烟测试只验证结构与逻辑；
- `WA_TranslucentBackground` 在部分系统/组合下可能与全屏或某些特效冲突，若遇到请关闭透明背景（阴影也会随之消失）；
- `Qt.Edges` 类型在 PyQt6 中不存在，边缘组合用 `Qt.Edge.LeftEdge | Qt.Edge.RightEdge`（flag 类型），类型注解写 `Qt.Edge`。
