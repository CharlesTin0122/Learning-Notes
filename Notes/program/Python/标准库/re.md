你好！作为一名动画TA，你平时在Maya或Unreal中做绑定脚本（比如批量重命名骨骼、解析控制器名称、处理FBX文件路径等）时，Python的 `re`（Regular Expression，正则表达式）库绝对是一个“神兵利器”。

`re` 库是Python内置的正则表达式模块，专门用于**字符串的模式匹配、查找、替换和分割**。

为了贴合你的日常工作场景，我将结合绑定和资产处理的例子来系统介绍 `re` 库的核心用法。

---

### 0. 正则表达式基础语法

|符号|含义|示例|匹配内容|
|---|---|---|---|
|.|任意单个字符（除换行）|a.c|abc, a1c, a@c|
|\d|数字 0-9|\d{3}|123, 999|
|\D|非数字|\D|a, @, 空格|
|\w|单词字符（字母、数字、下划线）|\w+|hello_123|
|\s|空白字符（空格、tab、换行）|\s+|多个空格|
|[]|字符类|[a-z0-9]|小写字母或数字|
|^|开头|^\d|以数字开头|
|$|结尾|\d$|以数字结尾|
|`|`|或|`cat|
|()|分组|(\d{3})|捕获3位数字|
|? * + {n,m}|量词|a?、a*、a+、a{2,5}|0或1个、0+、1+、2到5个a|

**常用量词**：

- *：0 个或多个
- +：1 个或多个
- ?：0 个或 1 个
- {n}：正好 n 个
- {n,}：至少 n 个
- {n,m}：n 到 m 个

**贪婪 vs 非贪婪**：* + 默认贪婪（匹配尽可能多），加 ? 变成非贪婪（如 *?）。

---

### 1. 必须要知道的前提：原生字符串（Raw String）

在使用 `re` 库时，建议**永远在正则表达式的字符串前面加 `r`**（例如 `r"\d+"`）。因为正则表达式里有大量的反斜杠 `\`，如果不加 `r`，你需要写成 `"\\d+"` 来避免Python转义，这会非常难以阅读。

---

### 2. `re` 库的四大核心函数

**常用函数**：

1. **re.match(pattern, string)** 从**字符串开头**匹配，返回 Match 对象或 None。
2. **re.search(pattern, string)** 在**整个字符串中搜索第一个匹配**，最常用。
3. **re.findall(pattern, string)** 返回**所有非重叠匹配的列表**（字符串列表或元组列表）。
4. **re.finditer(pattern, string)** 返回迭代器，每个元素是 Match 对象（推荐大数据量）。
5. **re.sub(pattern, repl, string)** 替换匹配的内容。
6. **re.split(pattern, string)** 根据模式分割字符串。

#### ① 查找所有匹配项：`re.findall()` 和 `re.finditer()`

这是最常用的功能，用于从文本中提取符合规则的所有内容。

- `findall` 返回一个列表。
- `finditer` 返回一个迭代器（包含匹配对象，可以获取具体的起止位置）。

**TA实战场景**：从一段乱码或长路径中提取所有的资产版本号。

```python
import re

text = "Exported files: run_v001.fbx, walk_v02.fbx, idle_v3.fbx"
# 提取 v 后面跟着数字的字符串
versions = re.findall(r"v\d+", text)
print(versions)  
# 输出: ['v001', 'v02', 'v3']
```

#### ② 模式替换：`re.sub()`

非常强大的批量替换工具，比字符串自带的 `.replace()` 强大无数倍。

**TA实战场景**：镜像绑定时，批量将左侧（L）的命名替换为右侧（R），同时忽略大小写或特定位置。

```python
import re

ctrl_name = "L_arm_IK_ctrl_01_L_proxy"
# 需求：只把开头的 L_ 或者 _L_ 替换成 R，保留其他部分
# 解释：^L_ 匹配开头的 L_， |_L_ 匹配中间的 _L_
new_name = re.sub(r"^L_|_L_", "R_", ctrl_name)
print(new_name)  
# 输出: R_arm_IK_ctrl_01R_proxy (注意这里正则写得比较简单，实战中可以使用正则的分组来精准替换)
```

#### ③ 匹配开头：`re.match()`

从字符串的**最开头**开始匹配。如果开头不符合规则，就算后面有符合的也会返回 `None`。

**TA实战场景**：检查节点命名是否符合项目规范（例如：必须以 `M_`, `L_`, `R_` 开头）。

```python
import re

def check_naming_convention(node_name):
    # 匹配开头必须是 L_, R_, M_ 之一
    if re.match(r"^(L|R|M)_", node_name):
        return True
    return False

print(check_naming_convention("L_leg_jnt"))  # True
print(check_naming_convention("spine_M_jnt")) # False (因为不是以M_开头)
```

#### ④ 全局搜索：`re.search()`

扫描整个字符串，找到**第一个**匹配的位置就返回一个 Match 对象。

**TA实战场景**：从带命名空间的 Maya 节点名中分离出基础名称。

```python
import re

node = "char_01:rig_grp:L_hand_ctrl"
# 查找最后一个冒号之后的所有字符
match = re.search(r"[^:]+$", node)
if match:
    print(match.group())  
    # 输出: L_hand_ctrl
```

---

### 3. 高级技巧：分组（Grouping）

在绑定脚本中，我们经常需要把一个名字拆成几个部分（前缀、部位、类型、序号）。使用括号 `()` 可以实现提取。

```python
import re

node_name = "L_index_finger_jnt_03"
# 正则解析：(左右)_(部位)_(节点类型)_(数字序号)
# (?P<name>...) 是命名分组，方便直接通过名字提取，代码可读性极高
pattern = r"(?P<side>[A-Z])_(?P<part>\w+)_(?P<type>[a-z]+)_(?P<index>\d+)"

match = re.search(pattern, node_name)
if match:
    print("完整匹配:", match.group(0))      # L_index_finger_jnt_03
    print("部位:", match.group("part"))    # index_finger
    print("类型:", match.group("type"))    # jnt
    print("所有分组:", match.groups())     # ('L', 'index_finger', 'jnt', '03')
    print("字典形式:", match.groupdict())  # {'side': 'L', 'part': 'index_finger', 'type': 'jnt', 'index': '03'}
```

_如果你要写一个通用的重命名或镜像工具，`match.groupdict()` 会让你的逻辑变得异常清晰。_

---

### 4. 性能优化：`re.compile()`

如果你在处理动捕数据或者遍历数万个顶点/节点，同一个正则表达式会被循环执行几千次。这时**务必提前编译正则表达式**，这会显著提升脚本运行速度。

```python
import re
import time

# 提前编译好正则对象
number_pattern = re.compile(r"\d+")

nodes = ["point_01", "point_02", "point_03"] # 假设这里有几万个节点

for node in nodes:
    # 直接使用编译好的对象调用方法，速度更快
    match = number_pattern.search(node)
    if match:
        pass # 执行你的逻辑
```

---



掌握了 `re` 库，以后在 Maya 或 UE 里写 Python 处理字符串、做自动化检查（Sanity Check）、批量重命名工具时，原本需要几十行 `split()` 和 `if-else` 的代码，往往一两行正则就能优雅搞定了。