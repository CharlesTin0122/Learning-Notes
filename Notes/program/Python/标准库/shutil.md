老田，作为动画TA，你在写自动化打包、资产提交（Publish）或者清理缓存缓存工具时，绝对离不开 `shutil`。

如果说 `pathlib` 是一把精致的手术刀，用来精准地获取和操作路径；那么 **`shutil` (Shell Utilities)** 就是一把瑞士军刀，专门用来执行**高级的文件和文件夹级操作**（比如拷贝、移动、打包压缩、强制删除目录树）。

从 Python 3.6 开始，`shutil` 完美兼容了 `pathlib` 对象，两者简直是管线开发中的“黄金搭档”。

以下是 `shutil` 在日常TA工作中最常用的几个核心功能及使用方法：
### 0. 常用函数及使用方法

#### **文件操作**

|函数|功能|示例|
|---|---|---|
|shutil.copy(src, dst)|复制文件（保留权限）|shutil.copy('src.txt', 'dst.txt')|
|shutil.copy2(src, dst)|复制文件（保留元数据，如修改时间）|shutil.copy2('src.txt', 'dst/')|
|shutil.copyfile(src, dst)|只复制文件内容（不复制权限和元数据）|shutil.copyfile('a.txt', 'b.txt')|
|shutil.move(src, dst)|移动文件/目录（可用于重命名）|shutil.move('old.txt', 'new.txt')|

**注意**：dst 可以是目录路径（会自动使用原文件名）或完整目标文件名。

#### **目录操作**

|函数|功能|示例|
|---|---|---|
|shutil.copytree(src, dst)|递归复制整个目录树|shutil.copytree('src_dir', 'dst_dir')|
|shutil.rmtree(path)|递归删除目录树（慎用！）|shutil.rmtree('temp_dir')|
|shutil.make_archive(base_name, format, root_dir)|创建压缩包（zip/tar 等）|shutil.make_archive('backup', 'zip', 'myfolder')|
|shutil.unpack_archive(filename, extract_dir)|解压压缩包|shutil.unpack_archive('backup.zip', 'extract_here')|

#### **其他实用函数**

- shutil.disk_usage(path)：获取磁盘使用情况（total, used, free）
- shutil.which(cmd)：类似 which 命令，查找可执行文件路径
- shutil.chown(path, user=None, group=None)：修改文件所有者
- shutil.copystat(src, dst)：仅复制权限和元数据
- shutil.ignore_patterns(*patterns)：配合 copytree 使用，忽略某些文件
### 1. 拷贝文件：`copy` vs `copy2`

拷贝文件是最常用的功能。`shutil` 提供了多个拷贝函数，但最常用的是 `copy2`。

- **`shutil.copy(src, dst)`**：拷贝文件数据和权限，但**不保留**创建时间、修改时间等元数据。
- **`shutil.copy2(src, dst)`**：连同元数据（时间戳等）一起拷贝。

**TA实战建议**：在同步 Maya/UE 资产（如 `.ma`, `.fbx`）时，**强烈建议永远使用 `copy2`**。因为很多游戏引擎（包括 UE）和版本控制系统（如 Perforce/Git）会依赖文件的修改时间来判断资产是否更新，如果丢失时间戳可能会导致引擎不断提示重新导入。

```python
import shutil
from pathlib import Path

src = Path("C:/Temp/export_anim_run.fbx")
dst_dir = Path("D:/UE_Project/Content/Animations")

# # 创建路径,自动补全缺失的父级目录,文件夹已存在时不要报错
dst_dir.mkdir(parents=True, exist_ok=True)

# 推荐：保留修改时间的拷贝
shutil.copy2(src, dst_dir) 
# 注意：如果 dst_dir 是一个文件夹路径，shutil 会自动把文件放进去，保持原文件名
```

### 2. 拷贝整个目录树：`copytree`

当你需要备份整个角色工程目录，或者给新角色创建一个基于模板的文件夹层级时，`copytree` 非常好用。它会递归地拷贝整个文件夹。

```python
import shutil
from pathlib import Path

template_dir = Path("D:/Pipeline/Templates/Character_Rig_Base")
new_char_dir = Path("D:/Project/Characters/Orc_Warrior")

# 将模板目录完整地复制一份作为新角色的目录
# dirs_exist_ok=True (Python 3.8+)：如果目标文件夹已存在，不会报错，而是覆盖/合并同名文件
shutil.copytree(
	template_dir, 
	new_char_dir, 
	dirs_exist_ok=True,
	ignore=shutil.ignore_patterns('*.pyc', '__pycache__', '.git','*.bak', '.mayaSwatches')
)

# 你还可以配合 ignore 参数，在拷贝时过滤掉不想拷的文件（比如历史备份文件）
# shutil.copytree(src, dst, ignore=shutil.ignore_patterns('*.bak', '.mayaSwatches'))
```

### 3. 移动文件或文件夹：`move`

类似命令行里的 `mv` 命令，通常用于资产处理完后，将其从临时目录（Temp）移动到发布目录（Publish）。

```python
import shutil
from pathlib import Path

# 假设你在后台用 MotionBuilder 跑完了一个重定向脚本，生成了文件
temp_file = Path("C:/Temp/processed_mocap.fbx")
publish_dir = Path("Z:/Server/Mocap_Library/Done")

# 将文件移动到服务器（跨磁盘移动也没问题，shutil在底层会先copy再delete）
shutil.move(temp_file, publish_dir)
```

### 4. 强制删除非空文件夹：`rmtree`

这是个极度危险但也极度常用的函数。`pathlib.Path.rmdir()` 只能删除**空文件夹**。如果文件夹里有贴图、FBX或者子文件夹，想直接把这个包含内容的总文件夹干掉，必须用 `rmtree`。

**TA实战建议**：常用于每次导出资产前，强制清空缓存（Cache）目录。

```python
import shutil
from pathlib import Path

cache_dir = Path("C:/Temp/Rig_Export_Cache")

if cache_dir.exists():
    # 强制删除该目录及其内部的所有文件和子文件夹
    shutil.rmtree(cache_dir)
    print("旧缓存已清空！")

# 清空后重新建一个干净的文件夹
cache_dir.mkdir()
```

### 5. 打包压缩 `make_archive`

作为一个TA，如果你写了一个 Maya 的插件工具包想要发给外包，或者想要收集崩溃日志，你可以用 `shutil` 直接把文件夹打成 `.zip` 压缩包。

```python
import shutil
from pathlib import Path

tool_folder = Path("D:/Pipeline/Tools/AutoRigger_v1.2")
output_zip = Path("D:/Pipeline/Releases/AutoRigger_v1.2") # 注意这里不要加 .zip 后缀，函数会自动加

# 将整个工具文件夹打包成 zip
shutil.make_archive(
    base_name=str(output_zip), # 压缩包的输出路径和名字
    format='zip',              # 支持 'zip', 'tar', 'gztar' 等
    root_dir=str(tool_folder)  # 要压缩的文件夹路径
)
print("工具包压缩完成！")
# 解压缩
shutil.unpack_archive(output_zip, tool_folder)
```
### 6. 异常处理建议

```Python
import shutil
from pathlib import Path

try:
    shutil.copytree('source', 'destination')
except FileExistsError:
    print("目标目录已存在")
except PermissionError:
    print("没有权限")
except Exception as e:
    print(f"复制失败: {e}")
```
### 总结

在你的 Python 管线脚本里，这套组合拳是最标准的：

- **组装路径、判断存在、建空文件夹** $\rightarrow$ 用 `pathlib`
- **拷贝、移动、删整个文件夹、打压缩包** $\rightarrow$ 调 `shutil`