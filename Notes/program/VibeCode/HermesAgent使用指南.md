# Hermes Agent 使用指南

> Hermes Agent 是 Nous Research 开源的 AI Agent 框架，与 Claude Code、Codex CLI 同属一类——自主执行任务的编程/通用助手。本指南面向 Claude Code 老用户，以 **Desktop 桌面客户端** 为主要使用场景。
>
> 官方文档（最权威）：https://hermes-agent.nousresearch.com/docs

---

## 一、认识 Hermes：与 Claude Code 的核心差异

| 维度 | Claude Code | Hermes Agent |
|------|-------------|--------------|
| 模型 | 仅 Anthropic Claude | **任意提供商**（OpenRouter、Anthropic、OpenAI、Google、DeepSeek、xAI、本地模型等 20+ 家），可随时切换 |
| 运行界面 | 终端 CLI | 终端 CLI / TUI / **原生桌面应用** / Web 面板 / IDE（ACP） |
| 消息平台 | 无 | **网关（Gateway）**：Telegram、Discord、Slack、微信、飞书、钉钉、邮件等 20+ 平台 |
| 记忆 | 会话内 + CLAUDE.md | **跨会话持久记忆** + 历史会话全文检索 |
| 技能积累 | 手工维护 CLAUDE.md | **Skills 系统**：自动保存、检索、安装、发布可复用流程 |
| 定时任务 | 无 | 内置 **cron 调度**（定时提醒、监控、日报） |
| 多实例 | 无 | **Profiles** + 多智能体协作（delegation、kanban） |
| 项目规则文件 | `CLAUDE.md` | `.hermes.md`，**兼容 `AGENTS.md`、`CLAUDE.md`、`.cursorrules`** |
| 扩展 | MCP | MCP + 插件 + 自定义工具 + Webhook |

**好消息**：项目目录下的 `CLAUDE.md` 在 Hermes 里直接生效，不用迁移。

---

## 二、安装与初始配置

```bash
# 方式一：shell 安装脚本（自动配置 uv、Python、虚拟环境）
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# 方式二：PyPI
pip install hermes-agent      # 或 uv pip install hermes-agent
```

首次配置（终端执行一次即可，之后日常用桌面客户端）：

```bash
hermes setup       # 交互式配置向导（模型、终端、工具等）
hermes model       # 选择模型 + 提供商
hermes auth        # 管理 OAuth / API Key 凭据
hermes doctor      # 健康检查
```

- 配置文件：`~/.hermes/config.yaml`（`hermes config edit` 编辑）
- API Key：`~/.hermes/.env`
- Windows 实际位置：`C:\Users\<用户名>\AppData\Local\hermes\`（用 `hermes config path` 确认）

---

## 三、Desktop 桌面客户端使用指南 ⭐

启动方式：`hermes desktop`（或 `hermes gui`），也可用系统的应用快捷方式。

### 3.1 界面布局

- **侧边栏**：会话列表 + **Projects（项目）**切换。项目是绑定到某个目录的命名工作区（如 X12RigAnimTools、Learning-Notes），切换项目 = 切换工作目录 + 自动加载该目录的 CLAUDE.md/AGENTS.md 规则
- **主聊天区**：完整 GitHub 风味 Markdown 渲染——表格、代码高亮、数学公式、任务列表；图片/音频/视频**内嵌显示播放**，文件以下载链接形式交付
- **状态栏**：模型选择器（点击即可跨提供商换模型）
- **后台终端标签页**：Agent 启动的后台进程（如服务器、长任务）会以只读终端 tab 形式实时展示输出

### 3.2 核心操作

| 操作             | 方式                            |
| -------------- | ----------------------------- |
| 命令面板           | **Cmd/Ctrl + K**（快速跳转会话、执行动作） |
| 发送文件/图片给 Agent | **直接拖拽**进聊天窗口，或剪贴板粘贴截图        |
| 换模型            | 点状态栏模型选择器，或 `/model 名称`       |
| 中断任务           | `/stop`；不打断插话用 `/steer 指令`    |
| 快捷键            | 可自定义重绑定                       |
| 桌面通知           | 原生系统通知（长任务完成、定时任务送达）          |
| 子智能体监控         | Agent 派生子任务时有实时 watch 窗口      |
| 主题             | 支持 VS Code Marketplace 主题     |

### 3.3 桌面端特色能力

- **多会话并行**：侧边栏开多个会话同时进行不同任务，互不干扰
- **远程网关登录**：本地轻量 GUI 可登录远程机器上的 Hermes（OAuth 或账密），"瘦客户端驱动重服务端"
- **与 CLI 共享一切**：会话、记忆、技能、配置全部通用，桌面开的会话可以在 CLI 用 `hermes --resume` 继续

### 3.4 桌面端使用建议

1. 为常用代码库/知识库建 Project，避免每次报路径
2. 长任务放心切走——完成时会有系统通知
3. 截图直接粘贴，让 Agent 看图（UI 报错、节点图等）
4. 要看 Agent 跑的后台服务日志，直接点对应终端 tab

---

## 四、斜杠命令大全（桌面端适用）

桌面客户端与 CLI 共享同一套命令注册表，绝大多数命令通用。会话内输入 `/help` 可查看当前环境的权威列表。

### 4.1 会话控制

| 命令 | 说明 |
|------|------|
| `/new`（`/reset`） | 开新会话 |
| `/retry` | 重发上一条消息 |
| `/undo` | 撤销上一轮对话 |
| `/title 名称` | 给会话命名 |
| `/resume [名称]` | 恢复指定会话 |
| `/branch`（`/fork`） | 从当前会话分叉出新会话 |
| `/compress` | 手动压缩上下文（≈ Claude Code 的 `/compact`） |
| `/stop` | 终止后台进程/当前任务 |
| `/steer 指令` | **不打断任务**，在下一次工具调用后插入指令 |
| `/queue 指令` | 排队到下一轮执行 |
| `/background 指令` | 后台运行一个任务 |
| `/goal 目标` | 设定跨轮次持续推进的长期目标（`status/pause/resume/clear`） |
| `/agents`（`/tasks`） | 查看活跃的子 Agent 和运行中任务 |
| `/rollback [N]` | 恢复文件系统检查点（需启用 checkpoints） |

### 4.2 配置与模型

| 命令                    | 说明                                                |
| --------------------- | ------------------------------------------------- |
| `/model [名称]`         | 查看/切换模型（可跨提供商）                                    |
| `/reasoning [级别]`     | 推理强度：none/minimal/low/medium/high/xhigh/show/hide |
| `/verbose`            | 循环切换输出详细度                                         |
| `/personality [名称]`   | 设置人格                                              |
| `/voice [on/off/tts]` | 语音模式                                              |
| `/yolo`               | 切换危险命令免确认                                         |

### 4.3 工具与技能

| 命令                      | 说明                            |
| ----------------------- | ----------------------------- |
| `/skill 名称`             | 手动加载技能到当前会话                   |
| `/reload-skills`        | 重新扫描技能目录                      |
| `/reload-mcp`           | 重载 MCP 服务器                    |
| `/learn <来源>`           | **从任意来源学习技能**：目录、URL、当前对话、笔记  |
| `/journey`（`/learning`） | 打开学习历程时间线（记忆+技能的积累回顾）         |
| `/curator [子命令]`        | 技能管家：status/run/pin/archive 等 |

### 4.4 信息查看

| 命令 | 说明 |
|------|------|
| `/help` | 命令列表 |
| `/usage` | Token 用量 |
| `/insights [天数]` | 使用分析 |
| `/profile` | 当前 profile 信息 |
| `/debug` | 生成调试报告（系统信息+日志） |

### 4.5 Claude Code 命令对照速查

| Claude Code | Hermes | 备注 |
|-------------|--------|------|
| `/clear` | `/new` | 开新会话 |
| `/compact` | `/compress` | 压缩上下文 |
| `/model` | `/model` | Hermes 可跨提供商 |
| `/memory`（编辑 CLAUDE.md） | 直接说"记住……" | 自动持久记忆 |
| `/rewind` | `/rollback` | 文件检查点回滚 |
| Esc 中断 | `/stop` 或 `/steer` | steer 不打断 |
| — | `/learn`、`/journey`、`/goal`、`/branch` | Hermes 独有 |

### 4.6 重要概念辨析：记住 vs /learn vs /journey

- **"请记住……"** → 写入**记忆（Memory）**：陈述性事实（偏好、环境、个人信息），每次对话自动注入
- **`/learn`** → 生成**技能（Skill）**：可复用的操作流程（步骤、命令、坑点），任务匹配时按需加载。素材可以是目录、URL、当前对话、笔记
- **`/journey`** → 只读的**时间线视图**，回顾记忆和技能的积累历史

一句话：记住存**事实**，learn 存**方法**，journey 看**历史**。

> Agent 完成复杂任务后主动提议"保存为技能"= `/learn` 的被动触发形式，产物相同。

---

## 五、核心功能详解

### 5.1 持久记忆（Memory）

自动记住偏好、环境、纠正过的错误，跨会话生效。直接说"记住……"即可。

```bash
hermes memory status / setup    # 查看状态 / 配置后端（内置/Honcho/Mem0）
```

配套 **session_search**：Agent 可全文检索所有历史会话——"上次那个 bug 怎么修的"它自己能查。

### 5.2 技能系统（Skills）

```bash
hermes skills list             # 已安装技能
hermes skills search 关键词    # 搜索技能中心
hermes skills install ID       # 安装
hermes skills browse           # 浏览全部
```

### 5.3 项目（Projects）与规则文件

**Projects**：桌面端侧边栏可切换的命名工作区，绑定到目录。对话中说"把 XX 目录注册为项目"即可创建。

**规则文件加载优先级**（只取第一个命中的）：

1. `.hermes.md` / `HERMES.md` —— 向上遍历父目录到 git 根，支持分层规则
2. `AGENTS.md` —— 仅当前目录（跨工具通用，新项目推荐）
3. `CLAUDE.md` —— 仅当前目录（旧文件直接可用）
4. `.cursorrules`

单文件上限 20,000 字符。注意：Hermes **不读** `~/.claude/CLAUDE.md` 全局文件——全局偏好应存入记忆或 `SOUL.md`。

### 5.4 定时任务（Cron）

```bash
hermes cron create "0 9 * * *"    # 支持 "30m"、"every 2h"、自然语言
hermes cron list / pause / resume / remove
```

对话中直接说"每天早 9 点给我汇总 XX"也能创建。

### 5.5 消息平台网关（Gateway）

同一个 Agent 挂到微信、Telegram、Discord、飞书、钉钉、邮件等，手机远程指挥，带完整工具权限。

```bash
hermes gateway setup / install / start
```

### 5.6 子智能体与多 Agent

- **delegate_task**：会话内派生子 Agent 并行处理（桌面端有实时监控窗口）
- **独立进程**：`hermes chat -q "..."` 后台跑完整实例；`-w` worktree 模式多 Agent 并行改同一仓库不冲突
- **kanban**：多 Agent 共享任务看板

### 5.7 Profiles、MCP、工具集

```bash
hermes profile create work && hermes -p work   # 多套独立配置
hermes mcp add/list/test/serve                 # MCP 客户端 + 可作为 MCP server
hermes tools                                   # 工具集开关（新会话生效）
```

---

## 六、CLI 速查（偶尔用终端时）

| 用途 | 命令 |
|------|------|
| 交互会话 | `hermes` |
| 单次提问 | `hermes chat -q "问题"`（≈ `claude -p`） |
| 继续上次 | `hermes --continue` / `-c` |
| 恢复指定会话 | `hermes --resume <ID或标题>` |
| 免确认模式 | `hermes --yolo` |
| worktree 隔离 | `hermes -w` |
| 预加载技能 | `hermes -s 技能名` |
| 指定 profile | `hermes -p 名称` |
| 桌面应用 | `hermes desktop` |
| Web 面板 | `hermes dashboard` |
| 升级 | `hermes update` |

---

## 七、安全与权限

| 场景 | 设置 |
|------|------|
| 危险命令确认（默认开） | `approvals.mode: manual` |
| 小模型自动放行低风险命令（推荐） | `hermes config set approvals.mode smart` |
| 全部跳过 | `/yolo` 或 `approvals.mode: off` |
| 密钥自动脱敏（默认开） | `security.redact_secrets` |
| 文件检查点回滚 | 启用 checkpoints 后 `/rollback` |

---

## 八、关键路径速查

```
~/.hermes/config.yaml      主配置
~/.hermes/.env             API Key 等密钥
~/.hermes/skills/          已安装技能
~/.hermes/state.db         会话存储（SQLite）
~/.hermes/logs/            日志（网关问题先看 gateway.log）
~/.hermes/profiles/<名>/   各 profile 独立目录
```

Windows 实际在 `C:\Users\<用户名>\AppData\Local\hermes\`。

---

## 九、常见问题（Troubleshooting）

- **改配置不生效** → 桌面端/CLI 重启；工具/技能变更需 `/new` 新会话（保护 prompt 缓存）
- **模型报错** → `hermes doctor`；`hermes auth` 重新认证；检查 `.env`
- **技能没加载** → `hermes skills list` 确认；`/skill 名称` 手动加载
- **Windows：Alt+Enter 换行无效（CLI）** → 用 **Ctrl+Enter**
- **Windows：首次运行 "No models provided"** → config.yaml 存成了 UTF-8 BOM，用 `hermes config edit` 重存

---

## 十、迁移建议（Claude Code → Hermes）

1. 项目 `CLAUDE.md` 不用动；全局 `~/.claude/CLAUDE.md` 的内容改存**记忆**（对话中让它记住即可）
2. `hermes setup` + `hermes model` 配好模型，`hermes doctor` 确认健康
3. `approvals.mode` 设为 `smart`——接近 Claude Code 的权限体验但少打扰
4. 日常用桌面客户端：建 Projects、粘贴截图、后台任务等通知
5. 主动积累：说"记住……"、用 `/learn` 沉淀流程，越用越顺手
6. 进阶体验 Gateway——Agent 接到手机 IM，相对 Claude Code 最大的升级

---

*基于 Hermes Agent 官方文档整理，命令如有出入以 `/help`、`hermes --help` 和官方文档为准。*

相关笔记：[MOC-program](../MOC-program.md)
