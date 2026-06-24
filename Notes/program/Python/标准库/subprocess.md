`subprocess` 是 Python 的标准库，用于创建和管理子进程，执行外部命令并与之交互。它取代了旧的模块如 `os.system` 和 `os.popen`，提供了更强大和灵活的功能。以下是对 `subprocess` 库的简要介绍：

### 主要功能
1. **运行外部命令**：可以在 Python 中调用系统命令（如 `ls`、`ping` 等）并获取输出。
2. **进程间通信**：支持与子进程的标准输入（stdin）、标准输出（stdout）和标准错误（stderr）交互。
3. **灵活的进程控制**：可以设置超时、环境变量、管道等，管理子进程的行为。

### 核心函数和类
1. **`subprocess.run()`**（Python 3.5+ 推荐）

   运行命令并**同步等待**其完成，返回一个 `CompletedProcess` 对象。这是最常用的 API。

   #### 参数详解


   | 参数 | 类型 | 默认值 | 说明 |
   |------|------|--------|------|
   | **args** | list \| str | 必须 | 命令及参数。建议用列表：`['ls', '-l']`，避免字符串拼接 |
   | **stdin** | int \| file | None | 子进程的输入源。常用：`subprocess.PIPE`（从 Python 传入），`subprocess.DEVNULL`（无输入） |
   | **stdout** | int \| file | None | 标准输出目标。常用：`subprocess.PIPE`（捕获），`subprocess.DEVNULL`（丢弃） |
   | **stderr** | int \| file | None | 标准错误目标。常用：`subprocess.PIPE`（捕获），`subprocess.STDOUT`（合并到 stdout） |
   | **shell** | bool | False | 是否通过 shell 运行（❌ 安全隐患，避免用户输入时使用） |
   | **cwd** | str \| Path | None | 子进程的工作目录（如 `git` 操作时需要） |
   | **env** | dict | None | 子进程的环境变量字典。若不设置，继承父进程环境 |
   | **timeout** | float | None | 超时时间（秒）。超时抛出 `TimeoutExpired` |
   | **check** | bool | False | 若为 `True`，非零退出码会抛出 `CalledProcessError` |
   | **capture_output** | bool | False | ✨ **便捷参数**：同时设置 `stdout=PIPE, stderr=PIPE`（Python 3.7+） |
   | **text** | bool | False | 若为 `True`，输出为字符串；否则为字节。`encoding` 可自定义编码 |
   | **encoding** | str | None | 输出编码（仅当 `text=True` 时有效）。常用 `'utf-8'` |


   #### 返回值：`CompletedProcess` 对象

   ```python
   class CompletedProcess:
       args: list | str          # 执行的命令
       returncode: int           # 退出码（0=成功，非0=失败）
       stdout: str | bytes | None  # 标准输出内容（若被捕获）
       stderr: str | bytes | None  # 标准错误内容（若被捕获）
   ```

   #### 示例1：基础用法

   ```python
   import subprocess
   
   def run_ls_command() -> str:
       """执行 ls 命令并返回输出"""
       result: subprocess.CompletedProcess[str] = subprocess.run(
           ['ls', '-l'],
           capture_output=True,  # 同时捕获 stdout 和 stderr
           text=True             # 返回字符串
       )
       return result.stdout
   ```

   #### 示例2：处理不同的退出码

   ```python
   def git_commit_with_check(message: str) -> bool:
       """
       提交代码，使用 check=True 自动异常处理
       
       Args:
           message: 提交信息
       
       Returns:
           是否提交成功
       """
       try:
           subprocess.run(
               ['git', 'commit', '-m', message],
               check=True,  # 非零退出码自动抛异常
               capture_output=True,
               text=True
           )
           return True
       except subprocess.CalledProcessError as e:
           print(f"❌ 提交失败（退出码 {e.returncode}）")
           print(f"输出: {e.stderr}")
           return False
   ```

   #### 示例3：工作目录与环境变量

   ```python
   import subprocess
   import os
   
   def run_in_directory(cmd: list[str], workdir: str) -> bool:
       """
       在指定目录运行命令（常用于 git、cmake 等）
       """
       result = subprocess.run(
           cmd,
           cwd=workdir,  # 设置工作目录
           capture_output=True,
           text=True,
           timeout=60
       )
       return result.returncode == 0
   
   def run_with_custom_env() -> None:
       """
       使用自定义环境变量运行命令
       """
       env = os.environ.copy()  # 复制当前环境
       env['MAYA_LOCATION'] = r'C:\Program Files\Autodesk\Maya2024'
       env['PYTHONPATH'] = '/path/to/libs'
       
       result = subprocess.run(
           ['python', 'my_script.py'],
           env=env,  # 传入自定义环境
           capture_output=True,
           text=True
       )
   ```

   #### 示例4：超时控制

   ```python
   import subprocess
   
   def run_with_timeout(cmd: list[str], timeout_seconds: int = 30) -> bool:
       """
       运行命令并设置超时
       """
       try:
           result = subprocess.run(
               cmd,
               capture_output=True,
               text=True,
               timeout=timeout_seconds  # 超时时间（秒）
           )
           print(f"✅ 命令完成，退出码: {result.returncode}")
           return result.returncode == 0
       except subprocess.TimeoutExpired:
           print(f"⏱️ 命令超时 (>{timeout_seconds}s)，子进程已被终止")
           return False
   ```

   #### 示例5：分离处理 stdout 和 stderr

   ```python
   import subprocess
   
   def diagnose_command(cmd: list[str]) -> None:
       """
       区分标准输出和错误输出（适合日志记录）
       """
       result = subprocess.run(
           cmd,
           stdout=subprocess.PIPE,  # 只捕获 stdout
           stderr=subprocess.PIPE,  # 只捕获 stderr
           text=True
       )
       
       if result.stdout:
           print(f"[OUTPUT] {result.stdout}")
       
       if result.stderr:
           print(f"[ERROR] {result.stderr}")
   ```

   #### 示例6：TA 工具场景 - 批量导出

   ```python
   import subprocess
   from pathlib import Path
   from typing import List
   
   MAYA_PATH = r"C:\Program Files\Autodesk\Maya2024\bin\maya.exe"
   
   def batch_fbx_export(
       maya_files: List[str],
       output_dir: str,
       timeout: int = 300
   ) -> dict[str, bool]:
       """
       批量导出 FBX，展示 subprocess.run() 的综合应用
       
       Args:
           maya_files: Maya 文件列表
           output_dir: 输出目录
           timeout: 每个文件的超时时间（秒）
       
       Returns:
           {文件名: 是否成功} 的字典
       """
       results = {}
       
       for maya_file in maya_files:
           try:
               output_fbx = Path(output_dir) / f"{Path(maya_file).stem}.fbx"
               
               result = subprocess.run(
                   [
                       MAYA_PATH,
                       '-batch',
                       '-command',
                       f'file -open "{maya_file}"; FBXExport -file "{output_fbx}"'
                   ],
                   capture_output=True,
                   text=True,
                   timeout=timeout,
                   check=False  # 不自动异常，手动处理
               )
               
               if result.returncode == 0:
                   print(f"✅ {Path(maya_file).name} → {output_fbx.name}")
                   results[maya_file] = True
               else:
                   print(f"❌ {Path(maya_file).name} 导出失败")
                   if result.stderr:
                       print(f"   错误: {result.stderr[:100]}...")
                   results[maya_file] = False
                   
           except subprocess.TimeoutExpired:
               print(f"⏱️ {Path(maya_file).name} 导出超时")
               results[maya_file] = False
           except Exception as e:
               print(f"⚠️ {Path(maya_file).name} 异常: {e}")
               results[maya_file] = False
       
       # 统计结果
       success_count = sum(1 for v in results.values() if v)
       print(f"\n总体: {success_count}/{len(maya_files)} 导出成功")
       
       return results
   ```

2. **`subprocess.Popen`**（更底层）
   - 用于更复杂的进程管理，允许异步执行和实时交互。
   - 提供对子进程的精细控制，如管道通信、等待进程结束等。
   - 示例：
     ```python
     import subprocess
     from typing import Tuple
     
     def run_echo_command() -> str:
         """执行 echo 命令并返回输出"""
         process: subprocess.Popen[str] = subprocess.Popen(
             ['echo', 'hello'],
             stdout=subprocess.PIPE,
             text=True
         )
         output, _ = process.communicate()
         return output.strip()
     ```

3. **其他辅助函数**（较老，不推荐广泛使用）
   - `subprocess.call()`：运行命令并返回退出码。
   - `subprocess.check_call()`：类似 `call`，但非零退出码抛出异常。
   - `subprocess.check_output()`：运行命令并返回输出，非零退出码抛出异常。

---

## 核心概念：标准流与 `subprocess.PIPE`

### 标准流（Standard Streams）

在 Unix 哲学中，每个进程有**三个标准流**：

| 流名 | 文件描述符 | 作用 | 来源/去向 |
|------|-----------|------|----------|
| **stdin** | 0 | 进程**接收**的输入 | 键盘、管道、文件 |
| **stdout** | 1 | 进程**正常**输出 | `print()` 结果、命令成功输出 |
| **stderr** | 2 | 进程**错误**输出 | 异常信息、警告、诊断日志 |

**为什么分开？** 允许用户在终端中分别重定向：
```bash
# 只捕获错误，正常输出显示
command 2>/dev/null

# 分别保存到不同文件
command > output.log 2> error.log
```

### `subprocess.PIPE` 是什么

`subprocess.PIPE` 是一个**特殊常量**（值为 `-1`），用来告诉 subprocess **捕获该流到变量**，而不是让其直接打到终端。

```python
import subprocess

# PIPE 的三种用法：
result = subprocess.run(
    ['ls', '-l'],
    stdout=subprocess.PIPE,  # 捕获标准输出
    stderr=subprocess.PIPE,  # 捕获错误输出
    text=True                 # 返回字符串（而不是字节）
)

# 现在可以访问：
print(result.stdout)  # 正常输出内容
print(result.stderr)  # 错误输出内容
```

### 标准流处理的三种模式

```python
import subprocess

# 🔴 模式1：不捕获（默认）
print("【模式1】输出直接打到终端")
subprocess.run(['echo', 'Hello'])  # 输出显示在控制台，Python 无法访问
# 输出: Hello

# 🟡 模式2：分别捕获
print("\n【模式2】分别捕获 stdout 和 stderr")
result = subprocess.run(
    ['ls', '/nonexistent'],  # 会报错
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
print(f"正常输出: {result.stdout or '（空）'}")
print(f"错误输出: {result.stderr or '（空）'}")

# 🟢 模式3：便捷捕获（Python 3.7+）
print("\n【模式3】同时捕获两个流")
result = subprocess.run(
    ['ping', 'localhost'],
    capture_output=True,  # ✨ 等价于 stdout=PIPE, stderr=PIPE
    text=True
)
# stdout 和 stderr 都被捕获
```

### 实战例子：TA 工具中的应用价值

```python
import subprocess
from pathlib import Path

def export_with_detailed_logging(maya_file: str) -> bool:
    """
    导出 FBX 时分离日志：
    - stdout：导出进度
    - stderr：顶点溢出、权重警告等
    """
    result = subprocess.run(
        ['maya', '-batch', '-command', f'file -open {maya_file}; FBXExport...'],
        stdout=subprocess.PIPE,  # 捕获正常信息
        stderr=subprocess.PIPE,  # 捕获警告和错误
        text=True,
        timeout=300
    )
    
    # 分别写日志
    if result.stdout:
        print(f"[INFO] {result.stdout}")  # 进度信息
    
    if result.stderr:
        print(f"[WARNING] {result.stderr}")  # 警告信息
        # 可根据错误类型做决策
        if "weight overflow" in result.stderr:
            print("需要调整骨骼权重！")
    
    return result.returncode == 0
```

### 流处理决策流程图

```
┌─────────────────────────────────────┐
│ 需要获取命令的输出吗？              │
└────┬────────────────────────────────┘
     │
     ├─ 不需要 → stdout=None（默认）
     │          输出直接显示在终端
     │
     └─ 需要 → 分别捕获还是合并？
              │
              ├─ 分别捕获 → stdout=PIPE
              │             stderr=PIPE
              │             （区分正常/错误信息）
              │
              └─ 合并捕获 → capture_output=True
                           （便捷写法）
```

---

### 常用参数
- `capture_output=True`：捕获 stdout 和 stderr（等价于 `stdout=PIPE, stderr=PIPE`）。
- `text=True`：以字符串形式返回输出（而不是字节）。
- `shell=True`：在 shell 中运行命令（小心安全风险，建议避免）。
- `timeout`：设置命令执行的最长时间，超时抛出 `TimeoutExpired`。
- `env`：自定义子进程的环境变量。

### 使用注意事项
1. **安全性**：避免 `shell=True` 拼接用户输入，可能导致命令注入漏洞。推荐使用参数列表形式。
   ```python
   # ✅ 安全：使用参数列表
   def safe_ls(user_input: str) -> subprocess.CompletedProcess[str]:
       return subprocess.run(['ls', user_input], capture_output=True, text=True)
   
   # ❌ 不安全：字符串拼接 + shell=True
   # subprocess.run(f'ls {user_input}', shell=True)
   ```

2. **异常处理**：
   - `CalledProcessError`：命令执行失败（非零退出码）。
   - `TimeoutExpired`：命令超时。
   - 示例：
     ```python
     def safe_run_command(cmd: list[str]) -> bool:
         """安全执行命令，返回是否成功"""
         try:
             subprocess.run(cmd, check=True, timeout=30)
             return True
         except subprocess.CalledProcessError as e:
             print(f"命令失败 (退出码 {e.returncode}): {e.stderr}")
             return False
         except subprocess.TimeoutExpired:
             print(f"命令超时 (>30s)")
             return False
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

def ping_host(host: str, timeout: int = 10) -> bool:
    """
    ping 指定主机，返回是否可达
    
    Args:
        host: 要 ping 的主机地址
        timeout: 超时时间（秒）
    
    Returns:
        True 表示可达，False 表示不可达或超时
    """
    try:
        result: subprocess.CompletedProcess[str] = subprocess.run(
            ['ping', '-c', '4', host],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0:
            print(f"✅ {host} 可达")
            return True
        else:
            print(f"❌ {host} 不可达")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏱️ {host} 超时")
        return False
    except Exception as e:
        print(f"⚠️ 错误: {e}")
        return False
```

### 总结
`subprocess` 是一个功能强大且灵活的库，适合需要与外部命令交互的场景。推荐优先使用 `subprocess.run` 处理简单任务，复杂场景使用 `Popen`。注意安全性、异常处理和资源管理，确保代码健壮。

# 实践案例

## 1. 启动 Maya（同步/异步）

```python
import subprocess
from pathlib import Path

MAYA_PATH: str = r"C:\Program Files\Autodesk\Maya2024\bin\maya.exe"

def start_maya_sync() -> int:
    """同步启动 Maya，阻塞直到用户关闭应用"""
    return subprocess.run([MAYA_PATH]).returncode

def start_maya_async() -> subprocess.Popen[str]:
    """异步启动 Maya，脚本立即继续执行"""
    return subprocess.Popen([MAYA_PATH])

def start_maya_with_script(script_path: str) -> int:
    """启动 Maya 并执行指定脚本"""
    return subprocess.run(
        [MAYA_PATH, "-command", f"python(\"{script_path}\")"]
    ).returncode
```

**选型指南**：
- **`run()`** 同步执行，适合工具链集成（等待 Maya 完成某项操作）
- **`Popen()`** 异步执行，适合启动长期运行的应用（如批处理工具）

---

## 2. 批量处理资产（TA 工具典型场景）

```python
import subprocess
from typing import List

def batch_export_fbx(maya_file_list: List[str], output_dir: str) -> None:
    """
    批量导出 FBX，单个文件失败不中断流程
    
    Args:
        maya_file_list: Maya 文件路径列表
        output_dir: 输出目录
    """
    for maya_file in maya_file_list:
        try:
            result = subprocess.run(
                [
                    MAYA_PATH,
                    "-batch",
                    "-command",
                    f"file -open {maya_file}; FBXExport -file {output_dir}/output.fbx"
                ],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode != 0:
                print(f"❌ 导出失败: {maya_file}")
                print(f"   错误: {result.stderr}")
            else:
                print(f"✅ 导出成功: {maya_file}")
        except subprocess.TimeoutExpired:
            print(f"⏱️ 超时: {maya_file}")
        except Exception as e:
            print(f"⚠️ 异常: {maya_file} - {e}")
```

---

## 3. 捕获 Git 操作结果（自动化脚本）

```python
def get_git_status(repo_path: str) -> str:
    """获取 git 工作区状态"""
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    return result.stdout

def commit_changes(repo_path: str, message: str) -> bool:
    """提交变更，返回是否成功"""
    try:
        subprocess.run(
            ["git", "add", "."],
            cwd=repo_path,
            check=True
        )
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=repo_path,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git 操作失败: {e}")
        return False
```