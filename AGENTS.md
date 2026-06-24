# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## 仓库性质

这是一个 **Obsidian Vault**（个人学习笔记库），不是软件工程项目。仓库内**没有**构建系统、测试、lint 配置或可执行代码 —— 不要尝试运行 build/test/lint 命令。

主题领域：游戏动画绑定 / 技术美术（Tech Art）。主要内容包括 Maya（rigging、变形器、Python/C++ API、MEL）、Unreal Engine 5（Control Rig、ChaosCloth、Python、C++、Gameplay 框架）、MotionBuilder（pyfbsdk）、Python/C++/数据结构算法、CMake、Git、VSCode 配置等。

笔记语言为**中文**，技术术语保留英文。回答与笔记内容编辑均使用中文。

## 顶层结构（仅记录非显而易见的部分）

- `Notes/MAYA/Rigging/` 按学习阶段分目录：`初级/`、`进阶/`、`常用算法和问题/`、`解决方案/`。文件名前缀（如 `1.02-`、`2.05-`）是章节序号，新增笔记时遵循同一编号体系。
- `Notes/Templates/` 是 Obsidian 笔记模板，新建特定主题笔记时可参考其结构。
- `Excalidraw/` 与各处的 `.canvas` 文件由 Excalidraw / Obsidian Canvas 插件生成 —— 不要手工编辑这些 JSON。
- `attachments/`（在 vault 根目录及多个子目录下都有）存放图片等附件。

## Obsidian 写作约定（关键）

`.obsidian/app.json` 已固定以下规则，编辑或新建笔记时**必须遵守**：

- **链接格式**：Markdown 格式 `[text](path)`，**不要**用 wiki 链接 `[[...]]`。
- **链接路径**：相对路径（`newLinkFormat: "relative"`），不要写绝对路径或仓库根路径。
- **附件位置**：`./attachments`（相对于当前笔记所在目录）。新增图片/资源时放入同级 `attachments/` 子目录，引用时也用相对路径。
- **新文件位置**：与当前编辑的笔记同目录（`newFileLocation: "current"`）。
- 文件名包含中文且常用全角字符；Bash 中处理路径时务必加双引号，并注意 git status 里中文显示为转义字符。

## 已启用的 Obsidian 插件（影响内容格式）

`obsidian-excalidraw-plugin`、`obsidian-kanban`、`image-converter`、`obsidian-image-toolkit`、`oz-clear-unused-images`。看到看似畸形的 `.md`（带大段 JSON / base64）通常是这些插件生成的，**不要**当作普通 markdown 改写。

## 代码片段风格（笔记中嵌入的示例代码）

笔记中常嵌入 Python / C++ / MEL 代码示例。当用户要求新增或修改这些示例时，遵循全局 `~/.Codex/AGENTS.md` 的技术规范：

- Maya Python：优先 `pymel`，密集数学计算用 Maya Python API 2.0；
- MotionBuilder：注意内存泄露与 UI 线程安全；
- UE Python：使用最新 `unreal` 模块，关注批量资产性能；
- Python 代码遵循 PEP 8 + 类型注解 + docstring；命名 snake_case / PascalCase / UPPER_SNAKE_CASE。

## Git 习惯

提交信息以中文为主（如 `笔记修改`、`新增内容`、`vault backup: <date>`）。`.gitignore` 采用白名单方式处理 `.obsidian/`：默认忽略全部，仅保留 `app.json`、`core-plugins.json`、`community-plugins.json` 三个跨机器共享的配置文件被跟踪；`workspace.json`、`appearance.json`、`themes/`、各插件 `data.json` 等本地状态/外观/缓存均不入库。
