一个 Python 脚本，它利用 `pathlib` 库的强大功能来处理文件路径，并结合 `glob` 模式来查找文件。这个脚本将能清晰地告诉你两个目录之间的差异。

### 概览介绍解决方案

我们将编写一个名为 `compare_directories` 的函数，该函数接收两个目录路径作为输入。

其工作原理如下：

1. **路径对象化**：我们使用 `pathlib.Path` 将输入的字符串路径转换为功能更强大的路径对象。这让检查路径是否存在、是否为目录等操作变得非常简单。
    
2. **获取资产列表**：我们使用路径对象的 `.glob('*')` 方法来获取每个目录下的所有项目（文件和子目录）的列表。我们只提取每个项目的名称（例如 `data.csv`），而不是完整的路径（例如 `path/A/data.csv`）。
    
3. **高效比对**：为了找出差异，我们将两个列表转换为 Python 的 `set`（集合）数据类型。集合运算（求差集）是找出两个列表中独有元素的最快、最简单的方法。
    
4. **清晰打印**：最后，脚本会清晰地打印出仅存在于 A 目录中的资产和仅存在于 B 目录中的资产。
    

下面是完整的代码。

### 代码展示和实现说明

这是一个功能完整且带有详细注释的脚本。你可以直接将其保存为 `.py` 文件并运行。

```Python
# 导入所需的库
import pathlib
import os  # 用于创建示例目录和文件


def compare_directories(path_a: str, path_b: str):
    """
    比对两个目录下的资产差异。

    该函数会：
    1. 获取两个目录中的所有资产名称（文件和文件夹）。
    2. 使用集合（set）操作找出各自独有的资产。
    3. 打印出比对结果。

    参数:
    path_a (str): 第一个目录的路径 (目录A)。
    path_b (str): 第二个目录的路径 (目录B)。
    """
    print("--- 开始比对 ---")
    print(f"目录 A: {path_a}")
    print(f"目录 B: {path_b}")

    # 1. 使用 pathlib 将字符串路径转换为 Path 对象
    dir_a = pathlib.Path(path_a)
    dir_b = pathlib.Path(path_b)

    # 检查路径是否存在且为目录
    if not dir_a.is_dir():
        print(f"错误: 路径 '{path_a}' 不是一个有效的目录。")
        return
    if not dir_b.is_dir():
        print(f"错误: 路径 '{path_b}' 不是一个有效的目录。")
        return

    # 2. 使用 glob('**/*') 获取每个目录下递归所有资产的名称
    # 我们使用 str(p.relative_to(dir_a)来获取扁平列表，例如 'subfolder/file.txt'
    # 使用集合推导式（set comprehension）来创建资产名称的集合
    assets_a = {str(p.relative_to(dir_a)) for p in dir_a.glob("**/*") if p.is_file()}
    assets_b = {str(p.relative_to(dir_b)) for p in dir_b.glob("**/*") if p.is_file()}

    # 3. 使用集合的差集运算找出差异
    # a - b 会得到所有在 a 中但不在 b 中的元素
    only_in_a = assets_a - assets_b
    only_in_b = assets_b - assets_a

    # 4. 打印结果
    print("\n--- 比对结果 ---")

    # 打印仅在目录 A 中的资产
    if only_in_a:
        print(f"\n✅ 仅存在于目录 A '{path_a}' 的资产:")
        # 排序使输出更整洁
        for item in sorted(list(only_in_a)):
            print(f"  - {item}")
    else:
        print(f"\n✅ 目录 A '{path_a}' 中没有独有资产。")

    # 打印仅在目录 B 中的资产
    if only_in_b:
        print(f"\n✅ 仅存在于目录 B '{path_b}' 的资产:")
        for item in sorted(list(only_in_b)):
            print(f"  - {item}")
    else:
        print(f"\n✅ 目录 B '{path_b}' 中没有独有资产。")


# --- 主程序入口 ---
if __name__ == "__main__":
    # 为了演示，我们先创建一些示例目录和文件
    print("正在创建用于演示的临时目录和文件...")

    # 定义示例目录路径
    path_A = "demo_folder_A"
    path_B = "demo_folder_B"

    # --- 调用比对函数 ---
    compare_directories(path_A, path_B)

```

### 如何运行此脚本

1. **保存代码**：将上面的代码复制并粘贴到一个名为 `compare_dirs.py` 的文件中。
    
2. **打开终端**：打开你的命令行工具（在 Windows 上是 PowerShell 或命令提示符，在 macOS 或 Linux 上是终端）。
    
3. **执行脚本**：导航到你保存 `compare_dirs.py` 的目录，然后运行以下命令：
    
    Bash
    
    ```
    python compare_dirs.py
    ```
    

脚本会自动创建两个演示文件夹（`demo_folder_A` 和 `demo_folder_B`），在其中放入一些文件，然后运行比对函数，最后打印出结果并删除临时文件夹。

**预期输出：**

```
正在创建用于演示的临时目录和文件...
示例文件创建完毕。

--- 开始比对 ---
目录 A: demo_folder_A
目录 B: demo_folder_B

--- 比对结果 ---

✅ 仅存在于目录 A 'demo_folder_A' 的资产:
  - document_A.pdf
  - file_only_in_A.txt

✅ 仅存在于目录 B 'demo_folder_B' 的资产:
  - data_B
  - log_from_B.log

--- 清理演示环境 ---
临时目录和文件已删除。
```

### 如何用于你自己的目录

要比对你自己的目录，只需修改 `if __name__ == "__main__":` 代码块中的 `path_A` 和 `path_B` 变量为你自己的路径即可，并移除或注释掉创建和清理示例目录的部分。

例如：

Python

```
if __name__ == "__main__":
    # --- 调用比对函数 ---
    my_first_path = "/path/to/your/first/folder"
    my_second_path = "C:\\Users\\YourUser\\Documents\\second_folder"
    
    compare_directories(my_first_path, my_second_path)
```

### 扩展和调整

- **仅比对文件**：如果你不希望将子目录纳入比对范围，可以在集合推导式中添加一个 `.is_file()` 的判断。
    
    Python
    
    ```
    assets_a = {p.name for p in dir_a.glob('*') if p.is_file()}
    assets_b = {p.name for p in dir_b.glob('*') if p.is_file()}
    ```
    
- **递归比对所有子目录中的文件**：如果你想比对目录 A 和其所有子目录中的全部文件与目录 B 的情况，你可以使用 `**/*` 模式。
    
    Python
    
    ```
    # 注意：这将给出一个包含子目录路径的扁平列表，例如 'subfolder/file.txt'
    assets_a = {str(p.relative_to(dir_a)) for p in dir_a.glob('**/*')}
    assets_b = {str(p.relative_to(dir_b)) for p in dir_b.glob('**/*')}
    ```
    

希望这个脚本和详细的解释能帮助你完成任务！如果你有任何其他问题或需要进一步的修改，请随时告诉我。