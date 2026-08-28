# Claude Code 使用指南

> Claude Code 是 Anthropic 推出的 AI 驱动的命令行编程助手，能够直接在终端中理解代码库、执行任务、调试问题，是开发者的智能编程搭档。

---

## 目录

1. 安装与配置
2. 启动与基本交互
3. 核心指令速查
4. 文件与代码操作
5. Git 工作流集成
6. 项目理解与分析
7. 调试与测试
8. 自定义配置（CLAUDE.md / settings.json）
9. 记忆系统与上下文管理
10. Plan 模式与权限模式
11. 自定义斜杠命令（Slash Commands）
12. 子代理（Subagents）
13. Hooks 钩子系统
14. MCP（Model Context Protocol）外部工具集成
15. Skills 技能系统
16. 会话管理（恢复 / 继续 / 压缩）
17. IDE 与编辑器集成
18. 非交互式（Headless）模式
19. 高级用法与技巧
20. 常见问题

---

## 一、安装与配置

### 系统要求

|环境|要求|
|---|---|
|操作系统|macOS / Linux / Windows (WSL)|
|Node.js|>= 18.0.0|
|网络|需要访问 Anthropic API|

### 安装步骤

```bash
# 通过 npm 全局安装
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version
```

### API 密钥配置

```bash
# 方式一：环境变量（推荐）
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxxxxx"

# 方式二：写入 shell 配置文件（永久生效）
echo 'export ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxxxxx"' >> ~/.zshrc
source ~/.zshrc

# 方式三：在启动时交互式输入
claude  # 首次运行时会提示输入 API Key
```

---

## 二、启动与基本交互

### 启动方式

```bash
# 在当前目录启动（最常用）
claude

# 直接传入任务，进入交互模式并附带初始 prompt
claude "帮我解释这个项目的结构"

# 非交互（headless）执行并退出，常用于脚本 / CI
claude -p "列出所有 TODO 注释所在文件和行号"

# 恢复最近一次会话
claude --continue
claude -c              # 简写

# 从历史会话列表中选择恢复
claude --resume
claude -r              # 简写

# 指定默认模型（可选 opus / sonnet / haiku，或完整 model id）
claude --model sonnet

# 指定权限模式启动
claude --permission-mode plan            # 进入 Plan 模式
claude --permission-mode acceptEdits     # 自动接受文件编辑

# 允许 / 禁止特定工具
claude --allowedTools "Read,Edit,Bash(git status)"
claude --disallowedTools "Bash"

# 追加系统指令（用于临时约束行为）
claude --append-system-prompt "所有回答请使用简体中文"

# 自动同意所有工具权限（谨慎使用 / 仅限受信任沙箱）
claude --dangerously-skip-permissions
```

### 交互界面说明

```
> ← 这是你的输入提示符，在此输入指令或问题

Claude will respond here...
esc  ← 按 ESC 中断当前生成
```

### 退出方式

```bash
exit      # 输入 exit 退出
# 或按 Ctrl + C / Ctrl + D
```

---

## 三、核心指令速查

### Slash 命令（斜杠指令）

在对话框中直接输入以下命令：

| 指令                   | 说明                                   |
| -------------------- | ------------------------------------ |
| `/help`              | 显示帮助信息和可用命令列表                        |
| `/clear`             | 清除当前对话上下文，开始新会话                      |
| `/compact`           | 压缩对话历史，节省 Token，保留核心上下文（可附加指令引导压缩重点） |
| `/cost`              | 查看当前会话的 Token 消耗和费用估算                |
| `/status`            | 显示当前状态、模型信息和配置                       |
| `/model`             | 切换使用的模型（Opus / Sonnet / Haiku）       |
| `/config`            | 打开交互式配置面板（主题、模型、通知等）                 |
| `/init`              | 为当前项目自动生成 `CLAUDE.md` 项目说明文件         |
| `/memory`            | 查看 / 编辑当前的记忆文件（CLAUDE.md 与个人记忆）      |
| `/agents`            | 查看、创建、管理子代理（Subagents）               |
| `/mcp`               | 查看与管理 MCP 服务器连接状态                    |
| `/permissions`       | 查看 / 修改工具权限（allowed / denied tools）  |
| `/hooks`             | 查看与编辑 Hooks 配置                       |
| `/login` / `/logout` | 登录或登出 Anthropic 账户（订阅模式）             |
| `/resume`            | 恢复之前的会话（按列表选择）                       |
| `/review`            | 发起对当前 PR / 改动的代码审查                   |
| `/vim`               | 切换 Vim 键位模式输入                        |
| `/bug`               | 向 Anthropic 反馈问题（自动附带会话上下文）          |
| `/exit` 或 `/quit`    | 退出 Claude Code                       |

> 使用 `#` 开头可快速将一条信息**写入项目记忆 (CLAUDE.md)**，例如：`# 本项目所有时间戳使用 UTC`。
> 使用 `!` 开头可在 REPL 中直接执行一条 shell 命令，例如：`!git status`。
> 使用 `@路径` 可快速引用某个文件作为上下文，例如：`@src/main.py 解释这个文件`。

### 快捷键

|快捷键|功能|
|---|---|
|`↑ / ↓`|翻阅历史输入|
|`Esc`|中断当前响应|
|`Esc Esc`（双击）|回退到上一条用户消息（编辑后重发）|
|`Ctrl + C`|强制中止或退出|
|`Ctrl + D`|退出会话|
|`Ctrl + L`|清屏|
|`Ctrl + R`|搜索历史输入|
|`Tab`|自动补全文件路径 / 命令|
|`Shift + Tab`|切换权限模式（Default / Auto-accept / Plan）|
|`\` + `Enter`|在输入框中插入换行|
|`Ctrl + V`|粘贴（在支持的终端中可粘贴图片用于多模态分析）|

---

## 四、文件与代码操作

### 读取与理解文件

```
# 让 Claude 读取并解释指定文件
请阅读 src/main.py 并解释它的主要逻辑

# 分析目录结构
解释一下整个 src/ 目录的架构

# 对比两个文件
对比 config.dev.json 和 config.prod.json 的差异
```

### 创建与修改文件

```
# 创建新文件
帮我在 src/utils/ 下创建一个 logger.py，实现带时间戳的日志记录功能

# 修改现有文件
修改 components/Button.tsx，添加 disabled 状态的样式支持

# 重构代码
重构 utils/data_parser.py，将其中的嵌套循环用列表推导式优化
```

### 批量操作

```
# 批量修改
将项目中所有 console.log 替换为使用 logger 模块的调用

# 批量创建
为 src/models/ 目录下所有模型文件生成对应的单元测试文件
```

---

## 五、Git 工作流集成

Claude Code 可以直接操作 Git，执行完整的版本控制工作流。

### 常用 Git 操作

```
# 查看当前改动
查看我修改了哪些文件，改动内容是什么？

# 生成 commit message
根据我的代码改动，帮我生成一个规范的 commit message

# 执行提交
将所有改动暂存并提交，使用合适的 commit 信息

# 创建分支
从 main 分支创建一个新的 feature/user-auth 分支

# 查看日志
展示最近 10 条 commit 历史，并简要说明每次改动
```

### 代码审查

```
# Review 改动
Review 我在这次 commit 中的代码，指出潜在问题

# 分析 diff
分析当前 staged 的改动，有没有遗漏的边界情况？
```

---

## 六、项目理解与分析

### 快速了解陌生项目

```
# 项目概览（推荐第一步）
这是什么项目？帮我梳理它的整体架构和技术栈

# 入口分析
项目的入口文件在哪里？数据流是怎样的？

# 依赖分析
分析 package.json / requirements.txt，解释各依赖的用途

# 找关键模块
哪个模块负责用户认证？帮我找到相关代码
```

### 代码质量分析

```
# 全面分析
扫描整个项目，找出代码质量问题、反模式和潜在的 bug

# 性能分析
分析 src/data/ 目录下的代码，找出可能的性能瓶颈

# 安全审查
检查项目中是否存在常见的安全漏洞（SQL注入、XSS等）
```

---

## 七、调试与测试

### 错误调试

```
# 粘贴报错信息
我运行时遇到了以下错误，帮我分析原因并修复：
[粘贴错误堆栈信息]

# 运行并调试
运行 python main.py，如果有报错帮我修复

# 逻辑调试
这个函数的输出不符合预期，帮我找出逻辑错误：
[粘贴代码]
```

### 测试相关

```
# 生成单元测试
为 src/utils/calculator.py 中的所有函数编写完整的单元测试

# 运行测试
运行项目的测试套件，并告诉我哪些测试失败了

# 测试覆盖率
分析当前测试覆盖率，找出缺少测试的关键模块

# 修复失败的测试
帮我修复 tests/test_auth.py 中失败的测试用例
```

---

## 八、自定义配置（CLAUDE.md / settings.json）

### CLAUDE.md 项目配置文件

在项目根目录创建 `CLAUDE.md`，Claude 每次启动会自动读取，用于传达项目规范、技术栈、约束等：

```markdown
# 项目规范（CLAUDE.md 示例）

## 技术栈
- 语言：Python 3.11
- 框架：FastAPI
- 数据库：PostgreSQL + SQLAlchemy

## 代码规范
- 遵循 PEP 8 规范
- 所有函数必须添加类型注解
- 公共函数必须有 docstring

## 命名约定
- 变量/函数：snake_case
- 类名：PascalCase
- 常量：UPPER_SNAKE_CASE

## 禁止事项
- 不要直接修改 migrations/ 目录
- 不要在代码中硬编码任何密钥或密码
```

> **CLAUDE.md 的加载层级**（按优先级从高到低合并）：
> 1. 项目根目录 `./CLAUDE.md`（团队共享，提交到 git）
> 2. 项目根目录 `./CLAUDE.local.md`（个人私有，建议 gitignore）
> 3. 父目录链上的 `CLAUDE.md`（向上递归查找，适合 monorepo）
> 4. 用户级 `~/.claude/CLAUDE.md`（个人在所有项目通用）
>
> 在文件中可使用 `@path/to/file.md` 语法**引用**其他 markdown 片段，便于模块化拆分规范。
> 使用 `/init` 命令可自动扫描项目并生成初版 `CLAUDE.md`。

### settings.json 配置层级

|位置|作用域|
|---|---|
|`~/.claude/settings.json`|**用户全局配置**（所有项目共用）|
|`<项目>/.claude/settings.json`|**项目共享配置**（建议提交到 git）|
|`<项目>/.claude/settings.local.json`|**项目个人配置**（自动 gitignore）|
|`<企业策略路径>/managed-settings.json`|**企业管理策略**（优先级最高，由管理员下发）|

### settings.json 常用字段

```json
{
  "model": "claude-opus-4-7",
  "theme": "dark",
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
    "ANTHROPIC_AUTH_TOKEN": "sk-xxxxxxxx",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  },
  "permissions": {
    "allow": [
      "Read",
      "Edit",
      "Bash(git status)",
      "Bash(git diff:*)",
      "Bash(npm test:*)"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(git push --force:*)"
    ],
    "additionalDirectories": ["../shared-libs"]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "prettier --write $CLAUDE_FILE_PATHS" }
        ]
      }
    ]
  },
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    }
  }
}
```

### 权限控制（--allowedTools / --disallowedTools）

权限规则支持**通配模式**，可以精细到具体子命令：

```bash
# 仅允许读取与编辑，禁止任意 Bash
claude --allowedTools "Read,Edit"

# 允许特定的 Bash 子命令（注意冒号 + 星号语法）
claude --allowedTools "Bash(git status),Bash(git diff:*),Bash(npm test:*)"

# 黑名单：禁止特定危险命令
claude --disallowedTools "Bash(rm -rf:*),Bash(git push --force:*)"
```

在交互中可用 `/permissions` 命令实时调整本会话权限。

---

## 九、记忆系统与上下文管理

Claude Code 提供分层的"记忆"机制，让模型在跨会话间保留必要的上下文：

|层级|文件|用途|
|---|---|---|
|项目共享记忆|`./CLAUDE.md`|项目规范、技术栈、约定（团队共享）|
|项目个人记忆|`./CLAUDE.local.md`|你个人的偏好（不入库）|
|用户全局记忆|`~/.claude/CLAUDE.md`|跨项目通用规范（中文回答、命名风格等）|
|自动记忆（可选）|`~/.claude/projects/<项目>/memory/`|由模型按类型自动维护的用户 / 反馈 / 项目 / 引用记忆|

### 常用记忆操作

```
# 1. 通过 # 前缀快速追加项目记忆
# 本项目使用 pnpm，不要使用 npm

# 2. 通过 /memory 编辑记忆文件
/memory

# 3. 让 Claude 主动记住偏好
请记住：以后所有 commit message 都用中文，并遵循 Conventional Commits 规范

# 4. 让 Claude 忘记某条记忆
忘掉关于 commit message 的约定
```

### 上下文管理技巧

```
# 压缩历史（保留要点，释放 Token）
/compact

# 带指令压缩：仅保留与某主题相关的内容
/compact 只保留与认证模块重构相关的上下文

# 完全清空，开新任务
/clear
```

---

## 十、Plan 模式与权限模式

Claude Code 提供 4 种权限模式，可按 `Shift + Tab` 循环切换，或在启动时通过 `--permission-mode` 指定：

|模式|说明|适用场景|
|---|---|---|
|**Default**|执行写操作 / 命令前逐项请求确认|日常开发，安全默认|
|**Auto-accept Edits**|自动接受文件编辑，但仍确认 Bash 命令|大批量重构 / 已审过的修改|
|**Plan Mode**|**只读模式**：仅探索代码、不执行任何写入，结束时输出计划|复杂任务的预先设计阶段|
|**Bypass Permissions**|跳过全部权限确认（等价 `--dangerously-skip-permissions`）|沙箱 / CI 环境，谨慎使用|

### Plan 模式典型流程

```
1. 按 Shift + Tab 切到 Plan 模式
2. 描述目标："为本项目添加用户登录功能"
3. Claude 会探索代码、读取文件，然后给出完整实施计划
4. 你 Review 计划 → 同意后自动退出 Plan 模式进入执行
```

> Plan 模式特别适合**架构改动、跨文件重构、新功能设计**这类需要先对齐方案的任务，可避免一上来就改代码。

---

## 十一、自定义斜杠命令（Slash Commands）

将常用 prompt 固化为可复用的命令，存放在 `.claude/commands/` 下，文件名即为命令名。

```
.claude/
└── commands/
    ├── refactor.md         → /refactor
    ├── fix-bug.md          → /fix-bug
    └── git/
        └── new-pr.md       → /git:new-pr   （子目录形成命名空间）
```

### 命令文件示例

`.claude/commands/refactor.md`：

```markdown
---
description: 按项目规范重构指定文件
argument-hint: <文件路径>
allowed-tools: Read, Edit, Bash(npm test:*)
---

请按以下步骤重构 $ARGUMENTS：
1. 阅读文件，识别坏味道（重复代码、过长函数、命名不清）
2. 输出重构计划并等待我确认
3. 执行重构，保持外部 API 不变
4. 运行 `npm test` 验证未引入回归
```

使用：`/refactor src/utils/parser.ts`

> 支持 `$ARGUMENTS`、`$1` `$2` 等位置参数，`@file` 嵌入文件，以及在 frontmatter 中限定可用工具。
> 用户级命令放在 `~/.claude/commands/`，团队级放项目下并入库。

---

## 十二、子代理（Subagents）

子代理是带有**独立上下文、独立系统 prompt、独立工具白名单**的小型代理，主代理可以委派任务给它。适合：

- **并行**执行独立任务（多分支搜索、多文件审查）
- **隔离上下文**：把噪声多的检索 / 长输出隔离在子代理中，避免污染主对话
- **角色专精**：代码审查员、测试编写者、安全审查员等

### 创建子代理

```
/agents
```

或手动新建 `.claude/agents/code-reviewer.md`：

```markdown
---
name: code-reviewer
description: 资深代码审查员，专注可读性、性能和安全。被动触发：当用户要求 review 改动时。
tools: Read, Grep, Glob, Bash(git diff:*)
model: sonnet
---

你是一名严格但建设性的代码审查员。流程：
1. 用 git diff 获取当前改动
2. 按 SOLID / 可读性 / 性能 / 安全四个维度评审
3. 输出"必须修改 / 建议修改 / 可忽略"三档清单
```

使用：在主对话中说 "请用 code-reviewer 帮我审查当前改动"，主代理会自动委派。

---

## 十三、Hooks 钩子系统

Hooks 让你在 Claude Code 生命周期的关键事件上自动执行 shell 命令，**由 harness 直接执行而非模型**，因此对"每次保存后自动格式化""提交前自动跑 lint"这类需求非常可靠。

### 常用事件

|事件|触发时机|典型用途|
|---|---|---|
|`PreToolUse`|工具调用前|拦截危险命令、补充上下文|
|`PostToolUse`|工具调用后|自动格式化、自动跑测试|
|`UserPromptSubmit`|用户提交 prompt 时|预处理输入、注入上下文|
|`Stop`|本轮回答结束|发通知、写日志|
|`SubagentStop`|子代理结束|聚合产物|
|`SessionStart` / `SessionEnd`|会话开始 / 结束|加载 / 归档环境|
|`Notification`|系统通知|桌面提醒|

### 配置示例：每次编辑 Python 文件后自动 ruff format

`.claude/settings.json`：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "ruff format $CLAUDE_FILE_PATHS && ruff check --fix $CLAUDE_FILE_PATHS"
          }
        ]
      }
    ]
  }
}
```

> Hooks 可通过返回非零退出码**阻断**对应操作（例如禁止编辑特定目录），返回 JSON 还可以注入额外上下文。

---

## 十四、MCP（Model Context Protocol）外部工具集成

MCP 是 Anthropic 推动的开放协议，让 Claude Code 可以连接**外部数据源与工具**：数据库、Jira、GitHub、Figma、Sentry、文件系统、Playwright 浏览器等。

### 添加 MCP 服务器

```bash
# 添加一个本地 stdio 类型 MCP（例：filesystem）
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem /your/path

# 添加远程 HTTP / SSE 类型 MCP
claude mcp add --transport http my-api https://api.example.com/mcp

# 列出 / 管理
claude mcp list
claude mcp remove filesystem
```

也可以在 `settings.json` 的 `mcpServers` 字段中声明，或在对话中输入 `/mcp` 查看连接状态。

### 在对话中使用

```
请用 GitHub MCP 列出 anthropics/claude-code 仓库的最近 5 个 issue
@figma:design-tokens 把设计稿中的色板同步到 tailwind.config.js
```

> MCP 资源可用 `@server:resource` 引用，MCP 工具会自动出现在工具列表中。

---

## 十五、Skills 技能系统

Skills 是**封装好的"专业能力包"**：包含 prompt、说明、可选脚本和参考资料，按需触发（关键词 / 任务类型匹配）。和 Subagent 的区别：Skill 是"会做某事的方法"，Subagent 是"会做某事的人"。

### 常见使用方式

```
# 列出 / 查找可用 skill
/help                       # 内置命令中会看到已加载 skill
请帮我找一个能 X 的 skill     # 触发 find-skills

# 直接调用某个 skill（如本会话已加载）
/maya-python 帮我写一段批量重命名骨骼的脚本
/security-review            # 对当前分支改动做安全审查
/init                       # 初始化 CLAUDE.md
/review                     # 审查当前 PR
```

### 创建自定义 Skill

把 skill 放到 `~/.claude/skills/<skill-name>/` 或项目 `.claude/skills/<skill-name>/`，目录中至少包含 `SKILL.md`（描述触发条件与流程），可附加脚本、模板、参考文档。可用内置的 `skill-creator` skill 引导生成。

---

## 十六、会话管理（恢复 / 继续 / 压缩）

```bash
# 终端中：继续最近一次会话
claude --continue
claude -c

# 终端中：从会话列表里选择一个恢复
claude --resume
claude -r

# 会话内：恢复（同上，列出最近会话）
/resume

# 复制会话 ID（便于在脚本中精确恢复）
/status

# 长会话节省 Token
/compact
/compact 仅保留与当前 bug 修复相关的内容

# 完全清空，开始新任务
/clear
```

> 会话历史保存在 `~/.claude/projects/<项目路径哈希>/` 下，可用 `--session-id` 精确指定恢复某次。

---

## 十七、IDE 与编辑器集成

Claude Code 提供官方的 IDE 集成，把 CLI 能力嵌入到编辑器：

|IDE|安装方式|
|---|---|
|VS Code / Cursor / Windsurf|应用市场搜索 "Claude Code"|
|JetBrains 全家桶（IDEA / PyCharm / WebStorm 等）|插件市场搜索 "Claude Code"|

集成后可获得：

- **在编辑器中直接发起对话**（侧边栏 / 内联）
- **当前选中代码自动作为上下文**
- **Diff 在编辑器原生 diff 视图中查看 / 接受 / 拒绝**
- **诊断信息（Lint / 类型错误）自动同步给 Claude**
- **`⌘ Esc` / `Ctrl + Esc`** 一键唤起 Claude（VS Code）

终端中也可用 `/ide` 命令连接当前打开的 IDE。

---

## 十八、非交互式（Headless）模式

适合 CI/CD、批处理、与脚本管道结合：

```bash
# -p / --print：执行后直接退出，输出到 stdout
claude -p "检查代码中是否有 TODO 注释，列出所有文件和行号"

# 指定输出为 JSON，便于程序解析
claude -p "列出所有 TODO" --output-format json
claude -p "实时流处理" --output-format stream-json

# 在 CI 中通过环境变量传 API Key
ANTHROPIC_API_KEY=sk-ant-xxx claude -p "生成 CHANGELOG"

# 与管道结合
cat error.log | claude -p "分析这个错误日志，找出根本原因"
git diff HEAD~1 | claude -p "Review 这次 commit 的代码改动"
pytest --tb=short 2>&1 | claude -p "分析测试失败原因并给出修复建议"

# 写入文件
claude -p "为这个项目生成 README.md" > README.md

# 限制工具与权限（CI 中推荐）
claude -p "..." --allowedTools "Read,Grep,Glob" --permission-mode plan
```

> 也可使用 **Claude Agent SDK**（Python / TypeScript）以编程方式调用同一套能力，构建自定义代理。

---

## 十九、高级用法与技巧

### 非交互式（脚本）模式

参见上文"十八、非交互式（Headless）模式"获取完整用法。这里给出最小示例：

```bash
claude -p "为这个项目生成 README.md" > README.md
```

### 多文件上下文管理

```
# 明确指定上下文文件，减少无关干扰
只关注 src/auth/ 目录，帮我重构认证模块

# 压缩上下文（长对话时使用）
/compact
```

### 任务拆解与复杂工作流

```
# 分步执行复杂任务
我需要添加用户登录功能，请分步骤完成：
1. 先设计数据库 Schema
2. 等我确认后再实现 API 端点
3. 最后生成前端表单组件

# 执行前确认（避免误操作）
在删除任何文件前先告诉我你打算做什么
```

### 与外部工具联动

```bash
# 结合 grep 定位问题
grep -r "deprecated" src/ | claude -p "分析这些废弃警告，建议如何迁移"

# 结合 git diff
git diff HEAD~1 | claude -p "Review 这次 commit 的代码改动"

# 分析测试结果
pytest --tb=short 2>&1 | claude -p "分析测试失败原因并给出修复建议"
```

### 多模态：粘贴图片 / 截图

在支持的终端（如 iTerm2 / Warp / VS Code 集成终端）中可直接 `Ctrl + V` 粘贴截图，让 Claude 分析：

```
[粘贴一张报错截图]
帮我看看这个报错是怎么回事

[粘贴一张 UI 设计稿]
请按此设计稿生成 React 组件代码
```

### 并行任务与子代理

对独立任务（多模块审查、并行搜索）让主代理派发多个子代理并行处理：

```
请同时启动 3 个子代理：一个审查 src/api/ 的代码质量，
一个审查 src/ui/ 的可访问性，一个审查 src/db/ 的 SQL 注入风险，
最后汇总报告。
```

---

## 二十、常见问题

### Q1：Claude 修改文件前会提示确认吗？

默认情况下，Claude Code 在执行**写入、删除、执行命令**等危险操作前会请求确认。可以通过以下方式控制：

```bash
# 自动同意所有操作（谨慎使用！）
claude --dangerously-skip-permissions
```

### Q2：如何让 Claude 忽略某些目录？

在 `CLAUDE.md` 或对话中明确说明：

```
忽略 node_modules/、.git/、dist/ 目录，只分析源码部分
```

### Q3：Token 消耗过大怎么办？

```
# 1. 定期压缩上下文
/compact

# 2. 开启新会话处理新任务
/clear

# 3. 查看消耗情况
/cost

# 4. 使用更轻量的模型
/model haiku           # 切到 Haiku（最快、最便宜）
/model sonnet          # 切到 Sonnet（速度与能力均衡）
/model opus            # 切到 Opus（最强、最贵）
```

### Q4：如何处理大型代码库？

```
# 先给出明确的范围限定
只分析 src/core/ 模块，不要读取其他目录

# 分模块逐步处理
先帮我理解 models/ 层，下一步再看 services/ 层

# 用 Plan 模式先做架构梳理，再让子代理并行钻研各模块
```

### Q5：命令执行失败或卡住怎么办？

```bash
# 按 ESC 中断当前任务
# 然后描述清楚问题重新尝试

# 或直接重启会话
/clear
```

### Q6：如何让 Claude 自动遵守某条规则（如每次保存自动格式化）？

仅靠记忆 / CLAUDE.md 无法保证 100% 触发；这类**确定性自动化**应使用 Hooks，配置 `PostToolUse` 上的 `Edit|Write` matcher 调用格式化工具。详见"十三、Hooks 钩子系统"。

### Q7：Plan 模式和 `--dangerously-skip-permissions` 有什么区别？

- **Plan 模式**：只读，安全探索 + 输出方案，**不会改任何文件**。
- **Bypass Permissions**：放弃所有权限确认，**会直接执行任意写入与命令**，仅适合容器 / 沙箱 / CI。

### Q8：怎么连接公司内的私有 API / 数据库 / Jira？

通过 MCP 服务器接入。可使用社区现成的 MCP 实现（filesystem / github / postgres / jira / sentry / playwright 等），也可自行用 SDK 开发。详见"十四、MCP 外部工具集成"。

### Q9：什么时候用 Subagent？什么时候用自定义 Slash Command？

- **Slash Command**：复用 prompt（"做一件事的方式"），轻量、即时。
- **Subagent**：需要独立上下文与工具白名单（"做某事的人"），适合并行 / 隔离 / 角色专精。

### Q10：会话中途想换模型？

`/model` 即可随时切换；切换后保留当前上下文。也可用 Fast 模式（`/fast`）在 Opus 上获得更快输出。

---

## 最佳实践总结

|场景|推荐做法|
|---|---|
|初次接触新项目|先 `/init` 生成 `CLAUDE.md`，再让 Claude 做整体架构分析|
|复杂功能开发|先进 **Plan 模式** 对齐方案，再退出执行|
|大批量重构|切到 **Auto-accept Edits** 模式，减少打断|
|跨模块独立任务|派发多个 **Subagent** 并行处理，主上下文聚焦汇总|
|确定性的自动化（格式化 / lint）|使用 **Hooks**，不要依赖记忆 / 提示词|
|连接外部系统（DB / Jira / GitHub）|接入对应的 **MCP 服务器**|
|高复用 prompt|沉淀为 **自定义 Slash Command**，团队共享入库|
|长时间工作|定期 `/compact` 压缩上下文，必要时 `/clear` 开新会话|
|调试问题|提供完整的错误堆栈和复现步骤；可粘贴截图|
|团队项目|维护好 `CLAUDE.md`，统一 AI 行为规范；敏感命令进 `permissions.deny`|
|自动化场景|使用 `-p` 非交互模式 + `--allowedTools` 限权限，集成到 CI|
|Token 成本敏感|轻量任务用 Haiku，复杂任务才用 Opus；善用 `/cost` 监控|

---

_本文档基于 Claude Code 当前版本整理，功能可能随版本更新而变化。_ _官方文档：[https://docs.anthropic.com/claude-code](https://docs.anthropic.com/claude-code)_

---

## 相关笔记

> 与开源 fork 路线的横向对照见 [oh-my-pi使用指南](oh-my-pi使用指南.md)：那篇以本工具为基准做过四轮 Python 编辑实测（含同名遮蔽陷阱），并对比了模型支持面（omp 69 provider vs Claude Code 仅 Claude 系）与协作能力（cron/task/worktree 是 Claude Code 独有）。本篇讲怎么用好 Claude Code，那篇讲什么时候该换工具。