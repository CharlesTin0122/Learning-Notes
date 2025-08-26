UV 是一个高性能的 Python 包管理和项目管理工具，由 Astral 开发，使用 Rust 编写，旨在替代传统的 Python 工具如 `pip`、`virtualenv`、`poetry` 等。它以极快的速度（号称比 `pip` 快 10-100 倍）、现代化的依赖管理和统一的工作流为特点，简化了 Python 项目的环境配置、依赖管理和命令行工具运行等操作。UV 的设计目标是将多种工具的功能整合到一个命令行工具中，提供更高效、更一致的开发体验。

以下是对 UV 工具的详细介绍及其基本使用方法：

---

### **UV 简介**

UV 是 Astral（Ruff 的开发者）推出的一款现代 Python 包管理工具，解决了 Python 生态系统中常见的痛点，例如依赖安装缓慢、依赖冲突、环境管理复杂等。UV 的核心特点包括：

1. **极快的速度**：UV 使用 Rust 实现，采用并行下载和优化的依赖解析器，安装速度远超 `pip`。
2. **内置虚拟环境管理**：无需手动创建和激活虚拟环境，UV 自动处理。
3. **现代化的依赖管理**：通过 `pyproject.toml` 和 `uv.lock` 文件支持精确的依赖锁定，确保跨环境的可重现性。
4. **多功能性**：支持包管理、虚拟环境管理、Python 版本管理、项目初始化、脚本运行和命令行工具管理，取代了 `pip`、`pipx`、`poetry`、`pyenv` 等多种工具。
5. **兼容性**：与现有 Python 生态系统（如 `requirements.txt` 和 PyPI）无缝兼容，支持现代 Python 打包标准。
6. **低资源占用**：内存和 CPU 使用效率高，适合大型项目和 CI/CD 场景。

UV 的适用场景包括个人项目、大型应用开发、命令行工具运行以及快速原型设计等。

---

### **UV 的核心功能**

1. **包管理**：快速安装、更新和移除 Python 包，支持版本约束和依赖锁定。
2. **虚拟环境管理**：自动创建和管理项目隔离的虚拟环境。
3. **项目管理**：通过 `uv init` 初始化项目结构，生成 `pyproject.toml` 和其他必要文件。
4. **工具管理**：通过 `uvx`（`uv tool run` 的别名）运行命令行工具，通过 `uv tool install` 安装工具到持久环境。
5. **Python 版本管理**：支持安装和切换多个 Python 版本，类似 `pyenv`。
6. **脚本运行**：通过 `uv run` 运行 Python 脚本，自动管理依赖和环境。
7. **构建和发布**：支持构建和发布 Python 包到 PyPI。

---

### **安装 UV**

以下是几种常见的安装 UV 的方法：

1. **使用官方安装脚本（推荐）**：
   - **macOS/Linux**：
     ```bash
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```
   - **Windows（PowerShell，需管理员权限）**：
     ```powershell
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```
   - 安装后，UV 的二进制文件通常位于 `~/.local/bin`，需确保该路径在系统的 `PATH` 环境变量中。

2. **通过 Homebrew（macOS/Linux）**：
   ```bash
   brew install uv
   ```

3. **通过 PyPI（不推荐，除非必要）**：
   ```bash
   pip install uv
   ```
   建议在虚拟环境中安装，以避免污染系统环境。

4. **验证安装**：
   ```bash
   uv --version
   ```
   输出示例：`uv 0.5.31 (e38ac4900 2025-02-12)`。

---

### **基本使用方法**

以下是 UV 的常用命令及其使用场景，结合实际示例说明：

#### **1. 初始化新项目**
UV 可以快速初始化一个结构化的 Python 项目，包含 `pyproject.toml`、`.gitignore`、`.python-version` 和示例脚本等。

```bash
uv init my-project
cd my-project
```

这将创建一个名为 `my-project` 的目录，结构如下：
```
my-project/
├── .git/
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
└── hello.py
```

- `pyproject.toml`：定义项目元数据和依赖。
- `.python-version`：指定项目使用的 Python 版本。
- `hello.py`：一个简单的示例脚本。

#### **2. 添加和安装依赖**
使用 `uv add` 添加依赖到项目并自动更新 `pyproject.toml` 和 `uv.lock` 文件。

```bash
uv add requests
```

- 这会在当前目录创建虚拟环境（`.venv`），安装 `requests` 及其依赖，并更新 `pyproject.toml`：
  ```toml
  [project]
  name = "my-project"
  version = "0.1.0"
  dependencies = [
      "requests>=2.32.3",
  ]
  ```
- `uv.lock` 文件记录了精确的依赖版本，确保跨环境一致性。

安装多个包：
```bash
uv add numpy pandas
```

指定版本：
```bash
uv add "Django>=4.0"
```

#### **3. 运行 Python 脚本**
使用 `uv run` 运行脚本，UV 会自动使用项目的虚拟环境，无需手动激活。

```bash
uv run hello.py
```

运行其他 Python 命令：
```bash
uv run python -c "import requests; print(requests.__version__)"
```

#### **4. 管理虚拟环境**
创建虚拟环境：
```bash
uv venv
```
默认在当前目录创建 `.venv` 文件夹。

指定 Python 版本：
```bash
uv venv --python 3.10
```

同步依赖（根据 `pyproject.toml` 和 `uv.lock` 安装）：
```bash
uv sync
```

#### **5. 运行命令行工具**
使用 `uvx`（`uv tool run` 的别名）运行工具，无需手动安装到环境中。

运行 `ruff` 检查代码：
```bash
uvx ruff check
```

指定版本：
```bash
uvx ruff@0.3.0 check
```

安装工具到持久环境：
```bash
uv tool install ruff
```
安装后，`ruff` 可直接在命令行运行：
```bash
ruff --version
```

#### **6. 管理 Python 版本**
安装特定 Python 版本：
```bash
uv python install 3.10
```

为项目指定 Python 版本：
```bash
uv python pin 3.10
```

查看已安装的 Python 版本：
```bash
uv python list
```

#### **7. 构建和发布包**
构建项目为 wheel 文件或源分发包：
```bash
uv build
```
输出文件位于 `dist/` 目录，如 `dist/my-project-0.1.0-py3-none-any.whl`。

发布到 PyPI：
```bash
uv publish
```
需要配置 PyPI 的 API 令牌。

#### **8. 升级 UV 或工具**
升级 UV 本身：
```bash
uv self update
```

升级已安装的工具：
```bash
uv tool upgrade ruff
```

升级所有工具：
```bash
uv tool upgrade --all
```

---

### **高级用法**

1. **依赖组管理**：
UV 支持将依赖分为不同组（如开发、测试、生产）。添加开发依赖：
```bash
uv add --dev pytest
```
这会更新 `pyproject.toml` 的 `[project.optional-dependencies]` 部分：
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
]
```

安装特定依赖组：
```bash
uv sync --dev
```

2. **从其他工具迁移**：
- **从 `pip` 和 `virtualenv`**：
  将 `requirements.txt` 转换为 `pyproject.toml`：
  ```bash
  uv pip compile requirements.in --output-file pyproject.toml
  ```
  然后使用 `uv sync` 安装依赖。

- **从 Poetry**：
  Poetry 的 `pyproject.toml` 格式与 UV 兼容，可直接使用：
  ```bash
  uv sync
  ```

3. **运行一次性工具**：
使用 `uvx` 从非 PyPI 源运行工具：
```bash
uvx --from git+https://github.com/httpie/cli@master httpie
```

4. **锁定依赖**：
显式生成 `uv.lock` 文件：
```bash
uv lock
```

---

### **UV 优势与注意事项**

#### **优势**
- **速度**：UV 的 Rust 实现和并行下载使其远超传统工具。
- **简化工作流**：一个工具取代多个，减少学习和维护成本。
- **可重现性**：`uv.lock` 确保跨环境一致。
- **灵活性**：支持 `pip` 兼容的 `requirements.txt` 和现代 `pyproject.toml`。

#### **注意事项**
- **学习曲线**：尽管 UV 命令简单，但从其他工具迁移可能需要适应。
- **生态系统依赖**：UV 由 Astral（一家初创公司）维护，未来可能受商业化影响。
- **非 Python 依赖**：UV 不支持非 Python 包（如 Conda 的系统级依赖）。

---

### **示例：创建一个简单的 CLI 应用**

以下是一个使用 UV 创建命令行应用的示例：

1. 初始化项目：
   ```bash
   uv init my-cli --package
   cd my-cli
   ```

2. 添加依赖（如 `click` 用于 CLI）：
   ```bash
   uv add click
   ```

3. 编辑 `src/my_cli/cli.py`：
   ```python
   import click

   @click.command()
   @click.argument("name")
   def greet(name):
       click.echo(f"Hello, {name}!")

   if __name__ == "__main__":
       greet()
   ```

4. 更新 `pyproject.toml`：
   ```toml
   [project]
   name = "my-cli"
   version = "0.1.0"
   dependencies = ["click>=8.0"]
   [project.scripts]
   my-cli = "my_cli.cli:greet"
   ```

5. 运行应用：
   ```bash
   uv run my-cli Alice
   ```
   输出：`Hello, Alice!`

6. 构建和发布：
   ```bash
   uv build
   uv publish
   ```

---

### **参考资源**

- **官方文档**：https://docs.astral.sh/uv/[](https://docs.astral.sh/uv/guides/tools/)
- **GitHub 仓库**：https://github.com/astral-sh/uv[](https://github.com/astral-sh/uv)
- **安装指南**：https://astral.sh/uv/install
- **命令行帮助**：运行 `uv --help` 查看详细命令说明。

---

### **总结**

UV 是一个功能强大、速度极快的 Python 包管理和项目管理工具，集成了虚拟环境管理、依赖管理、工具运行和 Python 版本管理等功能。通过简单的命令（如 `uv init`、`uv add`、`uv run`、`uvx`），开发者可以快速搭建和管理项目，显著提升开发效率。对于希望简化工作流、提高性能的 Python 开发者，UV 是 2025 年值得尝试的工具。

# 平时常用存根
他们来自：[LumaPictures/cg-stubs: Python stubs for VFX and Animation](https://github.com/LumaPictures/cg-stubs)
```bash
# 用于maya自动补全
uv add types-maya-strict

# 用于pyside2自动补全
uv add types-pyside2 

uv add Qt.py
uv add pymel

```