# Claude Code 使用指南

> Claude Code 是 Anthropic 推出的 AI 驱动的命令行编程助手，能够直接在终端中理解代码库、执行任务、调试问题，是开发者的智能编程搭档。

---

## 目录

1. [安装与配置](https://sider.ai/zh-CN/chat#%E4%B8%80%E5%AE%89%E8%A3%85%E4%B8%8E%E9%85%8D%E7%BD%AE)
2. [启动与基本交互](https://sider.ai/zh-CN/chat#%E4%BA%8C%E5%90%AF%E5%8A%A8%E4%B8%8E%E5%9F%BA%E6%9C%AC%E4%BA%A4%E4%BA%92)
3. [核心指令速查](https://sider.ai/zh-CN/chat#%E4%B8%89%E6%A0%B8%E5%BF%83%E6%8C%87%E4%BB%A4%E9%80%9F%E6%9F%A5)
4. [文件与代码操作](https://sider.ai/zh-CN/chat#%E5%9B%9B%E6%96%87%E4%BB%B6%E4%B8%8E%E4%BB%A3%E7%A0%81%E6%93%8D%E4%BD%9C)
5. [Git 工作流集成](https://sider.ai/zh-CN/chat#%E4%BA%94git-%E5%B7%A5%E4%BD%9C%E6%B5%81%E9%9B%86%E6%88%90)
6. [项目理解与分析](https://sider.ai/zh-CN/chat#%E5%85%AD%E9%A1%B9%E7%9B%AE%E7%90%86%E8%A7%A3%E4%B8%8E%E5%88%86%E6%9E%90)
7. [调试与测试](https://sider.ai/zh-CN/chat#%E4%B8%83%E8%B0%83%E8%AF%95%E4%B8%8E%E6%B5%8B%E8%AF%95)
8. [自定义配置](https://sider.ai/zh-CN/chat#%E5%85%AB%E8%87%AA%E5%AE%9A%E4%B9%89%E9%85%8D%E7%BD%AE)
9. [高级用法与技巧](https://sider.ai/zh-CN/chat#%E4%B9%9D%E9%AB%98%E7%BA%A7%E7%94%A8%E6%B3%95%E4%B8%8E%E6%8A%80%E5%B7%A7)
10. [常见问题](https://sider.ai/zh-CN/chat#%E5%8D%81%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98)

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

# 直接传入任务，非交互模式执行
claude "帮我解释这个项目的结构"

# 指定工作目录启动
claude --cwd /path/to/your/project
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

|指令|说明|
|---|---|
|`/help`|显示帮助信息和可用命令列表|
|`/clear`|清除当前对话上下文，开始新会话|
|`/compact`|压缩对话历史，节省 Token，保留核心上下文|
|`/cost`|查看当前会话的 Token 消耗和费用估算|
|`/status`|显示当前状态、模型信息和配置|
|`/model`|切换使用的模型（如 claude-opus / sonnet）|
|`/vim`|切换 Vim 键位模式输入|
|`/exit`|退出 Claude Code|

### 快捷键

|快捷键|功能|
|---|---|
|`↑ / ↓`|翻阅历史输入|
|`Esc`|中断当前响应|
|`Ctrl + C`|强制中止或退出|
|`Ctrl + L`|清屏|
|`Tab`|自动补全文件路径|

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

## 八、自定义配置

### CLAUDE.md 项目配置文件

在项目根目录创建 `CLAUDE.md`，Claude 每次启动会自动读取，用于传达项目规范：

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

### 全局配置

```bash
# 配置文件位置
~/.claude/config.json

# 常用配置项示例
{
  "model": "claude-sonnet-4-5",
  "theme": "dark",
  "vim": false,
  "autoApprove": false
}
```

### 权限控制（--allowedTools）

```bash
# 只允许读取文件，不允许执行命令（安全模式）
claude --allowedTools "Read,Write"

# 允许所有工具
claude --allowedTools "all"

# 禁止执行 Shell 命令
claude --disallowedTools "Bash"
```

---

## 九、高级用法与技巧

### 非交互式（脚本）模式

适合集成到 CI/CD 或自动化脚本：

```bash
# -p 参数直接执行任务后退出
claude -p "检查代码中是否有 TODO 注释，列出所有文件和行号"

# 结合管道使用
cat error.log | claude -p "分析这个错误日志，找出根本原因"

# 输出结果到文件
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

---

## 十、常见问题

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
/model claude-haiku-3-5
```

### Q4：如何处理大型代码库？

```
# 先给出明确的范围限定
只分析 src/core/ 模块，不要读取其他目录

# 分模块逐步处理
先帮我理解 models/ 层，下一步再看 services/ 层
```

### Q5：命令执行失败或卡住怎么办？

```bash
# 按 ESC 中断当前任务
# 然后描述清楚问题重新尝试

# 或直接重启会话
/clear
```

---

## 最佳实践总结

|场景|推荐做法|
|---|---|
|初次接触新项目|先让 Claude 做整体架构分析，再深入细节|
|复杂功能开发|拆分步骤，逐步确认，避免一次性交付大量改动|
|调试问题|提供完整的错误堆栈和复现步骤|
|长时间工作|定期 `/compact` 压缩上下文，保持响应质量|
|团队项目|维护好 `CLAUDE.md`，统一 AI 行为规范|
|自动化场景|使用 `-p` 非交互模式集成到脚本流程|

---

_本文档基于 Claude Code 当前版本整理，功能可能随版本更新而变化。_ _官方文档：[https://docs.anthropic.com/claude-code](https://docs.anthropic.com/claude-code)_