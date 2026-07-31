---
tags:
  - Maya
  - Python
  - Rigging
  - 开源库
---

# cymel vs cmdx：两个 Maya Python 包裹库对比

> 两个都是替代 PyMEL 的现代 Maya Python 包裹库，但设计哲学完全不同：**cymel 是给"写工具的人"用的（人体工学），cmdx 是给"跑得快的代码"用的（性能）**。二者并不互斥。

- cymel：https://github.com/ryusas/cymel （文档：[英](https://ryusas.github.io/cymel/en/index.html) / [日](https://ryusas.github.io/cymel/ja/index.html)）
- cmdx：https://github.com/mottosso/cmdx （[Command Reference](https://mottosso.com/cmdx)）

## 一、基本盘对比

| | **cymel** (ryusas) | **cmdx** (mottosso) |
|---|---|---|
| 作者背景 | 佐々木隆二，日本资深绑定 TA | Marcus Ottosson（Ragdoll Dynamics 作者），cmdx 是 Ragdoll 的底层库 |
| 定位 | **轻量版 PyMEL**：面向对象的 Maya 脚本体验 | **高速版 cmds 子集**：性能优先的 API 2.0 包裹 |
| 体量 | ~28,000 行，完整包结构（core/datatypes/ui/qt/…） | **单文件** `cmdx.py`，~9,100 行 |
| 维护状态 | 活跃（2026-07 仍有提交） | 活跃（0.6.5，2026-06，已支持 Maya 2027+） |
| 文档 | 日/英双语 Sphinx 文档 | 英文 README + 在线 Command Reference，非常详尽 |
| 安装 | pip / 拷贝包 | pip / **直接拷一个文件进项目**（官方推荐 vendoring） |
| Maya 2024 + Py3.10 | ✅ | ✅ |

## 二、设计哲学差异（核心）

### cymel —— "PyMEL 的正确打开方式"

官方目标（whycymel）：比 MEL 更面向对象、比 API 更顺手、**比 PyMEL 更轻更快**。

- **数学类是最大卖点**：Vector / Matrix / Quaternion / EulerRotation / Transformation 等 datatypes 专门为**绑定场景**充实了功能（作者本人是绑定 TA，痛点驱动）
- 行为保证严格（"信頼性高く、お行儀よく"）：
  - 所有修改操作**保证可 undo**
  - 不改 Maya 设置、不埋 scriptJob / MMessage 回调
  - 不持有 Networked Plug（避免经典的 plug 失效坑）
- 明确的"不做"清单：**不支持组件（component）**、不包裹 cmds 命令、不追求大而全
- 远期计划核心换 C++ 实现（cymel 的 C = C++ 的 C），Python 版将长期保留可切换

### cmdx —— "为每帧跑几千次的代码而生"

- 为**性能关键的运行时任务**设计：监听大量事件、每帧读写数千属性、插件 `compute()` / `draw()` 内调用
- 实测比 PyMEL 平均快 **140x**（最高 1300x），比 cmds 快 2.5x
- 特色功能：
  - 持久节点引用（hashable，可当 dict key）
  - Node / Plug 重用缓存（`CMDX_ENABLE_NODE_REUSE`）
  - **Transactions**：Modifier 批量提交修改
  - 声明式插件框架（superclass 直接写 Maya 插件）
  - 单位显式处理、PEP8 双语法（`camelCase` / `snake_case` 均可）
- undo 依赖把自身注册为 command plug-in —— **vendoring 多副本共存时需重命名**（如 `cmdx_mytool.py`，README 有专门章节）
- 只覆盖 cmds 的一个子集（YAGNI 哲学），组件 / UI 一概不管

## 三、选型建议（绑定 TA 视角）

### 日常绑定工具开发 → cymel

- 从 pymel 迁移成本最低，心智模型几乎一样（`cm.nt.Transform`、`node.attr('tx')`），却没有 PyMEL 的启动慢和运行慢
- 绑定向数学类（四元数、矩阵分解、Transformation）对约束 / 空间切换 / 姿态镜像类工具是直接生产力
- "保证 undo、不污染场景"的设计适合发给动画师的工具

### 性能敏感场景 → cmdx

- 实时性任务（每帧回调、批量处理数千节点属性、OpenMaya 插件 compute 内部逻辑），节点重用 + Modifier 事务是量级优势
- 单文件适合塞进工具包随包分发（如 X12RigAnimTools），不添加外部依赖

### 注意事项

- cymel **不支持组件** —— 刷权重、顶点级操作仍需掉回 OpenMaya / cmds
- cmdx 的 undo 是插件机制实现，多工具各 vendor 一份时按官方建议重命名模块
- 两者都不管 UI，PySide 部分照旧
- 实践中常见组合：**工具层 cymel/pymel 风格 + 热点路径 cmdx**

## 相关

- [PyMEL 官方 Why PyMEL?](https://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/PyMel/why_pymel.html)
- 类似的新库：[mayax](https://github.com/chirieac/mayax)（设计与 cmdx 相近）
