# PyQt6-Layout-Templates
基于 PyQt6 打造的桌面端UI布局预设合集，主打开箱即用、可灵活二次改造，项目初期自用开源，欢迎提交PR补充新布局、优化现有模板。

## 运行环境
- Python：`3.8 ~ 3.14.6`（已适配3.14.6稳定运行）
- 依赖库：PyQt6（安装拉取最新稳定版即可）
```bash
pip install PyQt6
```

### 代码规范检查（开发时推荐）
- 类型检查：**basedpyright**（VSCode 插件 + 命令行均可）
- 类型桩：**PyQt6-stubs**（让 basedpyright 能对 Qt API 做类型推断，不装会大量报 Unknown）
```bash
pip install basedpyright PyQt6-stubs
```
- 检查规则配置在根目录 `pyproject.toml` 的 `[tool.basedpyright]`，VSCode 安装 basedpyright 插件后自动生效；命令行执行：`basedpyright layouts/`
- 项目当前基于该配置达到 **0 error / 0 warning**，提交代码前建议保持该标准

## 仓库目录结构
```
PyQt6-Layout-Templates/
├── layouts/                # 所有布局模板分类存放
│   ├── left_side_nav_layout/   # 左侧导航+右侧多页面（qfluentwidget gallery 式分层）
│   │   ├── demo.py             # 入口层
│   │   ├── app/                # view组装/页面层 + common公共层 + components组件层
│   │   ├── assets/
│   │   └── README.md
│   ├── left_side_nav_ui_layout/ # 左侧导航+多页面（clock 式 Ui/Interface 分离）
│   │   ├── main.py             # 启动入口
│   │   ├── app/                # view(Ui定义+Interface逻辑) + common + components
│   │   ├── assets/
│   │   └── README.md
│   ├── top_nav_tabs_layout/    # 顶部导航+多标签页内容区布局
│   │   ├── main.py
│   │   ├── assets/
│   │   └── README.md
│   └── frameless_window_layout/ # 无边框窗口+自绘标题栏（纯 PyQt6）
│       ├── main.py
│       ├── app/                # view(FramelessWindow+页面) + common + components
│       ├── assets/
│       └── README.md
├── assets/                 # 全局共用图标、样式资源
├── docs/                   # 架构速查手册（写代码前翻一翻，防乱来）
└── README.md               # 仓库总说明
```

## 现有模板清单
|模板文件夹|布局特点|适用场景|
| ---- | ---- | ---- |
|left_side_nav_layout|qfluentwidget gallery式分层（demo入口+app包）、注册式addInterface导航、页面继承基类、信号总线跨页面通信、可拖拽双栏+折叠、窗口缩放约束|轻量效率工具、小型管理客户端、本地素材/题库软件|
|left_side_nav_ui_layout|clock式 Ui/Interface 分离（Ui_定义+Interface逻辑，多重继承+setupUi）、注册式导航、信号总线、可拖拽双栏+折叠|Qt Designer 工作流、UI与逻辑分工协作的桌面工具|
|top_nav_tabs_layout|顶部导航+多标签页、标签拖动/关闭、新建空白标签、导航高亮联动|多模块切换工具、文档工作台、后台管理系统|
|frameless_window_layout|纯PyQt6无边框窗口+自绘标题栏、Qt6原生拖拽/边缘缩放、圆角+阴影、最大化自适应|播放器/阅读器、现代观感桌面工具、需完全掌控窗口外观的应用|

## 使用方式
1. 安装PyQt6依赖；
2. 进入`layouts`下对应模板子目录；
3. 参照子目录README放置图标资源，执行`python main.py`直接预览布局；
4. 修改代码常量、样式、按钮列表，定制自身业务界面。

## 拓展开发指引
1. 新增布局：在`layouts`新建独立小写命名文件夹，内部放主代码、专属资源、单模板README；
2. 样式复用：通用图标可放到根目录`assets`，减少重复文件；
3. 提交建议：欢迎补充全新布局方案、优化交互逻辑、完善注释文档。

## 注意事项
各模板自带独立资源目录，运行前检查图标文件完整；窗口尺寸、按钮宽高这类参数集中定义在代码头部常量区，修改便捷。