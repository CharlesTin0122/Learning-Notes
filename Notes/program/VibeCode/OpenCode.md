# OpenCode 使用指南(含 Oh My OpenAgent 插件)

> 适用版本:OpenCode ≥ 1.14.x / Oh My OpenAgent(原 oh-my-opencode)
> 最后更新:2026-05-13
> 官方仓库:[anomalyco/opencode](https://github.com/anomalyco/opencode)(MIT 协议,150K+ stars)

---

## 一、OpenCode 简介

**OpenCode** 是一款开源的、终端原生的 AI 编码代理(AI Coding Agent),由 [opencode.ai](https://opencode.ai/) 维护。其核心特点:

- **开源 + 终端优先**:CLI 即产品,亦提供 macOS/Windows/Linux 桌面应用(Beta)
- **模型无关**:支持 Anthropic、OpenAI、Gemini、Bedrock、Groq、Azure、OpenRouter,以及本地 Ollama;官方推荐 **OpenCode Zen** 精选模型清单
- **客户端/服务器架构**:可作为 headless HTTP 服务运行,提供 OpenAPI 与 SDK
- **内置两种 Agent**:`build`(完整权限)与 `plan`(只读分析,只输出实现思路),按 `Tab` 切换
- **TUI 基于 Bubble Tea**:支持 vim 风格编辑、SQLite 会话持久化、LSP 集成
- **可扩展**:支持 MCP、自定义 Agent、Plugin、ACP(Agent Client Protocol)与 GitHub Actions 触发

---

## 二、安装 OpenCode

### 2.1 一键安装(推荐)

```bash
# macOS / Linux / WSL
curl -fsSL https://opencode.ai/install | bash

# Windows PowerShell
irm https://opencode.ai/install.ps1 | iex
```

### 2.2 包管理器

```bash
# Node 系
npm  i -g opencode-ai
pnpm add -g opencode-ai
yarn global add opencode-ai
bun  add -g opencode-ai

# macOS / Homebrew(社区 tap)
brew install anomalyco/tap/opencode

# Windows
scoop install opencode
choco install opencode

# Arch Linux
paru -S opencode               # 或 yay -S opencode

# 跨平台版本管理
mise use -g opencode@latest

# Docker
docker run -it --rm -v $PWD:/workspace anomalyco/opencode
```

桌面应用(Beta):macOS(Apple Silicon / Intel)、Windows、Linux,可在 [opencode.ai](https://opencode.ai/) 直接下载。

### 2.3 配置模型 Provider

```bash
opencode auth login                       # 交互式选择 Provider
opencode auth login -p anthropic -m oauth # 指定 Provider 与认证方式
opencode auth list                        # 查看已配置 Provider
opencode auth logout                      # 退出登录
```

按提示填入 API Key 或走 OAuth。本地推理可指向 `http://localhost:11434`(Ollama)。

> **OpenCode Zen**:官方维护的"已验证模型清单",在 `auth login` 中选 `zen` 即可统一调度多家模型,免去逐个配置 Key。

---

## 三、OpenCode 基础用法

### 3.1 交互式 TUI

```bash
cd your-project
opencode

# 常用主入口参数
opencode -c                       # --continue 接续最近会话
opencode -s <sessionID>           # --session 指定会话
opencode --fork                   # 从某会话派生新分支
opencode -m anthropic/claude-opus-4-7  # 指定模型
opencode --agent build            # 指定启动 Agent
opencode --prompt "..."           # 启动时直接喂入首条提示
```

| 快捷键 | 作用 |
|--------|------|
| `Tab` | 切换 build / plan 模式 |
| `@` | 项目内文件模糊搜索(@ + 关键词,Enter 引用) |
| `Ctrl+K` | 命令/搜索面板 |
| `?` | TUI 内查看完整快捷键表 |
| `Ctrl+Esc` | (IDE 扩展)新开 OpenCode 终端会话 |
| `Cmd+Esc` / `Ctrl+Esc` | (IDE 扩展)在分屏中唤起 OpenCode |

> 完整的 vim 风格编辑键位与 keybinds 自定义,以 TUI 内 `?` 显示为准。

### 3.2 非交互(脚本场景)

```bash
opencode run "请为 utils.py 中的函数补全 type hint"

# 常用参数
opencode run "..." --thinking                       # 启用扩展思考(若模型支持)
opencode run "..." --share                          # 生成可分享的会话链接
opencode run "..." --dangerously-skip-permissions   # 跳过权限确认(慎用)
```

### 3.3 Headless 服务

```bash
opencode serve --port 4096 --hostname 127.0.0.1   # HTTP 服务,OpenAPI 文档在 /doc
opencode web                                       # 内嵌 Web UI
opencode attach [url]                              # 终端连入已运行的后端
opencode acp                                       # ACP 服务(stdin/stdout,nd-JSON)
```

配合官方 SDK:`@opencode-ai/sdk`(JS/TS)、`opencode-ai`(Python)。

### 3.4 常用 CLI 子命令

| 命令 | 说明 |
|------|------|
| `opencode agent create` / `agent list` | 创建/列出自定义 Agent |
| `opencode models [provider] [--refresh]` | 查看/刷新可用模型 |
| `opencode mcp add` / `mcp list` / `mcp auth` / `mcp debug` | 管理 MCP(Model Context Protocol)服务器 |
| `opencode session list -n 20` | 列会话(支持 `--format json`) |
| `opencode session delete <id>` | 删除会话 |
| `opencode export [sessionID]` / `import <file>` | 导出/导入会话 |
| `opencode stats` | 查看 Token 与费用统计 |
| `opencode pr <number>` | 拉取 PR 上下文进入编辑流程 |
| `opencode github install` / `github run` | 安装 GitHub Actions,实现 `/oc` 评论触发 |
| `opencode plugin <module>` | 加载/管理插件 |
| `opencode db` / `db path` | 查看本地 SQLite 会话库 |
| `opencode upgrade [target]` | 升级到指定版本 |
| `opencode uninstall` | 卸载 |

---

## 四、Oh My OpenAgent 插件

> 项目地址:[code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)
> 官网:[ohmyopenagent.com](https://ohmyopenagent.com/) (旧域名 [ohmyopencode.com](https://ohmyopencode.com/))
>
> **改名说明**:项目已从 `oh-my-opencode` 改名为 `oh-my-openagent`,npm 包双发布。建议统一使用新名 `oh-my-openagent`,旧 CLI 名称在过渡期保留兼容。维护者建议简称 **omo** 或 **Sisyphus**。

### 4.1 它解决什么问题

将 OpenCode 升级为**多 Agent 编排系统**:

- **并行后台 Agent**:研究 / 实现 / 验证并发执行
- **Hash 锚定编辑**:`LINE#ID` 内容哈希校验,Grok Code Fast 1 成功率从 6.7% → 68.3%
- **IntentGate**:先分类意图(研究/实现/排查/修复)再路由到对应 Agent
- **LSP + AST 工具**:工作区级 rename、跳转定义、引用查询、构建前诊断
- **52 个生命周期 Hook + 26 个内置工具**
- **多模型协同**:Claude 负责编排、GPT 深推理、Gemini 前端、Mini 模型处理琐事

### 4.2 内置 Agent(共 11 个)

分为 **4 个主 Agent + 7 个 Subagent**:

#### 主 Agent(可独立驱动会话)

| Agent | 角色 |
|-------|------|
| **Sisyphus** | 主编排器(默认入口) |
| **Hephaestus** | 深度自主工作者(长任务、重 IO) |
| **Prometheus** | 战略规划师(访谈式生成 plan) |
| **Atlas** | 执行指挥(跨文件/跨模块任务承载) |

#### 子 Agent(由主 Agent 调度,不直接对话)

| Subagent | 角色 |
|----------|------|
| **Oracle** | 只读架构咨询、深度推理 |
| **Librarian** | 文档/上下文检索(走 context7) |
| **Explore** | 快速 grep / 代码库探索 |
| **Sisyphus-Junior** | 按类别分发琐碎子任务 |
| **Metis** | 计划缺口分析、方案顾问 |
| **Momus** | 高准确度评审(代码/方案双盲复核) |
| **Multimodal Looker** | 视觉/截图分析(UI、设计稿、报错截图) |

### 4.3 安装

前置:OpenCode ≥ 1.0.150(建议 ≥ 1.14)。

```bash
# 方式一:bunx(官方推荐,无需全局装)
bunx oh-my-openagent install

# 方式二:npm 全局
npm install -g oh-my-openagent
oh-my-openagent install
```

安装后检查 `~/.config/opencode/opencode.json`,其 `plugin` 数组应包含:

```jsonc
{
  "plugin": ["oh-my-openagent"]    // 旧条目 "oh-my-opencode" 仍兼容,但会有 warning
}
```

### 4.4 验证安装

```bash
bunx oh-my-openagent doctor                       # 环境自检
bunx oh-my-openagent get-local-version            # 查看当前版本
bunx oh-my-openagent refresh-model-capabilities   # 刷新模型能力清单
bunx oh-my-openagent run "..."                    # 非交互执行
```

### 4.5 启动与三种工作模式

```bash
cd your-project
opencode
```

OpenCode 启动后会自动加载插件,默认进入 **Sisyphus** 编排模式,支持三种节奏:

| 模式 | 触发方式 | 适用场景 |
|------|----------|----------|
| **Direct Prompting** | 直接发问 | 简短问答、单点修改 |
| **Prometheus Mode** | `Tab` 切到 plan,然后 `/start-work` 落地 | 需要先访谈、确认需求边界,再交给执行层 |
| **Ultrawork** | 输入 `ultrawork` 或 `ulw` | 全自动多 Agent 并行,适合长任务无人值守 |

---

## 五、Oh My OpenAgent 配置

### 5.1 配置文件位置(就近优先)

| 路径 | 作用域 |
|------|--------|
| `<project>/.opencode/oh-my-openagent.json` | 项目级 |
| `~/.config/opencode/oh-my-openagent.json` | 用户级 |
| `<project>/.sisyphus/plans/` | Prometheus 生成的计划文档 |
| `<project>/.sisyphus/boulder.json` | Sisyphus 当前会话状态 |
| `~/.omo/teams/<name>/config.json` | 团队模式共享配置 |

> 支持 **JSONC**(注释 + 尾逗号)。文件名 `oh-my-opencode.json` 与 `oh-my-openagent.json` 在过渡期均被识别。
> 查找规则:从工作目录向上递归至 `$HOME`,**越近的配置优先级越高**;若工作目录在 `$HOME` 之外则仅检查当前目录。

### 5.2 示例配置

```jsonc
{
  // 覆盖单个 Agent 的模型与温度
  "agents": {
    "Sisyphus": {
      "model": "anthropic/claude-opus-4-7",
      "temperature": 0.2
    },
    "Hephaestus": {
      "model": "openai/gpt-5.4-mini",
      "permissions": ["write", "exec"]
    },
    "Oracle": {
      "model": "anthropic/claude-opus-4-7",
      "thinking": true            // 开启扩展思考
    }
  },

  // 后台任务并发上限
  "background": {
    "max_concurrency": 4
  },

  // 内置 MCP
  "mcp": {
    "websearch": { "enabled": true },   // 基于 Exa
    "context7":  { "enabled": true },   // 文档检索
    "grep_app":  { "enabled": true }    // GitHub 代码搜索
  },

  // 内置技能(skills)
  "skills": {
    "playwright": { "enabled": true },
    "git-master": { "enabled": true }
  }
}
```

### 5.3 环境变量

| 变量 | 作用 |
|------|------|
| `OPENCODE_DEFAULT_AGENT` | 设置 OpenCode 启动默认 Agent(如 `Sisyphus`) |
| `OMO_SEND_ANONYMOUS_TELEMETRY=0` | 关闭匿名遥测(默认每台机器每日 UTC 上报一次哈希化安装标识,不含主机名) |
| `OMO_DISABLE_POSTHOG=1` | 关闭 PostHog 分析上报 |

```bash
export OMO_SEND_ANONYMOUS_TELEMETRY=0
export OMO_DISABLE_POSTHOG=1
export OPENCODE_DEFAULT_AGENT=Sisyphus
```

---

## 六、典型工作流示例

### 6.1 让 Sisyphus 编排一个 Maya 批处理脚本任务

```text
> 帮我写一个 Maya 批处理脚本:遍历 //assets/char/ 目录下所有 .ma 文件,
  检查骨骼命名是否符合 spine_xx / arm_l_xx 规范,生成 CSV 报告。
  使用 pymel,加 try-except 与日志输出。
```

Sisyphus 通常会:

1. **IntentGate** 判定为 implementation
2. 派发 **Prometheus** 生成计划(写入 `.sisyphus/plans/`)
3. **Librarian** 查阅 pymel 文档(走 context7 MCP)
4. **Hephaestus** 并行写 `batch_check_skel.py` 与单元测试
5. **Oracle** 复核命名正则边界情况
6. **Momus** 做最后评审,汇总结果交还主会话

### 6.2 Plan 模式安全审阅

```text
按 Tab 切到 plan
> 评估把 UE5 ChaosCloth 解算从 Tick 移到 AsyncTask 的可行性,列出风险点。
```

Plan 模式下插件不会写盘,只输出方案与影响面分析,适合上线前决策评估。

### 6.3 Ultrawork 全自动模式(长任务无人值守)

```text
> ulw 把仓库里所有 pymel.core 的 import 改写成 pm 别名,并同步修改调用点;
  跑完单测,提交到新分支 refactor/pymel-alias,开 PR。
```

插件会自动调度 Explore → Atlas → Hephaestus → Momus 流水线,最后用 `opencode github` 开 PR。

### 6.4 TA 常用场景速查

| 场景 | 建议 Agent 组合 | 关键 MCP |
|------|-----------------|----------|
| 阅读未知 Rig 代码库 | Explore + Librarian + Oracle | grep_app |
| 批量资产处理脚本 | Sisyphus → Prometheus → Hephaestus | context7 |
| UI 截图 + 修 bug | Multimodal Looker + Hephaestus | - |
| UE5 Python API 文档检索 | Librarian | context7 |
| MotionBuilder 老项目审计 | Atlas + Oracle | - |

---

## 七、常见问题

| 问题 | 处理 |
|------|------|
| 启动报 OpenCode 版本过低 | `npm i -g opencode-ai@latest`(或 `opencode upgrade`),要求 ≥ 1.0.150,建议 ≥ 1.14 |
| 插件未生效 | 检查 `opencode.json` 是否含 `"oh-my-openagent"`;运行 `bunx oh-my-openagent doctor` |
| 后台 Agent 卡住 | 调低 `background.max_concurrency`;TUI 中 `/session show` 查看 token 占用,或 `opencode stats` 看用量 |
| Anthropic 模型被阻断 | 项目自述提到 Anthropic 曾以本插件为由限制 OpenCode 访问;切换至 OpenRouter / Bedrock 路由,或使用本地 Ollama |
| 想要 Claude Code 兼容层 | 插件自带兼容层,可直接复用 Claude Code 的提示/工具协议 |
| Windows 下路径报错 | 使用 WSL,或在配置文件里用正斜杠 `/`,避免反斜杠被转义 |
| 会话数据库损坏 | `opencode db path` 找到 SQLite 文件,备份后删除,会话会重建;历史可用 `opencode export` 提前备份 |
| 切换 Provider 后模型不刷新 | 执行 `opencode models --refresh` 与 `bunx oh-my-openagent refresh-model-capabilities` |

---

## 八、参考链接

- [OpenCode 官网](https://opencode.ai/)
- [OpenCode 文档](https://opencode.ai/docs/)
- [OpenCode CLI 文档](https://opencode.ai/docs/cli/)
- [OpenCode GitHub(anomalyco/opencode)](https://github.com/anomalyco/opencode)
- [OpenCode Zen 模型清单](https://opencode.ai/zen)
- [awesome-opencode 资源集](https://github.com/awesome-opencode/awesome-opencode)
- [Oh My OpenAgent 官网](https://ohmyopenagent.com/)
- [Oh My OpenAgent 文档](https://ohmyopenagent.com/docs)
- [Oh My OpenAgent GitHub](https://github.com/code-yeongyu/oh-my-openagent)
- [Oh My OpenAgent DeepWiki](https://deepwiki.com/code-yeongyu/oh-my-openagent)
- [安装指南(官方)](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/guide/installation.md)
- [配置参考(官方)](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/reference/configuration.md)
- [专用 Agent 深度解析(第三方)](https://www.glukhov.org/ai-devtools/opencode/oh-my-opencode-agents/)
