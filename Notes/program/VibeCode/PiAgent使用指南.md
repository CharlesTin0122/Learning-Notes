# Pi Agent 使用指南（含 pi-mcp-adapter 接入 DCC）

> 适用版本：pi ≥ 0.81.x
> 最后更新：2026-07-22
> 官方仓库：[badlogic/pi-mono](https://github.com/badlogic/pi-mono)　官网/文档：[pi.dev](https://pi.dev)　包目录：[pi.dev/packages](https://pi.dev/packages)

---

## 一、Pi 简介

**Pi** 是一款极简、有主见（opinionated）的终端 AI 编码代理，作者 Mario Zechner（badlogic，libGDX 作者），现由 Earendil 公司维护（Armin Ronacher 亦参与开发）。

核心哲学：**"让 pi 适应你的工作流，而不是你去适应它"**。

- **极简默认**：默认只给模型 4 个工具——`read` / `write` / `edit` / `bash`，不内置子代理、plan mode、MCP 等功能
- **渐进式披露**：复杂能力放在外部脚本/CLI 里，agent 需要时用 bash 调用，只在必要时付出 token 成本
- **自扩展**：可以直接让 pi 给自己写 TypeScript 扩展；社区能力通过 Pi Packages 补充
- **四种运行模式**：交互 TUI、print/JSON（`pi -p`，无头）、RPC（进程集成）、SDK（嵌入自己的应用）
- **无内置权限系统**：默认以启动用户的权限裸跑，需要隔离时官方建议容器化（Docker / micro-VM / OpenShell）

### monorepo 包结构（嵌入开发时才需要关心）

| 包 | 作用 |
|---|---|
| `@earendil-works/pi-coding-agent` | 交互式终端编码代理 CLI（日常用的就是它） |
| `@earendil-works/pi-agent-core` | Agent 运行时（工具调用、状态管理），可嵌入自己的应用 |
| `@earendil-works/pi-ai` | 统一多供应商 LLM API（OpenAI / Anthropic / Google …） |
| `@earendil-works/pi-tui` | 差分渲染的终端 UI 库 |

### 与 oh-my-pi（omp）的关系

[oh-my-pi](https://github.com/can1357/oh-my-pi)（作者 can1357）是 Pi 的功能大幅扩展 fork，走"全家桶"路线：TypeScript + ~55k 行 Rust 核心、Bun 运行时、hash 锚定编辑、LSP/DAP 深度集成、双内核代码执行。一句话对比：**Pi 是"给你一个干净的骨架，自己长肉"；omp 是"肉都长好了，还练过"**。Pi 缺的能力（LSP、hash 编辑、子代理等）大多可以通过 Pi Packages 补回来。

---

## 二、安装

```bash
# npm 全局安装（--ignore-scripts 禁用依赖生命周期脚本，pi 正常安装不需要它们）
npm install -g --ignore-scripts @earendil-works/pi-coding-agent

# 或一键脚本（macOS / Linux）
curl -fsSL https://pi.dev/install.sh | sh
```

### Windows 注意事项

pi 在 Windows 上**必须有 bash**，按以下顺序查找：

1. `~/.pi/agent/settings.json` 里的自定义 `shellPath`
2. Git Bash（`C:\Program Files\Git\bin\bash.exe`）← 装了 Git for Windows 即开箱可用
3. PATH 上的 `bash.exe`（Cygwin / MSYS2 / WSL）

### 认证

```bash
# 方式一：环境变量 API key
export ANTHROPIC_API_KEY=sk-ant-...
pi

# 方式二：订阅登录（交互模式内）
pi
/login   # 选择 provider
```

模型切换：`/model` 或 `Ctrl+L`；强制刷新模型目录：`pi update --models`。

---

## 三、基本使用

### 3.1 交互模式常用命令

| 命令/快捷键 | 作用 |
|---|---|
| `/login` | 订阅登录 |
| `/model`（`Ctrl+L`） | 切换模型 |
| `/mcp` | MCP 服务器面板（装 pi-mcp-adapter 后可用） |
| `Tab` 补全 / 消息队列 | 输入体验同主流 agent |

### 3.2 无头模式（脚本化/验证用）

```bash
# -p：执行单条 prompt 后退出，适合自动化与验证
pi -p "运行测试并报告结果"
```

### 3.3 配置文件位置

- 全局设置：`~/.pi/agent/settings.json`（默认 provider/model、已装 packages 列表）
- 会话记录：`~/.pi/sessions/`
- Skills：`~/.pi/skills/`

---

## 四、Pi Packages 生态

pi 的扩展体系：**Extensions（TypeScript）、Skills、Prompt Templates、Themes**，都可以打包成 Pi Package 通过 npm 或 git 分发。安装方式：

```bash
pi install npm:<包名>    # 装完重启 pi 生效
```

官方目录 [pi.dev/packages](https://pi.dev/packages) 收录约 50 个包（2026-07），精选如下：

### 强烈推荐（前 5 个本机已装 ✅，后 2 个见下方小节）

| 包 | 功能 |
|---|---|
| **pi-mcp-adapter** | MCP 协议适配器，单个 `mcp` 代理工具（约 200 token）按需发现/调用 MCP 工具，server 懒启动 |
| **pi-subagents** | 子代理：链式、并行执行、TUI 澄清 |
| **pi-web-access** | 网页搜索/抓取、GitHub clone、PDF 提取、YouTube 理解 |
| **pi-lens** | 实时代码反馈：LSP、linter、格式化、类型检查（弥补 pi 无内置 LSP 的短板） |
| **cc-safety-net** | hook 拦截危险 git / 文件系统命令（pi 无权限系统，建议必装） |
| **pi-hermes-memory** | 持久记忆 + 会话搜索 + 密钥扫描（详见 [4.1 节](#41-pi-hermes-memory持久记忆)） |
| **@ayulab/pi-rewind** | `/rewind` 检查点导航，代码/对话可分别回滚（详见 [4.2 节](#42-ayulabpi-rewind检查点回滚)） |

### 按需选装

| 包 | 功能 |
|---|---|
| pi-readseek / pi-hashline-edit-pro | hash 锚定读写/编辑，弱模型编辑命中率大幅提升（omp 招牌功能移植） |
| pi-distill | 工具输出蒸馏，省 token |
| context-mode | 号称省 98% 上下文 + FTS5 知识库，跨多款 agent 通用 |
| @gotgenes/pi-permission-system | 系统化权限审批（与 cc-safety-net 二选一） |
| pi-simplify | 审查最近改动代码的质量 |
| pi-crew | 多 agent 团队 + git worktree 编排 |
| pi-llama-cpp | 接本地 llama.cpp 模型 |
| pi-vault-mind | Obsidian 库监听 + 向量/FTS 检索（对本知识库场景值得留意） |
| superpowers-zh | superpowers 完整汉化 + 中文原创 skills |
| gentle-pi | "高级架构师" harness：SDD/OpenSpec + 严格 TDD + 评审护栏 |

### 4.1 pi-hermes-memory（持久记忆）

> npm：`pi-hermes-memory`（v0.8.2，MIT，月下载约 1.7 万，693 个测试）
> 从 **Hermes Agent** 移植而来 —— pi 版的 Hermes 记忆体系。

pi 裸装是"金鱼记忆"，关掉 session 全忘；此扩展补齐跨会话上下文能力：

| 功能 | 说明 |
|---|---|
| 持久记忆（MEMORY.md / USER.md） | 事实、偏好、纠错各 5,000 字符上限，双层：全局 + 每项目 |
| 会话搜索 | SQLite FTS5 全文检索所有历史对话（"之前讨论过的 auth 在哪"） |
| 程序性技能 | 以 pi 原生 `SKILL.md` 保存"怎么解决的"，无字数上限 |
| 后台学习 | 每 10 轮（或 15 次工具调用）自动复盘保存；用户纠错立即保存 |
| 自动整合 | 记忆满时自动合并旧条目而不是报错，条目带时间戳判断陈旧度 |
| 密钥扫描 | API key / token / SSH key 禁止写入持久层；所有写入过内容扫描防注入 |
| 扩展存储 | 超出核心 5,000 字符限制的部分进无限量可搜索存储 |

```bash
pi install npm:pi-hermes-memory
# 重启 pi 后：
/memory-index-sessions   # 一次性索引历史会话
/memory-sync-markdown    # 可选：把旧 Markdown 记忆回填进 SQLite
/memory-interview        # 可选：问答式快速建立个人 profile
```

注意事项：

- 数据存在 `~/.pi/agent/pi-hermes-memory/`，与 Hermes Agent 本体的记忆是**两套独立数据**，不互通
- 从 v0.7.10 之前的版本升级会自动迁移旧目录（`~/.pi/agent/memory` → `pi-hermes-memory/`），启动一次即可

### 4.2 @ayulab/pi-rewind（检查点回滚）

> npm：`@ayulab/pi-rewind`（v0.4.6，GPL-3.0，零第三方依赖，自带 `@ayulab/pi-checkpoint` 引擎）
> 补齐 pi 相对 Claude Code 的原生短板：checkpoint / 后悔药。

每轮对话前后自动对工作区拍快照（基于 Git commit），`/rewind` 打开带文件变更统计的交互式检查点列表，恢复范围三选一：

| 恢复选项 | 场景 |
|---|---|
| 代码 + 对话一起回滚 | agent 改崩了，整轮撤销重来 |
| 只回滚对话 | 回到早先的思路分叉点，但保留现在的文件 |
| 只回滚代码 | 对话继续，文件回到某个检查点（修好代码后重试同一提示） |

```bash
pi install npm:@ayulab/pi-rewind
# 重启 pi 后：
/rewind       # 交互式检查点列表（含文件变更统计）
/checkpoint   # 检查点存储管理器（Ctrl+D 删除、Ctrl+P 切换路径显示）
```

配合 pi 原生树状 session（`/tree`）可做分支实验——试两种实现方案再择优；`ayu.rewind.restoreOnTree` 可配 `never` / `ask` / `always` 控制树导航时是否同步文件状态。fork/clone 会自动复制检查点存储。

注意事项：

- 基于 Git commit 做快照，**不要在超大目录**（如美术资产原始文件目录）里跑 pi + rewind，快照开销大；X12RigAnimTools 这类正常 git 仓库无问题
- `/resume`、`pi -r` 打开旧会话默认只恢复对话，文件恢复需显式开启 `ayu.checkpoint.restoreOnResume`
- 删除检查点存储会保留 pi 会话记录，但该会话的文件恢复能力随之失效
- GPL-3.0 许可 —— 本地工具使用无影响，不传染项目代码

> 💡 pi 包是能执行任意代码的 TypeScript 扩展（官方页面也有安全提示），装第三方包前扫一眼源码是好习惯。

---

## 五、pi-mcp-adapter 接入 Maya / MotionBuilder（实测配置）

### 5.1 为什么用 MCP 桥

Maya / MoBu 的代码必须在 DCC 进程内验证（`import pyfbsdk` 在独立进程直接失败），pi 本身碰不到 DCC；通过 pi-mcp-adapter 把自建的 maya-mcp / mobu-mcp server 接进来即可。

### 5.2 配置文件与优先级

pi-mcp-adapter 读取标准 MCP 配置，优先级（后者覆盖前者）：

1. `~/.config/mcp/mcp.json`（用户全局共享）
2. `~/.pi/agent/mcp.json`（Pi 全局覆盖）
3. `.mcp.json`（项目共享）
4. `.pi/mcp.json`（Pi 项目覆盖）

也支持 `imports` 直接吸收 Cursor / Claude Code / Codex 等宿主的既有配置（`/mcp setup` 引导导入）。

### 5.3 本机实测配置（`~/.pi/agent/mcp.json`）

```json
{
  "settings": { "toolPrefix": "short", "idleTimeout": 30 },
  "mcpServers": {
    "maya-mcp": {
      "command": "C:/Users/dalaotian/Documents/maya/scripts/mayaMCP/mayaMcpServer/maya_mcp_server.exe",
      "lifecycle": "lazy",
      "requestTimeoutMs": 120000
    },
    "mobu-mcp": {
      "command": "C:/Users/dalaotian/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe",
      "args": ["D:/Code/MoBuMCP/server/mobu_mcp_server.py"],
      "lifecycle": "lazy",
      "requestTimeoutMs": 120000
    }
  }
}
```

配置要点：

- **`lifecycle: "lazy"`**（默认）：pi 启动不连接，第一次调用工具时才拉起 server；工具元数据有磁盘缓存，search/describe 不需要活连接
- **`requestTimeoutMs: 120000`**：DCC 里跑重脚本（加载 DNA 等）默认超时不够，放宽到 2 分钟
- **`idleTimeout: 30`**：空闲 30 分钟才断开，避免来回切任务反复重启 server
- MoBu 侧前提：MoBuMCP 监听器需在 MoBu GUI 内手动启动（TCP 4600），播放/模态框会阻塞 OnUIIdle 任务

### 5.4 agent 侧用法（两段式）

```js
// 1. 发现工具（空参数 = 列出所有 server 状态）
mcp({ search: "maya" })

// 2. 调用工具 —— 注意 args 是 JSON 字符串，不是对象！
mcp({ tool: "maya_mcp_run_python_code_in_maya", args: '{"python_code": "...", "main_function": "..."}' })
```

如需让 DCC 工具直接出现在一级工具列表（免 search），在 server 配置加 `"directTools": true`，代价是每个工具约 150-300 token 常驻系统提示词。

### 5.5 验证结果（2026-07-22 实测通过）

```bash
pi -p "调用 mcp 工具检查 Maya 与 MoBu 状态"
```

| 目标 | 返回 |
|---|---|
| Maya 2024 | `{'maya_version': '2024', 'python_version': '3.10.8 ...'}` |
| MoBu 2019 | `{"connected": true, 'mobu_version': 19000.0, 'python_version': '2.7.11'}` |

---

## 六、坑点与注意事项

1. **`mcp` 工具的 `args` 参数是 JSON 字符串**，写成对象会报错。
2. **pi 无任何权限防护**，在重要仓库（美术资产库等）使用前先装 cc-safety-net 或权限扩展。
3. **新 server 首次配 `directTools` 时缓存不存在**，工具会先回落到 proxy 模式，用 `/mcp reconnect <server>` 强制建缓存。
4. **MCP 输出守卫**：默认单条工具输出截断到 50 KiB / 2000 行，超出部分落盘临时文件（路径附在结果里）；可用 `settings.outputGuard` 调整。
5. Windows 上 pi 依赖 bash，PowerShell-only 环境需先装 Git for Windows。
6. 各 pi session 各自拉起独立的 MCP server 进程（暂不支持跨 session 共享），多开 pi 时注意 DCC 监听端口冲突。

---

## 相关笔记

- [ClaudeCode](ClaudeCode.md)
- [opencode](opencode.md)
- [HermesAgent使用指南](HermesAgent%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97.md)
- [vibe-coding-guide](vibe-coding-guide.md)
