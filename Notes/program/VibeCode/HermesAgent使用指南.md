# Hermes Agent 使用指南（写给 Claude Code 用户）

> Hermes Agent 是 Nous Research 开源的 AI Agent 框架，与 Claude Code、Codex CLI 同属一类——在终端里自主执行任务的编程/通用助手。本指南假设你熟悉 Claude Code，重点讲"对应关系"和"Hermes 独有的东西"。
>
> 官方文档（最权威）：https://hermes-agent.nousresearch.com/docs

---

## 1. 核心差异一览：Claude Code vs Hermes Agent

| 维度 | Claude Code | Hermes Agent |
|------|-------------|--------------|
| 模型 | 仅 Anthropic Claude | **任意提供商**（OpenRouter、Anthropic、OpenAI、Google、DeepSeek、xAI、本地模型等 20+ 家），可随时切换 |
| 运行界面 | 终端 CLI | 终端 CLI / TUI / **原生桌面应用** / Web 面板 / IDE（ACP） |
| 消息平台 | 无 | **网关（Gateway）**：Telegram、Discord、Slack、微信、飞书、钉钉、邮件等 20+ 平台，带完整工具权限 |
| 记忆 | 会话内 + CLAUDE.md | **跨会话持久记忆** + 历史会话全文检索 |
| 技能/经验积累 | 手工维护 CLAUDE.md | **Skills 系统**：可自动保存、检索、安装、发布可复用流程 |
| 定时任务 | 无 | 内置 **cron 调度**（定时提醒、监控、日报） |
| 多实例 | 无 | **Profiles**（多套独立配置/会话/技能）+ 多智能体协作（delegation、kanban） |
| 项目规则文件 | `CLAUDE.md` | `.hermes.md` / `HERMES.md`，**同时兼容 `AGENTS.md`、`CLAUDE.md`、`.cursorrules`** |
| 扩展 | MCP | MCP + 插件 + 自定义工具 + Webhook |

**好消息**：你的 `CLAUDE.md` 在 Hermes 里直接生效，不用迁移。

---

## 2. 安装与初始配置

```bash
# 方式一：shell 安装脚本（自动配置 uv、Python、虚拟环境）
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# 方式二：PyPI
pip install hermes-agent      # 或 uv pip install hermes-agent
```

首次配置：

```bash
hermes setup       # 交互式配置向导（模型、终端、工具等）
hermes model       # 选择模型 + 提供商（交互式）
hermes auth        # 管理 OAuth / API Key 凭据
hermes doctor      # 健康检查，排查依赖和配置问题
```

API Key 写在 `~/.hermes/.env`，配置写在 `~/.hermes/config.yaml`（用 `hermes config edit` 编辑）。

---

## 3. 日常使用（对照 Claude Code 习惯）

### 启动会话

| 你在 Claude Code 里做的 | Hermes 里的等价操作 |
|------------------------|---------------------|
| `claude` | `hermes` |
| `claude -p "问题"` | `hermes chat -q "问题"` |
| `claude --continue` | `hermes --continue`（或 `-c`） |
| `claude --resume <id>` | `hermes --resume <会话ID或标题>` |
| `claude --dangerously-skip-permissions` | `hermes --yolo` |
| `claude --model xxx` | `hermes chat -m anthropic/claude-sonnet-4` |

其他常用启动参数：

```bash
hermes -w                  # git worktree 隔离模式（多 agent 并行改代码不冲突）
hermes -s skill_name       # 预加载技能
hermes -p work             # 使用名为 work 的 profile
hermes desktop             # 启动桌面应用
hermes dashboard           # 启动 Web 管理面板
```

### 会话内斜杠命令（对照表）

| Claude Code | Hermes | 说明 |
|-------------|--------|------|
| `/clear` | `/new` 或 `/clear` | 开新会话 |
| `/compact` | `/compress` | 手动压缩上下文 |
| `/model` | `/model [名称]` | 查看/切换模型（**可跨提供商切换**） |
| `/help` | `/help` | 命令列表 |
| `/config` | `/config` | 查看配置 |
| `/memory` (编辑 CLAUDE.md) | 记忆是自动的；也可直接说"记住……" | 持久记忆 |
| Esc 中断 | `/stop`、`/steer <指令>` | `/steer` 可以在不打断的情况下中途插入指令 |
| — | `/undo` | 撤销上一轮对话 |
| `/rewind` | `/rollback [N]` | 恢复文件系统检查点（需 `--checkpoints` 启动） |
| — | `/branch` | 从当前会话分叉 |
| `/vim`、主题等 | `/skin`、`/verbose`、`/reasoning` | 界面与输出控制 |
| — | `/queue <指令>` | 排队到下一轮执行 |
| — | `/goal <目标>` | 设定跨轮次持续推进的长期目标 |
| — | `/handoff telegram` | 把当前会话交接到消息平台继续聊 |

### 项目规则文件

Hermes 按以下优先级加载（**只取第一个命中的**）：

1. `.hermes.md` / `HERMES.md` —— 会向上遍历父目录直到 git 根，支持分层规则
2. `AGENTS.md` —— 仅当前目录（跨工具通用，推荐新项目用这个）
3. `CLAUDE.md` —— 仅当前目录（**你的旧文件直接可用**）
4. `.cursorrules` / `.cursor/rules/*.mdc`

单文件上限 20,000 字符，超出会截断。用 `hermes --ignore-rules` 可临时跳过全部规则文件。

---

## 4. Hermes 独有的重点功能

### 4.1 持久记忆（Memory）

Hermes 自动记住你的偏好、环境信息、纠正过的错误，**跨会话生效**。直接对它说"记住我喜欢简洁回答"即可。管理命令：

```bash
hermes memory status     # 查看记忆状态
hermes memory setup      # 配置记忆后端（内置 / Honcho / Mem0 等）
```

还有 **session_search**：Agent 可以全文检索你的所有历史会话，问它"上次我们那个 bug 怎么修的"它能自己查。

### 4.2 技能系统（Skills）

Skills 是可复用的流程文档（类似把 CLAUDE.md 的经验模块化）。Hermes 完成复杂任务后会主动提议保存为技能，下次遇到同类任务自动加载。

```bash
hermes skills list             # 已安装技能
hermes skills search 关键词    # 搜索技能中心
hermes skills install ID       # 安装
hermes skills browse           # 浏览全部
```

会话内：`/skill 名称` 手动加载某个技能。

### 4.3 定时任务（Cron）

让 Agent 定时干活并把结果发给你：

```bash
hermes cron create "0 9 * * *"    # 也支持 "30m"、"every 2h"、自然语言
hermes cron list / pause / resume / remove
```

例：每天早 9 点汇总技术新闻发到你的 Telegram。

### 4.4 消息平台网关（Gateway）

同一个 Agent 挂到微信、Telegram、Discord、飞书、钉钉、邮件……手机上随时指挥它，且带完整工具权限（可以远程让它跑命令、改代码）。

```bash
hermes gateway setup      # 配置平台
hermes gateway install    # 装成后台服务
hermes gateway start      # 启动
```

### 4.5 子智能体与多 Agent

- **delegate_task 工具**：会话内让 Agent 派生子 Agent 并行处理子任务（类似 Claude Code 的 subagent/Task，但可并行、可指定 orchestrator 角色）。
- **spawn 独立进程**：`hermes chat -q "..."` 后台运行完整实例；配合 `-w` worktree 模式多 Agent 并行改同一仓库。
- **kanban**：`hermes kanban` 提供多 Agent 共享的任务看板（工作队列）。

### 4.6 Profiles（多套配置）

```bash
hermes profile create work     # 建独立 profile（独立配置/会话/技能/记忆）
hermes -p work                 # 用它启动
hermes profile use work        # 设为默认
```

适合区分"工作/个人"或不同模型配置。

### 4.7 MCP 支持

和 Claude Code 一样支持 MCP，且 Hermes 自己也能作为 MCP server：

```bash
hermes mcp add NAME --url ... / --command ...
hermes mcp list / test / configure
hermes mcp serve               # 把 Hermes 暴露为 MCP server
```

### 4.8 工具集管理

Claude Code 工具是固定的；Hermes 的工具按 toolset 开关：

```bash
hermes tools            # 交互式开关（web、browser、terminal、file、vision、
                        # image_gen、tts、memory、delegation、cronjob……）
hermes tools enable browser
```

注意：工具变更在 **新会话**（`/new`）才生效，为了不破坏 prompt 缓存。

---

## 5. 安全与权限

| 场景 | 设置 |
|------|------|
| 危险命令确认（默认开启，类似 Claude Code 的 permission 提示） | `approvals.mode: manual` |
| 用小模型自动放行低风险命令 | `hermes config set approvals.mode smart`（推荐） |
| 全部跳过 | `hermes --yolo` 或 `approvals.mode: off` |
| 密钥自动脱敏（工具输出中的 API Key 会被遮蔽，默认开） | `security.redact_secrets` |
| 文件系统检查点（可回滚） | `hermes --checkpoints` 启动，会话内 `/rollback` |

---

## 6. 关键路径速查

```
~/.hermes/config.yaml      主配置
~/.hermes/.env             API Key 等密钥
~/.hermes/skills/          已安装技能
~/.hermes/state.db         会话存储（SQLite）
~/.hermes/logs/            日志（排查网关问题先看 gateway.log）
~/.hermes/profiles/<名>/   各 profile 独立目录
```

Windows 下位于 `C:\Users\<用户名>\AppData\Local\hermes\`（或 `~/.hermes`，视安装方式而定，用 `hermes config path` 确认）。

---

## 7. 常见问题（Troubleshooting）

- **改了配置不生效** → CLI 需退出重启；网关用 `/restart`；工具/技能变更需 `/new` 新会话。
- **模型报错** → `hermes doctor` 体检；`hermes auth` 重新认证；检查 `.env` 里的 Key。
- **技能没加载** → `hermes skills list` 确认已装；`/skill 名称` 手动加载。
- **Windows 下 Alt+Enter 换行无效** → 改用 **Ctrl+Enter**。
- **首次运行报 "No models provided"（Windows）** → config.yaml 被记事本存成了 UTF-8 BOM，用 `hermes config edit` 重新保存。

---

## 8. 给 Claude Code 老用户的迁移建议

1. **CLAUDE.md 不用动**，Hermes 直接读；新项目建议改用 `AGENTS.md`（跨工具通用）或 `.hermes.md`（要分层规则时）。
2. 先跑 `hermes setup` + `hermes model` 把模型配好，再 `hermes doctor` 确认健康。
3. 把 `approvals.mode` 设为 `smart`，体验接近 Claude Code 的权限提示但少打扰。
4. 主动使用记忆和技能：说"记住……"、任务完成后同意它"保存为技能"，用得越久越顺手。
5. 试试 gateway——把 Agent 接到你的手机 IM 上，是相对 Claude Code 最大的体验升级。
6. 从 OpenClaw 迁移可用 `hermes claw migrate`；随时 `hermes update` 升级。

---

*本指南基于 Hermes Agent 官方文档整理，命令如有出入以 `hermes --help` 和官方文档为准。*
