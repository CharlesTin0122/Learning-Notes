# OpenCode 使用指南与操作手册

本指南旨在帮助开发者快速掌握 **OpenCode** 的核心功能，并详细介绍如何配合 **oh-my-OpenAgents** 插件极大提升开发效率。

---

## 1. 什么是 OpenCode？

**OpenCode** 是一款开源的智能编程辅助命令行工具（CLI）。它能够通过自然语言理解开发者的意图，自动生成代码、解释复杂逻辑、重构项目结构，并能够直接与本地文件系统和终端进行交互。

### 核心特性

- 💬 **自然语言编程**：将自然语言指令转化为可执行代码。
- 📁 **上下文感知**：自动读取当前工作目录和项目依赖，给出精准建议。
- ⚡ **无缝终端集成**：支持在终端内直接运行、测试和调试生成的代码。

---

## 2. 基础安装与配置

### 2.1 安装 OpenCode

确保您的系统已安装 Python 3.8+ 或 Node.js（取决于具体版本要求），在终端中执行：

```bash
# 使用 pip 安装
pip install opencode-cli

# 或者使用 npm 安装
npm install -g opencode
```

### 2.2 初始化与鉴权

首次安装后，需要进行初始化以配置大模型 API Key（如 OpenAI、Anthropic 或本地模型）：

```bash
opencode init
```

按提示输入您的 API 密钥及默认偏好设置。配置文件通常保存在 `~/.opencode/config.yaml`。

---

## 3. 常用指令与用法

OpenCode 提供了丰富的命令行指令，以下是日常开发中最常用的几个：

### 3.1 基础对话与代码生成

```bash
# 在终端直接提问
opencode ask "如何在 Python 中反转一个链表？"

# 让 OpenCode 生成特定的脚本文件
opencode generate "编写一个批量重命名当前目录下所有图片为序列号的 Python 脚本" -o rename.py
```

### 3.2 项目级操作

```bash
# 分析当前项目的结构和潜在报错
opencode analyze ./src

# 代码重构建议
opencode refactor ./utils/helpers.js --style="clean-code"
```

### 3.3 交互式模式

```bash
opencode chat
```

进入持续交互的对话模式，适合进行复杂的、需要多轮沟通的任务（如系统架构设计或复杂的 Bug 排查）。

---

## 4. 进阶：配合 oh-my-OpenAgents 插件

**oh-my-OpenAgents** 是一个为 OpenCode 社区驱动的扩展框架（灵感来源于 oh-my-zsh），它提供了丰富的主题、快捷别名（Aliases）以及针对不同开发场景的预设智能体（Agents）。

### 4.1 安装 oh-my-OpenAgents

执行以下一键安装脚本：

```bash
curl -fsSL https://raw.githubusercontent.com/opencode/oh-my-openagents/main/install.sh | bash
```

安装完成后，重启您的终端。

### 4.2 启用插件

打开 OpenCode 的插件配置文件（通常在 `~/.opencode/plugins.yaml`），确保包含以下内容：

```yaml
plugins:
  - oh-my-openagents
```

### 4.3 核心功能与用法

#### a) 快捷命令别名 (Aliases)

oh-my-OpenAgents 提供了大量缩写命令，节省敲击键盘的时间：

- `oca` = `opencode ask`
- `ocg` = `opencode generate`
- `occ` = `opencode chat`
- `ocf` = `opencode fix` (自动修复最后一次编译/运行错误)

#### b) 专属领域 Agents 唤醒

您可以直接唤醒针对特定领域的专家级 Agent。例如，作为动画 TA 或技术美术，您可以唤醒专属的 Python/Maya 绑定助手：

```bash
# 唤醒 Maya/Python 绑定专家
oca @ta-maya "写一个批量给选中骨骼添加控制器的 Python 脚本"

# 唤醒 Unreal Engine 蓝图/C++ 助手
oca @ue5 "如何通过 C++ 暴露一个带有动画蒙太奇参数的函数给蓝图？"
```

#### c) 自动化工作流 (Workflows)

使用 `oma` (oh-my-agents) 指令执行一键式预设任务：

```bash
# 自动化的代码审查工作流
oma run code-review --target=./src

# 自动生成当前目录下的 README.md 文档
oma run auto-readme
```

---

## 5. 最佳实践与注意事项

1. **上下文限制**：在使用 `opencode analyze` 提交整个项目时，请注意通过 `.opencodex` 文件（类似 `.gitignore`）忽略不必要的二进制文件或大型素材（如 `.uasset`, `.mb`），以免消耗过多 Token。
2. **安全执行**：当 OpenCode 提议执行系统命令（如 `rm`, `pip install`）时，始终保持默认的“执行前确认”机制开启。
3. **自定义提示词**：如果您从事游戏研发（如 MotionBuilder/Maya TA），可以在 `~/.opencode/prompts/` 下创建自己的专属预设，让 AI 默认以 TA 的思维方式回答问题。

---

_文档版本：v1.2 | 更新日期：2026-05_