# oh-my-pi (omp) 使用指南

> 适用版本：omp 17.2.9（2026-08 实测）
> 官方仓库：[can1357/oh-my-pi](https://github.com/can1357/oh-my-pi)　官网：[omp.sh](https://omp.sh)　授权：MIT
> 本机配置：中转站多 provider（详见第六章），配置根目录 `~/.omp/agent/`

---

## 一、omp 是什么

**oh-my-pi**（命令名 `omp`）是 [Pi Agent](PiAgent%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97.md) 的社区重装 fork，作者 can1357。两者取向完全相反：

- **Pi**：极简自组装 —— 默认只给 4 个工具，能力靠扩展包一个个装
- **omp**：batteries included —— 内置 LSP/DAP/AST 编辑/浏览器/桌面控制/位图上下文压缩，开箱即用

技术栈与 Pi 也不同：**Bun 运行时**（≥1.3.14）+ **约 8 万行 Rust**（另有约 7.7 万行 vendored：brush bash fork、jq 引擎 jaq、46 个 uutils coreutils 直接编进 shell）。搜索、shell、AST、PTY、图像解码、BPE 计数全部在进程内跑，热路径不 fork/exec。

### 与 Claude Code 的定位差异

| | Claude Code | omp |
|---|---|---|
| 性质 | Anthropic 官方，闭源商业 | 社区 fork，**MIT 开源** |
| 模型面 | 仅 Claude 系（+Bedrock/Vertex/Foundry） | **69 个 provider 描述符 / 4120 条模型目录** |
| 模型角色 | 单一 `--model` + `--fallback-model` | **10 个角色**分工路由 |
| 长处 | 云端协作：cron、托管 task、worktree、ultrareview | 代码理解深度：LSP 14 操作、DAP 调试、AST 编辑 |
| 迭代 | 稳定发布 | CHANGELOG 已 672 个版本 —— 快，但**会撞坑** |

一句话：**Claude Code 往上长（协作与托管执行），omp 往下长（代码理解深度）**。

> 关于「omp 改 Python 代码是否更强」，本机做过四轮对照实测，结论与直觉相反 —— 见第九章。

---

## 二、安装

### Windows（本机方式）

```powershell
irm https://omp.sh/install.ps1 | iex
```

也可用 Bun（官方推荐）：

```sh
bun install -g @oh-my-pi/pi-coding-agent
```

> **坑**：本机 scoop 的 `bun` shim 曾损坏（`bun --version` 报找不到 bun.exe），装 omp 前先验一次。实际可用的 bun 在 `~/.bun/bin/bun`。

其他平台：macOS/Linux 用 `curl -fsSL https://omp.sh/install | sh`，Homebrew 用 `brew install can1357/tap/omp`，锁版本用 `mise use -g github:can1357/oh-my-pi`。

### Shell 补全

omp 从实时命令元数据生成补全脚本，不会与真实 CLI 漂移：

```bash
eval "$(omp completions bash)"    # 加到 ~/.bashrc
```

### 目录结构

```
~/.omp/
├── agent/
│   ├── config.yml          # 主配置（shellPath、模型角色、审批模式…）
│   ├── models.yml          # provider / 模型定义
│   ├── mcp.json            # MCP 用户级配置 + disabledServers 黑名单
│   ├── agent.db / history.db / models.db
│   └── sessions/           # 按项目路径组织
├── logs/                   # JSONL 格式，排查必看
└── natives/
```

---

## 三、基本使用

```bash
omp                                    # 交互式 TUI
omp -p "提示词"                        # 无头单轮，输出到 stdout
omp -c                                 # 继续上次会话
omp -r                                 # 恢复会话（选择器）
omp --model paperhub-deepseek/deepseek-v4-pro "..."   # 指定模型
omp -p --no-session --auto-approve "..."              # 临时会话 + 自动批准（脚本/验证用）
```

### 常用子命令

| 命令 | 用途 |
|---|---|
| `omp models` | 列出全部可用模型（按 provider 分组） |
| `omp models refresh` | 强制刷新模型目录 |
| `omp config list` | 列出全部配置项（约 450 项，含类型与默认值） |
| `omp config set <键> <值>` | 改配置（**推荐方式**，见第七章） |
| `omp setup` | 引导式设置向导 |
| `omp stats` | 用量统计（会起本地 dashboard，前台会阻塞） |
| `omp commit` | 生成 commit message + 更新 changelog |
| `omp bench` | 基准测试模型的首 token 延迟与吞吐 |

### 内置工具

顶层 13 个：`read` `bash` `edit` `write` `eval` `glob` `grep` `task` `hub` `todo` `web_search` `learn` `manage_skill`

另有一批挂在 **`xd://` 虚拟设备**上（不占顶层工具槽，因为每个顶层工具的 schema 都要在每次 API 调用里重发）：`ast_edit` `debug` `lsp` `browser` `computer` `checkpoint` `memory_*` `security_scan` `github`

调用方式是往 `xd://<名字>` 写 JSON 参数，而非直接调工具。

---

## 四、TUI 内的输入前缀（`#` `/` `!` `$` `@`）

进入交互式 TUI（直接跑 `omp`）后，欢迎屏右侧的 Tips 就写着四个入口。这些**只在交互模式生效**，`omp -p` 无头模式下不可用 —— 斜杠命令由 TUI/session 层在提示词送到模型**之前**就解析掉了，模型本身拿不到（实测让 agent 自报"有哪些斜杠命令"，它答 0 个，并解释自己收到的已是展开后的文本）。

| 前缀 | 作用 |
|---|---|
| `#` | **提示动作**（prompt actions）—— 编辑器操作，不发给模型 |
| `/` | **斜杠命令** —— 70 个内置顶层命令，见下节 |
| `!` | **直接跑 bash** —— 走 `AgentSession.executeBash`，不是模型的工具调用 |
| `$` | **直接跑 python** —— 进 eval 内核 |
| `@` | **文件提及补全** —— 模糊查找并插入文件路径 |

### 4.1 `#` 提示动作（共 7 个）

输入 `#` 触发模糊搜索，选中后执行编辑器动作。**它不是给 agent 下命令**，纯粹操作输入框：

| 动作 | 说明 |
|---|---|
| Copy current line | 复制当前行到剪贴板 |
| Copy whole prompt | 复制整个提示词 |
| Undo | 撤销编辑 |
| Move cursor to end / beginning of message | 光标跳到消息末尾 / 开头 |
| Move cursor to beginning / end of line | 光标跳到行首 / 行尾 |

每项后面会显示对应快捷键，所以 `#` 也可以当**快捷键速查表**用。

### 4.2 `!` bash 与 `$` python

```
!git status                    # 直接执行，输出进上下文
$import sys; print(sys.path)   # 进 eval 内核，与 agent 共享同一个 Python 会话
```

`$` 复用的正是第八章那个持久化内核 —— 你手动 stub 的 `maya.cmds` 之后 agent 也能用，反之亦然。这对 DCC 调试很顺手。

---

## 五、常用斜杠命令

omp 内置 **70 个顶层斜杠命令**（源码 `src/slash-commands/builtin-registry.ts`）。下面按使用频率分组，不求全，只列实际会用到的。

### 5.1 会话与上下文管理（最常用）

| 命令 | 作用 |
|---|---|
| `/new` | 开新会话 |
| `/clear` | 原地清空上下文，**保留会话** |
| `/drop` | 删除当前会话并开新的 |
| `/compact` | 手动压缩上下文（走 snapcompact） |
| `/shake [elide\|images]` | 从上下文里丢掉重内容 —— `elide` 剥工具结果+大块（默认），`images` 只剥图片 |
| `/context` | **查看上下文占用明细**（排查为什么快满了） |
| `/handoff [重点说明]` | 把当前上下文交接给一个新会话 |
| `/resume [会话id\|@claude\|@codex]` | 恢复会话，**可直接导入 Claude Code / Codex 的会话** |
| `/rename <标题>` / `/move [路径]` | 重命名 / 移动当前会话 |
| `/fresh` | 只重置 provider 流状态，不动本地记录（流卡死时用） |
| `/retry` | 重试上一次失败的回合 |

### 5.2 模型切换

| 命令 | 作用 |
|---|---|
| `/model`（别名 `/models`） | 切换本会话模型 |
| `/switch` | 同上（等价于 `Alt+P`） |
| `/prewalk` | **下一个动作起切到快模型**（不必启动时加 `--prewalk`） |
| `/fast [on\|off\|status]` | 优先服务档（OpenAI `service_tier=priority` / Anthropic `speed=fast`） |
| `/usage [show\|reset]` | 查看各 provider 用量与限额 |

> `Ctrl+P` 在当前角色的候选模型间循环 —— 候选池就是配置里的 `enabledModels`（见第七章规则 3）。

### 5.3 模式切换（omp 的特色）

| 命令 | 作用 |
|---|---|
| `/plan [提示词]` | **plan 模式** —— 先出方案再执行 |
| `/plan-review` | 重新打开最近一次方案的评审（仅 plan 模式） |
| `/goal [目标]` | **goal 模式** —— 设持久自主目标，子命令 `set` / `show` / `pause` / `resume` / `drop` / `budget` |
| `/guided-goal [粗略目标]` | 让 agent 先在对话里访谈你，再帮你配 goal 模式 |
| `/loop [次数\|时长] [提示词]` | **循环模式** —— 每次 yield 后自动重投同一提示词，`Esc` 取消当前轮 |
| `/vibe [提示词]` | vibe 模式 —— 持久快/好双 worker，只读工具集 |
| `/tan <工作>` | 把**旁支工作**丢给后台 agent 跑，不打断主线 |
| `/btw <问题>` | 用当前上下文问一个**临时侧面问题**，不污染主对话 |
| `/queue <消息>` | 排队一条消息，等 agent yield 后再发 |
| `/pause` | **冻结所有 agent**（主 + 子代理 + advisor） |
| `/force <工具名> [提示词]` | 强制下一回合必须用指定工具 |

`/btw` 和 `/tan` 这两个很实用：前者问完即走不留痕，后者把"顺手想查的事"甩给后台。

### 5.4 工具与诊断

| 命令 | 作用 |
|---|---|
| `/tools` | **列出 agent 当前实际可见的工具**（排查工具没加载时第一步） |
| `/mcp` | MCP 管理，子命令 `list` / `add` / `remove` / `test` / `enable` / `disable` / `reconnect` / `reload` / `resources` / `prompts` |
| `/debug` | 打开调试工具选择器 |
| `/hotkeys` | 全部快捷键一览 |
| `/jobs` | 后台异步任务状态 |
| `/info` | 会话信息与统计 |
| `/vision [on\|off\|auto\|status]` | 控制 `inspect_image` 视觉委派 |
| `/computer [on\|off\|status]` | 本机桌面控制工具开关 |
| `/browser [headless\|visible]` | 浏览器有头 / 无头切换 |
| `/advisor [on\|off\|status\|dump\|configure]` | advisor（第二个模型逐回合复审并注入意见） |

### 5.5 记忆与技能

| 命令 | 作用 |
|---|---|
| `/memory` | 记忆维护，子命令 `view` / `stats` / `diagnose` / `clear` / `reset` / `enqueue` / `rebuild`，另有 `mm list` / `mm show` / `mm refresh` 等心智模型操作 |
| `/todo` | 查看修改 agent 的 todo 列表，子命令 `edit`（用 `$EDITOR` 打开，Markdown 往返）/ `append` / `start` / `done` / `rm` |
| `/omfg <吐槽>` | **从抱怨里锻造一条 TTSR 规则**来阻止某个反复出现的行为 —— omp 的特色功能 |

### 5.6 会话分享与协作

| 命令 | 作用 |
|---|---|
| `/export [--themes] [路径]` | 导出会话为 HTML |
| `/dump` | 会话记录复制到剪贴板（并把 LLM 请求 JSON 写到临时目录） |
| `/share` | 加密链接分享 |
| `/view` | 只读链接（对方能看不能发言） |
| `/collab [start\|view\|stop\|status]` | 经中继实时共享会话；对方用 `/join <链接>` 加入，`/leave` 离开 |
| `/branch` / `/fork` / `/tree` | 从历史消息开分支 / 复刻 / 在会话树间导航 |

`/tree` + `/branch` 组合可以在同一份上下文上试多条路线，比反复 `/clear` 高效。

### 5.7 配置与插件

| 命令 | 作用 |
|---|---|
| `/settings` | 打开设置菜单（图形化改 `config.yml`） |
| `/setup`（别名 `/providers`） | provider 设置 |
| `/login [provider]` / `/logout` | OAuth 登录登出 |
| `/plugins [list\|enable\|disable]` | 管理已装插件 |
| `/marketplace` | 插件市场，子命令 `add` / `discover` / `install` / `uninstall` / `upgrade` / `installed` |
| `/reload-plugins` | **重载全部插件**（技能、命令、钩子、工具、agent、MCP）—— 改完扩展不必重启 |
| `/extensions` / `/agents` | 扩展 / Agent 控制中心面板 |
| `/add-dir <路径>` / `/remove-dir` / `/dirs` | 多根工作区管理 |
| `/ssh` | SSH 主机管理（`add` / `list` / `remove`） |

### 5.8 魔法关键词（不是命令，写在提示词里就生效）

三个词作为**独立散文**出现在消息里即触发隐藏指令，输入时还会有渐变高亮：

| 关键词 | 效果 |
|---|---|
| `ultrathink` | 追加隐藏提示，推动模型做谨慎的多步推理（对齐 Claude Code 的同名功能） |
| `orchestrate` | 引导编排式分工 |
| `workflowz` | 引导按工作流推进 |

匹配规则很严（源码 `modes/magic-keywords.ts`）：

- **仅小写、必须是独立词** —— `ultrathinking`、`Ultrathink`、`ultrathink.ts`、`orchestrate()`、`foo::orchestrate` 都**不**触发；`orchestrate,` 触发
- 代码块、行内代码、HTML/XML 标签内部的出现一律忽略
- 只对**包含该词的那一回合**生效

> **坑**：关掉某个关键词的配置键名与关键词本身不一致 —— 是 `omp config set magicKeywords.workflow false`（不是 `workflowz`）。

### 5.9 内部 URL 协议（模型侧，非输入前缀）

omp 给模型挂了一套 `xxx://` 内部 URL，用 `read` / `write` 访问。**这些不是编辑器补全前缀**，是 agent 的能力入口：

| 协议 | 用途 |
|---|---|
| `xd://` | 挂载的工具设备（`xd://` 列全部，`xd://<名字>` 看该设备文档，写 JSON 即调用） |
| `omp://` | **omp 自己的内部文档**（124 篇，查机制时很有用） |
| `vault://` | Obsidian 库读写（需 `vault.enabled: true`） |
| `memory://` | 记忆库 |
| `skill://` | 技能 |
| `agent://` | 子代理 |
| `mcp://` | MCP 资源 |
| `local://` / `history://` / `artifact://` / `rule://` / `security://` / `ssh://` / `issue://` / `pr://` | 本地资源 / 历史 / 产物 / 规则 / 安全扫描 / SSH / issue / PR |

排查 omp 自身行为时，`read omp://<文档名>.md` 比翻源码快 —— 本笔记的若干结论就是这么核实的。

---

## 六、模型与 provider 配置（本机中转站方案）

配置文件 `~/.omp/agent/models.yml`。本机 5 个 provider 对应中转站的三种协议：

| provider | 通道 | 协议 | 模型 |
|---|---|---|---|
| `anthropic`（覆盖内置） | `/anthropic` | `anthropic-messages` | claude 全系 |
| `paperhub-openai` | `/v1` | `openai-responses` | gpt-5.6-sol / terra / luna |
| `paperhub-deepseek` | `/v1` | `openai-completions` | deepseek-v4-pro / flash |
| `paperhub-moonshot` | `/v1` | `openai-completions` | kimi-k3 |
| `paperhub-zhipu` | `/v1` | `openai-completions` | glm-5.2 |

### API key 单点存储技巧

`apiKey` 字段的取值规则（源码 `src/config/resolve-config-value.ts`）：**以 `!` 开头当 shell 命令执行取 stdout**，否则先查同名环境变量，最后才当字面量。

利用这点让 key 只存一处：

```yaml
providers:
  anthropic:
    baseUrl: https://tc-paperhub.diezhi.net/anthropic
    apiKey: "!node C:/Users/dalaotian/.omp/agent/anthropic-token.js"
```

该脚本从 Claude Code 的 `~/.claude/settings.json` 读 `env.ANTHROPIC_AUTH_TOKEN`。换 key 只改 Claude Code 一处，omp 自动跟随。（Pi 侧的 `models.json` 只支持明文，换 key 要单独改。）

### Claude 系为何不写 models 列表

覆盖内置 `anthropic` provider 时只写 `baseUrl` + `apiKey`，**不写 `models`** —— 这样能继承 omp 内置目录的完整能力元数据（1M 上下文、128K 输出、thinking 档位、变体折叠），比手写更全。代价是内置目录里中转站没有的型号也会列出来，调用时才报 404。

其余厂商必须显式写 `api` + `models`，因为内置目录不认识自定义 provider 名。

### 10 个模型角色

`default` `smol`(快) `slow`(推理) `vision` `plan`(架构) `designer` `commit` `tiny` `task`(子代理) `advisor`

本机分配（`config.yml`）：

```yaml
modelRoles:
  default: anthropic/claude-opus-5      # 主力
  slow: anthropic/claude-opus-5         # 深度推理
  plan: anthropic/claude-opus-5         # 架构规划
  task: anthropic/claude-sonnet-5       # 子代理
  vision: anthropic/claude-sonnet-5
  smol: anthropic/claude-haiku-4-5      # 轻量快模型
  commit: anthropic/claude-haiku-4-5
```

选择器语法：`@<角色>`（如 `--model @smol`）、`provider/model`、或模糊匹配裸名。

---

## 七、配置管理的三个硬规则

### 1. 改配置优先用 `omp config set`，别手写文件

**omp 会重写整个 `config.yml`** —— `omp setup`、TUI 内改设置、`omp config set` 都会用 YAML 序列化器重写，**注释全部丢失**，并把当前所有非默认值展开写入（会凭空多出 `setupVersion`、`colorBlindMode`、`theme.dark` 等你没写过的键）。

本机踩过：手写的中文注释在跑过一次 setup 后全没了。**说明性文字应写在笔记里，不要写在 config.yml 里。**

### 2. 数组类型的键要传 JSON

```bash
omp config set enabledModels '["anthropic/claude-opus-5","paperhub-deepseek/deepseek-v4-pro"]'
# 传逗号分隔字符串会报 Invalid array JSON
```

### 3. 候选池的键叫 `enabledModels`，不叫 `models`

`--models` 是 CLI flag，它的**配置文件等价物是 `enabledModels`**（源码 `main.ts::resolveScopedModels`：`parsed.models ?? activeSettings.get("enabledModels")`）。

在 `config.yml` 里写 `models:` 是**死配置** —— YAML 能解析、`omp config list` 也不报错，但代码永远不读。唯一提示是 `omp config set models ...` 会明确报 `Unknown setting: models`。

> 另注：Ctrl+P 循环**角色**的顺序是另一个键 `cycleOrder`（默认 `["smol","default","slow"]`），与 `enabledModels`（模型池）是两回事。

### 与直觉相反的默认值

| 配置 | 默认值 | 说明 |
|---|---|---|
| `tools.approvalMode` | **`yolo`** | 自动批准一切。`write` 档自动批准读+写，但 bash/eval/browser/task 仍需确认 |
| `task.maxConcurrency` | **32** | 子代理并发数，走中转站时可能触发限流 |
| `task.enableLsp` | `false` | 为省 token 关闭子代理的 LSP |
| `autolearn.autoContinue` | `false` | 开启后**每次 agent 停下都会多跑一个私有回合**烧 token |
| `vault.enabled` | `false` | 开启后 `vault://` 可直读写 Obsidian 库 |
| `compaction.strategy` | `snapcompact` | omp 独门的位图压缩，见第八章 |

---

## 八、omp 的三个独门技术

### 8.1 hashline —— 抗错位的编辑格式

每个 patch 锚定到文件内容的 4 位 hex 哈希（`[路径#TAG]` + `PUT 37.=37:`），行号漂移或文件被外部改过时**直接拒绝而不是写坏代码**。

副产品很实用：**文件快照 tag 可作为「哪些文件被改过」的硬证据** —— 未改动的文件 tag 不变。

### 8.2 snapcompact —— 位图上下文压缩

不让 LLM 总结被丢弃的历史，而是**把历史文本渲染成像素字体的 PNG 帧**，让视觉模型直接读回。全程本地确定性执行，**零 LLM 调用、零 API key、零额外延迟**。

帧型还按 provider 计费方式调优过：

| 读取方 | 默认帧型 | 原因 |
|---|---|---|
| Anthropic | `11on16-bw` | 高分辨率 Claude 行给 1932px 帧 |
| Google | `8on22-bw` @2048 | Gemini 按固定图片预算计费 → 大帧等于"免费字符" |
| OpenAI | `8on22-bw` | 以 `detail: "original"` 发送 |

### 8.3 eval —— 持久化 Python 内核

跨 cell 保持状态，这对 DCC 开发很有价值：

```
cell1: stub maya.cmds → import rig_helper → build_fk_controls() → ['ctrl_a','ctrl_b','ctrl_c']
cell2: 不重新 import、不重建 stub → build_ik_controls() → ['ctrl_a_ik','ctrl_c_ik']
       rig_helper is sys.modules['rig_helper'] → True（同一模块对象）
```

**一次打桩，后续 cell 直接调用被测函数** —— 在**没开 Maya/MoBu** 的情况下验证绑定工具逻辑。Claude Code 每次 Bash 都是新进程，做不到这件事。

> 已知缺陷：`eval` 内核跑 `subprocess.run` 时会挂死，agent 会自己 fallback 到 bash。

---

## 九、Python 开发实测（2026-08-06）

在真实代码库（`D:\Code\MhRigCreator`，10.6k 行）+ Maya 风格沙盒上，与 Claude Code 2.1.223 做同任务对照，结果**由第三方独立验证**（diff + `py_compile` + stub `maya.cmds` 跑行为等价），不采信 agent 自述。

### 致命前提：Python LSP 需单独装 language server，且静默失效

omp 的 Python LSP 需要 **`pyright-langserver` 在 PATH 上**（源码 `src/lsp/defaults.json`，另支持 `basedpyright-langserver` / `pylsp`）。未装时 `lsp` 工具返回：

```
No language servers configured for this project
```

**不报错、不提示、`lsp.enabled: true` 照样显示开着** —— 招牌能力实际为 0 却毫无感知。

`omp setup python` **不装 LSP**（它只配 python 执行环境，`--check` 回一句 "Python execution is ready"，很有误导性）。正确装法：

```bash
npm i -g pyright        # 提供 pyright + pyright-langserver
```

装后验证要两步（第一步不够）：

```bash
cd <有 pyproject.toml 的项目>
omp -p --no-session --auto-approve "Use the lsp tool with action 'status'. Report verbatim."
# 期望：Language servers: pyright (configured, not started)
# "not started" 表示二进制在 PATH 但未 spawn，发一次真实请求才转 ready
```

触发条件：项目根需有 `pyproject.toml` / `pyrightconfig.json` / `setup.py` / `setup.cfg` / `requirements.txt` / `Pipfile` 之一。

### 四轮对照结果

| 任务 | omp | Claude Code |
|---|---|---|
| ① 歧义单点改（两处近似行，只改其一） | ✅ | ✅ |
| ② 提取重复代码为 helper（3 行 × 2 处） | ✅ 行为等价 | ✅ 行为等价，**多合并一行更简洁** |
| ③ 跨文件重命名（7 处 / 3 文件 / 两种导入形态） | ✅ 7/7 | ✅ 7/7 |
| ④ **同名遮蔽陷阱**（另文件 6 处同名但语义无关，一个都不能改） | ✅ 7 改 / 6 零污染 | ✅ 7 改 / 6 零污染（md5 未变） |

④ 是专门设计来击穿"文本/AST 机械替换"的：另一文件有独立的 `def get_joint_chain(data: dict)` + 类方法 `ChainCache.get_joint_chain` + 注释提及。

**结论：装 pyright 前 omp ≈ Claude Code；装 pyright 后在上述任务上仍然打平。**

原因值得记住：Claude Code 没有 LSP，靠**读代码理解作用域**而非机械替换，它甚至主动保留了注释里的旧名，理由是"注释描述的正是本文件自己的那个函数，改掉反而失真"。**在中小规模、语义清晰的代码上，模型的理解力足以替代 LSP。** LSP 的价值要到"符号被几十个文件引用、有别名重导出、跨包继承"的规模才会压倒性显现。

### 装 pyright 的净收益（不是零）

`references`（语义级查引用）、`definition` / `type_definition` / `implementation`（跳转）、`hover`（类型签名，对 pymel 动态 API 有用）、`code_actions`（自动修复）、`diagnostics`（类型检查）。

最实用的是最后一项：`lsp.diagnosticsOnWrite` 默认为 `true`，**改完 .py 会自动跑 pyright 类型检查**，写错属性名/参数类型立刻反馈，不用等到 Maya 里报错。

### ast_grep 有效但非决胜项

在真实 MhRigCreator 上找 `build*` 函数得到 **8 个**，含 2 个 `build_all` 内的**嵌套闭包** —— 纯文本 grep 按列锚定会漏。但 Claude Code 的 Grep 配合正则能覆盖多数场景，属"更省心"而非"能 vs 不能"。

---

## 十、MCP 配置与排查

### omp 会自动发现多处配置（不止一处）

omp 同时扫这些来源（`src/discovery/` 下每个文件一个）：

- `~/.claude.json` + `~/.claude/mcp.json`（Claude Code 的配置）
- **`~/.claude/plugins/`（Claude Code 市场插件）**
- `.cursor/mcp.json`、`.vscode/mcp.json`、codex、gemini、opencode
- `~/.omp/agent/mcp.json` + 项目 `.omp/mcp.json`

**后果：omp 里出现的 server 未必写在你编辑过的任何文件里。** 本机 5 个 server 全部来自 `~/.claude.json`，omp 自己的 `mcp.json` 原本根本不存在。

### 排查入口

```bash
cd ~/.omp/logs && L=$(ls -t omp.*.log | head -1)
grep -iE "MCP tool load failed|mcp:" "$L" | tail
```

日志是 JSONL，`"path":"mcp:<server名>"` 直接给出来源标识。

> `MCP finished with failures. Connected: ... Failed: ...` 这句话是 **omp 独有**的（源码 `src/mcp/startup-events.ts`）。看到它别去翻 Hermes 或 Claude Code 的配置。

### 名字带冒号 = 来自 Claude Code 市场插件

`claude-plugins.ts:553` 做 `${plugin}:${serverName}` 命名空间化。所以 `github:github` 意为"插件 github 里名为 github 的 server"，定义在：

```
~/.claude/plugins/cache/<市场>/<插件>/<版本哈希>/.mcp.json
```

**坑：omp 不读 Claude Code 的 `enabledPlugins` 开关。** 在 `~/.claude/settings.json` 里把插件关成 `false`，Claude Code 会停用，但 omp 照样加载并报错（实测确认）。

### 正确的禁用方式：omp 用户级 denylist

写 `~/.omp/agent/mcp.json`，server 名用**带命名空间的全名**：

```json
{
  "mcpServers": {},
  "disabledServers": ["github:github"]
}
```

源码依据：`disabledServers` 是用户级 denylist 且**永远优先**（"The denylist always wins"）；配套的 `enabledServers` 只能覆盖来源配置里的 `enabled: false`，压不过 denylist。

优点：改插件缓存目录会被插件更新覆盖，denylist 不会。

### transport 声明必须与服务端匹配

grep.app 的 MCP 只支持 streamable-http。若在 `~/.claude.json` 里写成 `"type": "sse"`，omp 报 `HTTP 405: Method not allowed`：

```bash
# POST（streamable-http）→ 200
curl -s -o /dev/null -w "%{http_code}\n" -X POST https://mcp.grep.app \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}'
# GET（SSE）→ 405
curl -s -o /dev/null -w "%{http_code}\n" -m 10 https://mcp.grep.app -H "Accept: text/event-stream"
```

修法：`type` 改成 `"http"`。同一个 server 在两个 agent 里表现不同时，**先往 transport 声明上找**。

### omp 没有 mcp 子命令

`omp mcp` / `omp mcp list` **不存在**（MCP 管理只在交互式 TUI 的 `/mcp` 里）。无头验证靠提示词：

```bash
cd /tmp && omp -p --no-session --auto-approve \
  "List every tool name starting with mcp__. Output only the names, one per line."
```

**坑：`-p` 模式的 MCP 加载有时序抖动。** 本机遇到同一配置连续两次运行，一次列出全部 9 个工具、一次回答"没有任何 mcp 工具"。**判定失败前至少跑两次**，并以日志的实际错误为准，别只信模型自述。

---

## 十一、坑点汇总

1. **裸模型名会解析到错误的 provider。** 中转站 `/anthropic` 通道也接受 deepseek/kimi/glm，导致内置 `anthropic` provider 下也有同名模型，裸名优先命中它。两者都返回 200，**"能跑通"完全掩盖配置失效**（`maxTokens`、协议特性全没生效）。判据只能看日志里的实际 provider：

   ```bash
   cd ~/.omp/logs && L=$(ls -t omp.*.log | head -1); grep -oE '"(provider|model)":"[^"]*"' "$L" | sort -u
   ```

   gpt 系与 claude 系裸名安全（无同名冲突），**只有国产模型有歧义**。稳妥起见全写全名。

2. **中转站会下线模型。** `omp models` 列出的型号来自内置目录，**不代表中转站真的有**（`claude-fable-5`、`claude-sonnet-4-5` 都曾报 `not_found_error`）。配置引用前先实际打一发请求探测。

3. **`omp` 在 `~` 目录会自动切到临时目录**（除非 `--allow-home`）。验证时 `cd /tmp` 更干净。

4. **`omp stats` 会起本地 dashboard 并阻塞前台**，脚本里调用需注意超时。

5. **配置文件的注释必然丢失**（见第七章规则 1）。

6. **迭代太快 = 会撞坑。** 672 个版本的代价：本机实测就撞上了 `eval` 内核挂死、`-p` 模式 MCP 时序抖动两个问题。

---

## 十二、omp / Pi / Claude Code 怎么分工

本机三套并存是合理配置，因为它们**共用同一把 key 和同一份 MCP 声明**（都从 Claude Code 的 settings.json / .claude.json 读）。

| 场景 | 建议 |
|---|---|
| 日常改 Python | Claude Code 或 omp 均可；**Claude Code 更稳** |
| 无 DCC 环境验证绑定逻辑 | **omp 的 `eval` 内核**（独门） |
| 需要跑非 Claude 模型 | **omp**（69 provider 原生多协议） |
| 超大代码库符号级重构 | 装了 pyright 的 omp（`lsp rename` 语义级） |
| 云端协作 / 定时任务 / worktree | **Claude Code** |
| 极简可控、自己攒能力 | **Pi** |

**副作用要知情**：配置互相发现意味着会互相污染 —— 本机的 `github:github` MCP 报错就是 Claude Code 装的市场插件被 omp 自动发现并尝试连接导致的。

---

## 相关笔记

- [PiAgent使用指南](PiAgent%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97.md) —— omp 的上游项目，极简路线
- [ClaudeCode](ClaudeCode.md) —— 本篇多处对照的基准工具
- [HermesAgent使用指南](HermesAgent%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97.md)
- [opencode](opencode.md)
- [vibe-coding-guide](vibe-coding-guide.md)
- [vibecoding的缺点](vibecoding%E7%9A%84%E7%BC%BA%E7%82%B9.md)
