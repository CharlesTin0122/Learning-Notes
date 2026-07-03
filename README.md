# Learning-Notes

游戏动画绑定 / 技术美术（Tech Art）方向的个人学习笔记库。

这是一个 **Obsidian Vault**，而非软件工程项目 —— 仓库内没有构建系统、测试或可执行代码。笔记以**中文**书写，技术术语保留英文。目前收录约 800+ 篇 Markdown 笔记。

## 主题领域

- **Maya**：Rigging（绑定）、变形器、Python/C++ API、MEL、PySide UI、Bifrost、布料（Qualoth / Carbon）
- **Unreal Engine 5**：Control Rig、ChaosCloth、ML Deformer、Physics、Python/C++、Gameplay 框架、Lyra、ALS、MetaHuman、高级运动系统
- **MotionBuilder**：操作与 pyfbsdk 编程
- **编程基础**：Python、C++、C 语言、数据结构与算法
- **数学**：矩阵、线性代数等绑定相关数学基础

## 目录结构

```
Notes/
├── MAYA/                 # Maya 相关（Rigging、API、Mel、UI、布料、Bifrost）
│   ├── Rigging/          # 按学习阶段：初级 / 进阶 / 常用算法和问题 / 解决方案
│   ├── Maya Python API/  # Python API 1.0 入门 / 2.0 / 基础知识
│   ├── mayaUI/           # PySide for Maya
│   └── 布料/             # Qualoth、Carbon 布料插件
├── Unreal/               # UE5 相关
│   ├── Control Rig/      # 控制绑定
│   ├── 布料/             # ChaosCloth
│   ├── MLDeformer/       # 机器学习变形器
│   ├── unreal_gameplay/  # Gameplay 框架
│   ├── Lyra、ALS v4、MetaHuman、深入浅出高级运动系统 ...
│   └── UEC++、Unreal Python、项目规范 ...
├── MotionBuilder/        # 操作 + 编程（pyfbsdk）
├── program/              # 编程基础（Python / C++ / C语言 / 数据结构与算法）
├── math/                 # 数学基础
├── Misc/                 # 杂项、面试笔记
├── Work/                 # 工作相关
└── Templates/            # Obsidian 笔记模板
```

`Rigging/` 及部分目录的文件名前缀（如 `1.02-`、`2.05-`）为章节序号，新增笔记时沿用同一编号体系。各处的 `attachments/` 子目录存放图片等附件。

## 写作约定

由 `.obsidian/app.json` 固定，编辑或新建笔记时须遵守：

- **链接格式**：Markdown 链接 `[text](path)`，不使用 wiki 链接 `[[...]]`
- **链接路径**：相对路径
- **附件位置**：放入笔记同级的 `attachments/` 子目录，用相对路径引用
- **新文件位置**：与当前笔记同目录

带大段 JSON / base64 的畸形 `.md`，以及 `.canvas` 文件，由 Excalidraw / Canvas 等插件生成，**不要**手工编辑。

## 已启用插件

`obsidian-excalidraw-plugin`、`obsidian-kanban`、`image-converter`、`obsidian-image-toolkit`、`oz-clear-unused-images`、`obsidian-style-settings`、`better-export-pdf`、`consistent-attachments-and-links`、`obsidian-git`。

其中 `obsidian-git` 会自动生成 `vault backup: <date>` 备份提交；`consistent-attachments-and-links` 会自动维护附件路径与链接一致性。

## Git 约定

提交信息以中文为主（如 `笔记修改`、`新增内容`、`vault backup: <date>`）。`.gitignore` 对 `.obsidian/` 采用白名单策略：默认忽略全部，仅跟踪 `app.json`、`core-plugins.json`、`community-plugins.json` 三个跨机器共享的配置文件。
