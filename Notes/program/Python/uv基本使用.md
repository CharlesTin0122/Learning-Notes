# 概述
- 一个速度极快的 Python 包和项目管理器，用 Rust 编写。
# 安装
```powershell
# 三种安装方法
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
pip install uv
scoop install main/uv
# 更新
uv self update
```
# 项目
- `uv init`: 创建一个新的 Python 项目.
- `uv add`: 向项目添加一个依赖.
- `uv remove`: 从项目中移除一个依赖.
- `uv sync`: 同步项目的依赖与环境.
- `uv lock`: 为项目的依赖创建一个锁定文件.
- `uv run`: 在项目环境中运行一个命令.
- `uv tree`: 查看项目的依赖树.
- `uv build`: 将项目构建为分发档案.
- `uv publish`: 将项目发布到软件包索引.
```powershell
# 构建项目
mkdir hello-world
cd hello-world
uv init
uv venv
uv run main.py

# 添加Ruff并执行检查
uv add ruff
uv run ruff check

# 创建锁定文件.
uv lock

# 同步项目的依赖与环境
uv sync
```
# 工具
 - `uv tool run`: 在临时环境中运行工具。
- `uvx` : 是 uv tool run 的便捷别名，用于快速运行 Python 包提供的命令行工具，而无需在当前项目的虚拟环境中永久安装这些工具。
- `uv tool install`: 用户范围内安装工具。
- `uv tool uninstall`: 卸载工具。
- `uv tool list`: 列出已安装的工具。
- `uv tool update-shell`: 更新 shell 以包含工具可执行文件。
```powershell
# py牛牛说话
uvx pycowsay 'hello world!'

# 安装ruff
uv tool install ruff
ruff --version
uv tool upgrade ruff
# 运行Ruff 无需安装
uvx ruff
# 使用python版本创建虚拟环境
uv venv --python 3.12.0

# 使用特定版本python
uv python pin 3.11
# mypy
uv tool install mypy
uv tool run mypy controll_creator.py
# 检查整个父目录
uv tool run mypy .
uvx mypy .

uv tool run ruff check .
uvx ruff check .
```
# 管理python
- `uv python install`: 安装Python版本。
- `uv python list`: 查看可用的Python版本。
- `uv python find`: 查找已安装的Python版本。
- `uv python pin`: 将当前项目固定为使用特定的Python版本。
- `uv python uninstall`: 卸载Python版本。
```
# 安装Python版本
uv python install 3.10 3.11 3.12
# 构建虚拟环境
uv venv
# 重新安装python
uv python install --reinstall
# 查看可用的Python版本
uv python list
# 执行
uv run example.py
```
# 运行脚本
- `uv run`: 运行脚本。
- `uv add --script`: 向脚本添加依赖项
- `uv remove --script`: 从脚本中删除依赖项
# pip接口
- `uv pip install`: 将软件包安装到当前环境。
- `uv pip show`: 显示已安装软件包的详细信息。
- `uv pip freeze`: 列出已安装的软件包及其版本。
- `uv pip check`: 检查当前环境是否具有兼容的软件包。
- `uv pip list`: 列出已安装的软件包。
- `uv pip uninstall`: 卸载软件包。
- `uv pip tree`: 查看环境的依赖树。
- `uv pip compile`: 将需求编译成锁定文件。
- `uv pip sync`: 使用锁定文件同步环境。
# 管理
- `uv cache clean`: 移除缓存条目。
- `uv cache prune`: 移除过时的缓存条目。
- `uv cache dir`: 显示 uv 缓存目录路径。
- `uv tool dir`: 显示 uv 工具目录路径。
- `uv python dir`: 显示 uv 安装的 Python 版本路径。
- `uv self update`: 将 uv 更新到最新版本。