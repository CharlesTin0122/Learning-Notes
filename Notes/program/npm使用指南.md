# npm 使用指南

> 一份面向技术美术 / 开发者的 npm 实用指南，从基础概念到日常命令，并重点介绍如何用 npm 安装与管理 **Vibe Coding（AI 编程）命令行工具**。

---

## 目录

1. [什么是 npm](#一什么是-npm)
2. [安装 Node.js 与 npm](#二安装-nodejs-与-npm)
3. [npm 核心概念](#三npm-核心概念)
4. [常用命令速查](#四常用命令速查)
5. [全局安装 vs 本地安装](#五全局安装-vs-本地安装)
6. [package.json 详解](#六packagejson-详解)
7. [配置镜像源（中国用户必看）](#七配置镜像源中国用户必看)
8. [npx 与 npm 的区别](#八npx-与-npm-的区别)
9. [用 npm 安装 Vibe Coding 工具](#九用-npm-安装-vibe-coding-工具)
10. [Vibe Coding 工具的日常管理](#十vibe-coding-工具的日常管理)
11. [常见问题与排错](#十一常见问题与排错)

---

## 一、什么是 npm

**npm（Node Package Manager）** 是 Node.js 的官方包管理器，类似于：

- Python 的 `pip`
- Windows 的 [Scoop](Scoop使用入门.md)
- Rust 的 `cargo`

它主要做三件事：

1. **安装/管理依赖包**：从 [npm registry](https://www.npmjs.com/) 下载第三方库。
2. **运行脚本**：通过 `package.json` 中定义的 `scripts` 执行命令。
3. **发布包**：把你自己的代码发布到 npm 仓库供他人使用。

> 💡 对技术美术而言，npm 最大的价值之一是：**很多 AI 编程命令行工具（Claude Code、Gemini CLI、Codex CLI 等）都通过 npm 全局安装。** 掌握 npm 就能轻松管理这些 Vibe Coding 工具。

---

## 二、安装 Node.js 与 npm

npm 随 Node.js 一起安装，所以只需安装 Node.js 即可。

### 方式 1：Scoop 安装（推荐，Windows）

如果你已经用了 [Scoop](Scoop使用入门.md)：

```powershell
# 安装 LTS 长期支持版本（推荐）
scoop install nodejs-lts

# 或安装最新版
scoop install nodejs
```

### 方式 2：官网安装包

从 [Node.js 官网](https://nodejs.org/) 下载 LTS 版本的安装包，一路下一步即可。

### 方式 3：nvm 管理多版本（进阶）

如果需要在多个 Node 版本间切换，可使用 `nvm-windows`：

```powershell
scoop install nvm
nvm install lts
nvm use lts
```

### 验证安装

```powershell
node -v      # 查看 Node.js 版本，如 v20.11.0
npm -v       # 查看 npm 版本，如 10.2.4
```

> ⚠️ 安装后建议先[配置镜像源](#七配置镜像源中国用户必看)，否则在国内下载速度会很慢甚至失败。

---

## 三、npm 核心概念

| 概念 | 说明 |
|------|------|
| **package（包）** | 一个被发布到 registry 的代码模块 |
| **registry** | 包仓库，默认是 `https://registry.npmjs.org/` |
| **package.json** | 项目清单文件，记录依赖、脚本、元信息 |
| **package-lock.json** | 锁定依赖的精确版本，保证环境一致 |
| **node_modules** | 存放已安装依赖的目录（通常加入 `.gitignore`） |
| **dependencies** | 生产依赖，项目运行必需 |
| **devDependencies** | 开发依赖，仅开发/构建时需要 |
| **global（全局）** | 安装到系统级目录，可在任意位置当命令使用 |

---

## 四、常用命令速查

npm 命令结构通常为 `npm <命令> [参数]`：

```powershell
# 初始化项目，生成 package.json
npm init              # 交互式
npm init -y           # 全部使用默认值

# 安装依赖
npm install                 # 安装 package.json 中所有依赖
npm install <包名>          # 安装并写入 dependencies
npm install <包名> -D       # 安装到 devDependencies（开发依赖）
npm install <包名> -g       # 全局安装
npm install <包名>@<版本>   # 安装指定版本，如 npm install eslint@8.0.0

# 卸载
npm uninstall <包名>        # 本地卸载
npm uninstall <包名> -g     # 全局卸载

# 更新
npm update                  # 更新所有依赖
npm update <包名>           # 更新指定包
npm update <包名> -g        # 更新全局包

# 查看
npm list                    # 查看本地已安装依赖
npm list -g --depth=0       # 查看全局已安装的包（仅顶层）
npm view <包名>             # 查看包的信息
npm view <包名> versions    # 查看包的所有可用版本
npm outdated                # 检查哪些包有新版本

# 运行脚本
npm run <脚本名>            # 运行 package.json 中 scripts 定义的命令
npm start                   # 等价于 npm run start
npm test                    # 等价于 npm run test

# 缓存与排错
npm cache clean --force     # 清理缓存
npm config list             # 查看当前配置
```

> 💡 `npm install` 可简写为 `npm i`，`npm install -g` 可简写为 `npm i -g`。

---

## 五、全局安装 vs 本地安装

这是新手最容易困惑的地方，务必理解：

| | 本地安装（默认） | 全局安装（`-g`） |
|------|----------------|------------------|
| 安装位置 | 当前项目的 `node_modules/` | 系统全局目录 |
| 适用场景 | 项目的依赖库 | 命令行工具（CLI） |
| 调用方式 | 代码 `require`/`import`，或 `npm run` | 直接在终端当命令用 |
| 典型例子 | `react`、`lodash` | `claude`、`gemini`、`eslint` |

**关键判断**：如果一个包是「能在终端里直接敲命令运行的工具」，就用 `-g` 全局安装。**几乎所有 Vibe Coding 工具都属于这一类。**

查看全局安装目录：

```powershell
npm root -g       # 全局 node_modules 路径
npm prefix -g     # 全局安装前缀路径
```

---

## 六、package.json 详解

`package.json` 是 Node 项目的核心配置文件。一个典型示例：

```json
{
  "name": "my-tool",
  "version": "1.0.0",
  "description": "一个示例工具",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "build": "tsc",
    "lint": "eslint ."
  },
  "dependencies": {
    "lodash": "^4.17.21"
  },
  "devDependencies": {
    "eslint": "^8.0.0"
  }
}
```

**版本号符号说明**（语义化版本 `主版本.次版本.修订号`）：

| 符号 | 含义 | 示例 |
|------|------|------|
| `^` | 允许更新次版本与修订号 | `^4.17.21` → 可升到 `4.x.x` |
| `~` | 仅允许更新修订号 | `~4.17.21` → 可升到 `4.17.x` |
| 无符号 | 锁定精确版本 | `4.17.21` |
| `*` | 任意最新版本 | `*` |

**scripts 的用法**：定义在 `scripts` 里的命令可通过 `npm run <名字>` 执行，这是项目自动化的核心。

---

## 七、配置镜像源（中国用户必看）

默认 registry 在国内访问慢，建议切换为国内镜像。

### 查看与设置镜像源

```powershell
# 查看当前源
npm config get registry

# 设置为淘宝镜像（npmmirror）
npm config set registry https://registry.npmmirror.com

# 恢复官方源
npm config set registry https://registry.npmjs.org
```

### 使用 nrm 管理多个源（进阶）

```powershell
npm install -g nrm
nrm ls            # 列出可用源
nrm use taobao    # 切换到淘宝源
nrm test          # 测试各源速度
```

> ⚠️ **注意**：部分 Vibe Coding 工具（如 Claude Code）的运行依赖于访问 Anthropic 官方 API，**镜像源只影响 npm 下载速度，不影响工具运行时的网络请求**。如果工具运行报网络错误，需要单独配置代理（见[排错章节](#十一常见问题与排错)）。

---

## 八、npx 与 npm 的区别

`npx` 随 npm 一起安装，用于**临时执行包，而无需全局安装**：

```powershell
# 临时运行一个包（用完即弃，不污染全局环境）
npx create-react-app my-app

# 等价于：先 npm i -g create-react-app，再运行，再卸载
```

**何时用 npx**：

- 只想用一次某个脚手架工具（如 `create-*` 系列）。
- 想试用某个 CLI 工具的最新版而不想全局安装。

**何时用 npm i -g**：

- 频繁使用的工具（如每天都用的 Vibe Coding 工具），全局安装更方便、启动更快。

---

## 九、用 npm 安装 Vibe Coding 工具

这是本指南的重点。**Vibe Coding（氛围编程 / AI 辅助编程）** 工具大多是 Node.js 编写的命令行程序，通过 npm 全局安装。

> 📖 关于 Vibe Coding 的方法论与工作流程，见 [Vibe Coding 实践指南](VibeCode/vibe-coding-guide.md)。

### 1. Claude Code（Anthropic）

Anthropic 官方的命令行 AI 编程助手，本指南所在环境的核心工具。

```powershell
# 全局安装
npm install -g @anthropic-ai/claude-code

# 启动（在项目目录下运行）
claude

# 查看版本
claude --version
```

> 💡 安装后在项目根目录运行 `claude`，它会读取项目里的 `CLAUDE.md` 作为上下文规范。

### 2. Gemini CLI（Google）

Google 官方的开源命令行 AI 编程工具。

```powershell
npm install -g @google/gemini-cli

# 启动
gemini
```

### 3. OpenAI Codex CLI（OpenAI）

OpenAI 的命令行编程代理。

```powershell
npm install -g @openai/codex

# 启动
codex
```

### 4. opencode

开源、模型无关（支持多种 LLM）的终端编程代理。

```powershell
npm install -g opencode-ai

# 启动
opencode
```

> 📖 本库中已有相关笔记：[opencode](VibeCode/opencode.md)、[ClaudeCode](VibeCode/ClaudeCode.md)。

### 5. 其他相关工具

```powershell
# Cline / Continue 等多为 VSCode 插件，不通过 npm 安装

# 一些通用 AI 辅助 CLI（按需选择）
npm install -g aichat        # 示例：通用聊天 CLI
```

### 安装对照表

| 工具 | 厂商 | npm 包名 | 启动命令 |
|------|------|----------|----------|
| Claude Code | Anthropic | `@anthropic-ai/claude-code` | `claude` |
| Gemini CLI | Google | `@google/gemini-cli` | `gemini` |
| Codex CLI | OpenAI | `@openai/codex` | `codex` |
| opencode | 开源社区 | `opencode-ai` | `opencode` |

> ⚠️ npm 包名可能随官方调整而变化。安装前可先用 `npm view <包名>` 确认包是否存在、最新版本号是多少。

---

## 十、Vibe Coding 工具的日常管理

把这些 AI CLI 工具当作普通的全局 npm 包来管理即可。

```powershell
# 查看已安装的全局工具及版本
npm list -g --depth=0

# 更新某个工具到最新版（AI 工具迭代很快，建议定期更新）
npm update -g @anthropic-ai/claude-code

# 一次性更新所有全局包
npm update -g

# 卸载工具
npm uninstall -g @anthropic-ai/claude-code

# 检查工具是否有新版本
npm outdated -g
```

> 💡 **实用建议**：AI 编程工具迭代极快（常常一周多个版本），遇到 bug 或功能缺失时，**先 `npm update -g <工具>` 升级到最新版**往往能解决问题。

---

## 十一、常见问题与排错

### 1. `npm` 不是内部或外部命令

Node.js 未正确安装或环境变量未配置。重新安装 Node.js（推荐用 [Scoop](Scoop使用入门.md)），或重启终端使环境变量生效。

### 2. 全局安装的命令无法运行

全局 bin 目录未加入 `PATH`。查看路径：

```powershell
npm prefix -g
```

把输出的目录（Windows 下通常是该目录本身）加入系统 `PATH` 环境变量。用 Scoop 安装的 Node 一般已自动处理。

### 3. 安装速度慢 / 下载失败

切换国内镜像源（见[第七章](#七配置镜像源中国用户必看)），或清理缓存后重试：

```powershell
npm cache clean --force
npm install
```

### 4. 权限错误（EACCES / EPERM）

Windows 下尽量避免用 `sudo` 思路。建议：

- 用 Scoop 安装的 Node（用户级目录，无需管理员权限）。
- 或以管理员身份运行一次终端再安装全局包。

### 5. Vibe Coding 工具运行时报网络错误

镜像源只影响 npm 下载，**不影响工具运行时调用 AI API**。如果工具启动后连不上服务，需配置代理（以 Clash 默认端口为例）：

```powershell
# 在 PowerShell 中临时设置代理环境变量
$env:HTTPS_PROXY="http://127.0.0.1:7890"
$env:HTTP_PROXY="http://127.0.0.1:7890"

# 然后再启动工具
claude
```

端口号根据自己的代理软件设置修改。

### 6. 版本冲突 / 依赖损坏

删除 `node_modules` 和锁文件后重装：

```powershell
# PowerShell
Remove-Item -Recurse -Force node_modules, package-lock.json
npm install
```

---

## 相关笔记

- [Scoop 使用入门](Scoop使用入门.md) —— Windows 包管理器，可用于安装 Node.js
- [Vibe Coding 实践指南](VibeCode/vibe-coding-guide.md) —— AI 辅助编程的方法论
- [ClaudeCode](VibeCode/ClaudeCode.md)
- [opencode](VibeCode/opencode.md)

---

> **一句话总结**：npm 是 Node 生态的包管理器，对技术美术最实用的场景就是用 `npm install -g` 安装并用 `npm update -g` 维护各类 Vibe Coding 命令行工具。
