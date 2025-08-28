`subprocess` 是 Python 的标准库，用于创建和管理子进程，执行外部命令并与之交互。它取代了旧的模块如 `os.system` 和 `os.popen`，提供了更强大和灵活的功能。以下是对 `subprocess` 库的简要介绍：

### 主要功能
1. **运行外部命令**：可以在 Python 中调用系统命令（如 `ls`、`ping` 等）并获取输出。
2. **进程间通信**：支持与子进程的标准输入（stdin）、标准输出（stdout）和标准错误（stderr）交互。
3. **灵活的进程控制**：可以设置超时、环境变量、管道等，管理子进程的行为。

### 核心函数和类
1. **`subprocess.run()`**（Python 3.5+ 推荐）
   - 运行命令并等待其完成，返回一个 `CompletedProcess` 对象。
   - 参数：
     - `args`：命令及其参数（列表或字符串）。
     - `shell`：是否在 shell 中运行（默认 `False`，建议用列表格式避免 shell 注入）。
     - `stdout`/`stderr`：指定输出捕获方式（如 `subprocess.PIPE`）。
     - `timeout`：设置超时时间（秒）。
     - `check`：若为 `True`，命令返回非零退出码会抛出 `CalledProcessError`。
   - 示例：
     ```python
     import subprocess
     result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
     print(result.stdout)  # 输出命令结果
     ```

2. **`subprocess.Popen`**（更底层）
   - 用于更复杂的进程管理，允许异步执行和实时交互。
   - 提供对子进程的精细控制，如管道通信、等待进程结束等。
   - 示例：
     ```python
     process = subprocess.Popen(['echo', 'hello'], stdout=subprocess.PIPE, text=True)
     output, _ = process.communicate()
     print(output)  # 输出：hello
     ```

3. **其他辅助函数**（较老，不推荐广泛使用）
   - `subprocess.call()`：运行命令并返回退出码。
   - `subprocess.check_call()`：类似 `call`，但非零退出码抛出异常。
   - `subprocess.check_output()`：运行命令并返回输出，非零退出码抛出异常。

### 常用参数
- `capture_output=True`：捕获 stdout 和 stderr（等价于 `stdout=PIPE, stderr=PIPE`）。
- `text=True`：以字符串形式返回输出（而不是字节）。
- `shell=True`：在 shell 中运行命令（小心安全风险，建议避免）。
- `timeout`：设置命令执行的最长时间，超时抛出 `TimeoutExpired`。
- `env`：自定义子进程的环境变量。

### 使用注意事项
1. **安全性**：避免 `shell=True` 拼接用户输入，可能导致命令注入漏洞。推荐使用参数列表形式。
   ```python
   # 安全
   subprocess.run(['ls', user_input])
   # 不安全
   subprocess.run(f'ls {user_input}', shell=True)
   ```
2. **异常处理**：
   - `CalledProcessError`：命令执行失败（非零退出码）。
   - `TimeoutExpired`：命令超时。
   - 示例：
     ```python
     try:
         subprocess.run(['ls', '/invalid'], check=True)
     except subprocess.CalledProcessError as e:
         print(f"命令失败：{e}")
     ```
3. **编码问题**：设置 `text=True` 或 `encoding='utf-8'` 处理非 ASCII 输出。
4. **资源管理**：使用 `subprocess.run` 或 `with` 语句确保子进程正确关闭，防止资源泄漏。

### 典型应用场景
- 执行系统命令（如 `git commit`、`docker run`）。
- 获取命令行工具的输出（如 `grep`、`awk`）。
- 自动化脚本中调用外部程序并处理结果。
- 与需要实时输入输出的进程交互（如模拟终端输入）。

### 示例：捕获命令输出并处理
```python
import subprocess

try:
    result = subprocess.run(
        ['ping', '-c', '4', '8.8.8.8'],
        capture_output=True,
        text=True,
        timeout=10
    )
    print("输出：", result.stdout)
    print("退出码：", result.returncode)
except subprocess.TimeoutExpired:
    print("命令超时")
except subprocess.CalledProcessError as e:
    print(f"命令失败：{e.stderr}")
```

### 总结
`subprocess` 是一个功能强大且灵活的库，适合需要与外部命令交互的场景。推荐优先使用 `subprocess.run` 处理简单任务，复杂场景使用 `Popen`。注意安全性、异常处理和资源管理，确保代码健壮。

# 案例
- 启动maya软件
```python
import os
import subprocess

MAYA_PATH = r"C:\Program Files\Autodesk\Maya2024\bin\maya.exe"
maya_args = [MAYA_PATH]
# 运行命令并等待其完成，返回一个 CompletedProcess 对象。
subprocess.call(maya_args)
subprocess.run(maya_args)
subprocess.Popen(maya_args)
```
- 最后三行只能选择其一
### 代码中的具体行为

假设 MAYA_PATH 指向正确的 maya.exe：

1. **第一行：subprocess.call(maya_args)**
    - 启动 Maya，脚本等待用户关闭 Maya 后返回退出码（例如 0）。
    - 同步执行：调用 call 后，脚本会阻塞，直到 maya.exe 进程结束（即 Maya 应用程序关闭）。
    - 继续执行下一行。
2. **第二行：subprocess.run(maya_args)**
    - 启动 Maya，脚本等待用户关闭 Maya，返回 CompletedProcess 对象，包含退出码、stdout 和 stderr（如果捕获）。
    - 同步执行：与 call 类似，脚本会阻塞，直到 maya.exe 进程结束。
    - 继续执行下一行。
3. **第三行：subprocess.Popen(maya_args)**
    - 启动 Maya，但脚本不等待，直接结束（Maya 进程在后台运行）。返回一个 Popen 对象，允许更灵活的进程管理。
    - 异步执行：与 call 和 run 不同，Popen 不等待进程结束，脚本会立即继续执行后续代码。
    - 实时交互：可以通过 Popen 对象的 communicate() 方法或 stdout/stderr 管道与子进程交互。
    - Maya 窗口保持打开，直到用户手动关闭。