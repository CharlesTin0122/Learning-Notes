### Python中的`glob`库简介

`glob` 是 Python 的标准库模块，用于查找符合特定模式的文件路径名。它基于 Unix 风格的通配符（wildcard）模式，简单易用，适合快速处理文件和目录的匹配操作。`glob` 模块主要用于文件系统路径的模式匹配，类似于在命令行中使用 `ls *.txt` 或 `dir *.txt` 的功能。

### 主要功能
- **文件路径匹配**：根据指定的模式查找文件或目录。
- **通配符支持**：支持 `*`（匹配任意字符）、`?`（匹配单个字符）、`[seq]`（匹配指定字符集）等。
- **递归查找**：支持递归遍历目录以查找匹配的文件。

### 常用方法
`glob` 模块提供了以下主要函数：
1. **`glob.glob(pattern, recursive=False)`**：
   - 根据指定的模式返回匹配的文件路径列表。
   - `pattern`：文件路径模式（如 `*.txt`）。
   - `recursive`：若为 `True`，启用递归查找（常与 `**` 配合使用）。
   - 返回：匹配的路径列表（字符串形式）。

2. **`glob.iglob(pattern, recursive=False)`**：
   - 与 `glob.glob` 类似，但返回一个迭代器，适合处理大量文件以节省内存。
   - 返回：匹配路径的迭代器。

3. **`glob.escape(pathname)`**：
   - 用于转义路径名中的特殊字符（如 `*`、`?`、`[]`），避免它们被当作通配符处理。
   - 示例：`glob.escape("file[1].txt")` 返回 `file\[1\].txt`。

### 通配符说明
- `*`：匹配任意长度的字符（不包括路径分隔符 `/` 或 `\`）。
- `**`：当 `recursive=True` 时，匹配任意深度的目录（需写为 `**/`）。
- `?`：匹配任意单个字符。
- `[seq]`：匹配指定字符集中的任意一个字符（如 `[abc]` 匹配 `a`、`b` 或 `c`）。
- `[!seq]`：匹配不在指定字符集中的任意一个字符（如 `[!abc]` 不匹配 `a`、`b`、`c`）。

### 用法示例

#### 1. 查找当前目录下所有 `.txt` 文件
```python
import glob

# 查找所有 .txt 文件
txt_files = glob.glob("*.txt")
print(txt_files)  # 输出类似：['file1.txt', 'file2.txt']
```

#### 2. 查找特定目录下的 `.py` 文件
```python
# 查找指定目录下的 Python 文件
py_files = glob.glob("./scripts/*.py")
print(py_files)  # 输出类似：['scripts/main.py', 'scripts/test.py']
```

#### 3. 递归查找所有 `.jpg` 文件
```python
# 递归查找当前目录及其子目录下的所有 .jpg 文件
jpg_files = glob.glob("**/*.jpg", recursive=True)
print(jpg_files)  # 输出类似：['images/photo1.jpg', 'images/subfolder/photo2.jpg']
```

#### 4. 使用 `iglob` 迭代器处理大量文件
```python
# 使用迭代器逐个处理文件
for file in glob.iglob("**/*.txt", recursive=True):
    print(file)  # 逐行输出匹配的 .txt 文件路径
```

#### 5. 转义特殊字符
```python
# 处理包含特殊字符的文件名
pattern = glob.escape("file[1].txt")
files = glob.glob(pattern)
print(files)  # 输出类似：['file[1].txt']
```

#### 6. 查找特定模式的数字文件名
```python
# 查找文件名以数字开头，扩展名为 .txt 的文件
num_files = glob.glob("[0-9]*.txt")
print(num_files)  # 输出类似：['123.txt', '456.txt']
```

### 注意事项
1. **路径分隔符**：
   - `glob` 自动适配系统路径分隔符（Windows 用 `\`，Linux/Mac 用 `/`）。
   - 建议使用 `os.path.join` 或 `pathlib` 构建跨平台路径。

2. **性能**：
   - 对于大量文件，使用 `glob.iglob` 更节省内存。
   - 递归查找（`recursive=True`）可能较慢，需根据需求优化模式。

3. **相对路径与绝对路径**：
   - 默认使用相对路径，可通过 `os.path.abspath` 转换为绝对路径。
   - 示例：
     ```python
     import os
     files = [os.path.abspath(f) for f in glob.glob("*.txt")]
     print(files)
     ```

4. **与 `pathlib` 的对比**：
   - Python 3.5+ 的 `pathlib` 模块也支持类似的模式匹配（`Path.glob`），且更现代化。
   - `glob` 更轻量，适合简单任务；`pathlib` 适合需要路径操作的复杂场景。

### 实际应用场景
- **批量文件处理**：如批量读取、移动或删除特定类型的文件。
- **数据分析**：查找数据集中的所有 `.csv` 或 `.json` 文件。
- **自动化脚本**：扫描目录以查找符合条件的日志文件或配置文件。
- **测试框架**：自动发现测试用例文件（如 `test_*.py`）。

### 总结
`glob` 是一个简单而强大的工具，适合快速查找和处理文件路径。通过灵活的通配符模式和递归查找功能，它能高效应对各种文件操作需求。对于更复杂的路径操作，建议结合 `os` 或 `pathlib` 使用。

如果你有具体的使用场景或需要更详细的示例，请告诉我！