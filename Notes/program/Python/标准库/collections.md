## Python `collections` 库概览  

`collections` 是 Python 标准库中**高性能容器数据类型**的集合，专门为常见编程需求提供更高效、更易用的替代方案。相比内置的 `list`、`dict`、`tuple`、`set`，`collections` 中的容器往往在**特定场景**下性能更好、API 更丰富。

> **导入方式**  
> ```python
> from collections import (
>     Counter, defaultdict, deque, namedtuple, ChainMap,
>     OrderedDict, UserDict, UserList, UserString, abc
> )
> ```

---

## 1. 常用容器一览表

| 类型 | 主要用途 | 关键特性 | 典型示例 |
|------|----------|----------|----------|
| `namedtuple` | 轻量级“具名元组” | 不可变、字段可通过属性访问 | `Point = namedtuple('Point', 'x y')` |
| `deque` | 双端队列 | O(1) 的左右端增删 | `d = deque([1,2,3])` |
| `Counter` | 计数器 | 自动统计元素出现次数 | `c = Counter('abracadabra')` |
| `defaultdict` | 带默认值的字典 | 访问不存在的键时返回默认值 | `d = defaultdict(list)` |
| `OrderedDict` | 有序字典 | 保留插入顺序（Python 3.7+ 普通 dict 已有序） | `od = OrderedDict()` |
| `ChainMap` | 字典链 | 多个字典逻辑上合并，优先前面的 | `c = ChainMap(a, b, c)` |
| `UserDict / UserList / UserString` | 可继承的容器包装 | 方便自定义行为 | `class MyDict(UserDict): …` |

---

## 2. 详细介绍（带代码示例）

### 2.1 `namedtuple` —— 带字段名的元组

```python
from collections import namedtuple

# 定义一个“点”结构体
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 4)

print(p.x, p.y)          # 3 4
print(p)                 # Point(x=3, y=4)

# 支持解包、_asdict、_replace
x, y = p
print(p._asdict())       # {'x': 3, 'y': 4}
p2 = p._replace(y=10)
print(p2)                # Point(x=3, y=10)
```

**适用场景**：代替简单的类、返回结构化数据、CSV 行解析等。

---

### 2.2 `deque` —— 高效双端队列

```python
from collections import deque

d = deque([1, 2, 3])
d.append(4)          # 右端
d.appendleft(0)      # 左端
print(d)             # deque([0, 1, 2, 3, 4])

d.pop()              # → 4
d.popleft()          # → 0
print(d)             # deque([1, 2, 3])

# 限定长度（滑动窗口）
d = deque(maxlen=3)
d.extend([1,2,3,4])
print(d)             # deque([2, 3, 4], maxlen=3)
```

**优势**：`list` 的 `insert(0, ...)` 和 `pop(0)` 是 O(n)，`deque` 是 O(1)。

---

### 2.3 `Counter` —— 计数神器

```python
from collections import Counter

c = Counter('mississippi')
print(c)                     # Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})

print(c.most_common(2))      # [('i', 4), ('s', 4)]
c['i'] += 1
print(c['i'])                # 5

# 数学运算
a = Counter(a=3, b=1)
b = Counter(a=1, b=2)
print(a + b)                 # Counter({'a': 4, 'b': 3})
print(a - b)                 # Counter({'a': 2})
```

**常见用途**：词频统计、投票计数、库存管理。

---

### 2.4 `defaultdict` —— 自动提供默认值

```python
from collections import defaultdict

# 列表默认值
d = defaultdict(list)
d['key'].append(1)
d['key'].append(2)
print(d)                     # defaultdict(<class 'list'>, {'key': [1, 2]})

# int 默认 0（常用于计数）
cnt = defaultdict(int)
for word in 'the quick brown fox'.split():
    cnt[word] += 1
print(cnt)
```

**省去** `if key not in d: d[key] = []` 的繁琐判断。

---

### 2.5 `OrderedDict`（Python 3.7+ 可选）

```python
from collections import OrderedDict

od = OrderedDict()
od['z'] = 1
od['y'] = 2
od['x'] = 3
print(list(od.keys()))   # ['z', 'y', 'x']（保持插入顺序）

# 移动到末尾
od.move_to_end('y')
print(list(od.keys()))   # ['z', 'x', 'y']
```

> **Python 3.7+**：普通 `dict` 已保证插入顺序，`OrderedDict` 仅在需要 `move_to_end`、`popitem(last=False)` 等额外方法时使用。

---

### 2.6 `ChainMap` —— 多字典合并视图

```python
from collections import ChainMap

defaults = {'theme': 'Dark', 'lang': 'en'}
user = {'theme': 'Light'}

config = ChainMap(user, defaults)
print(config['theme'])   # Light（优先 user）
print(config['lang'])    # en
```

**优势**：不复制数据，更新任一底层 dict 都会实时反映。

---

### 2.7 `UserDict / UserList / UserString` —— 自定义容器

```python
from collections import UserDict

class MyMapping(UserDict):
    def __setitem__(self, key, value):
        print(f"Setting {key} = {value}")
        super().__setitem__(key.upper(), value)

m = MyMapping()
m['name'] = 'Alice'      # Setting name = Alice
print(m['NAME'])         # Alice
```

适合**封装**、**日志**、**校验**等需求。

---

## 3. 小技巧 & 常见坑

| 场景 | 推荐写法 |
|------|----------|
| 统计词频 | `Counter(text.split())` |
| 分组聚合 | `defaultdict(list)` + `for item in data: d[group(item)].append(item)` |
| 实现 LRU 缓存 | `collections.OrderedDict`（或 `functools.lru_cache`） |
| 滑动窗口 | `deque(maxlen=N)` |
| 延迟绑定陷阱 | `defaultdict(lambda: default_factory())` 避免闭包晚绑定问题 |

---

## 4. 性能对比（简要）

| 操作 | `list` | `deque` | `dict` | `defaultdict` |
|------|--------|---------|--------|---------------|
| 左端插入 | O(n) | O(1) | — | — |
| 右端插入 | O(1) | O(1) | O(1) | O(1) |
| 键不存在处理 | 手动 `if` | — | 手动 `if` | 自动默认值 |

---

## 5. 官方文档速查

```text
https://docs.python.org/3/library/collections.html
```

---

### 小结

- **`namedtuple`** → 结构化数据  
- **`deque`** → 高效队列/栈  
- **`Counter`** → 计数统计  
- **`defaultdict`** → 省去键检查  
- **`ChainMap`** → 多配置合并  
- **`User*`** → 自定义容器基类  

掌握 `collections`，能让代码**更简洁、更高效、更 Pythonic**！

---

# collections.abc
## `collections.abc` 是什么？

`collections.abc`（**Abstract Base Classes**，抽象基类）是 Python 标准库 `collections` 模块中的一个**子模块**，它定义了 Python 各种**容器类型**的**抽象接口**。

简单说：

> **`collections.abc` 提供了“容器应该长什么样”的蓝图（接口规范）**，让你可以：
> - **检查**某个对象是否符合某种容器协议（如可迭代、映射、序列等）
> - **自定义容器类**时，继承这些 ABC 来获得标准方法和类型检查支持

---

### 官方文档
```text
https://docs.python.org/3/library/collections.abc.html
```

---

## 1. 为什么需要 `collections.abc`？

在 Python 中，**鸭子类型**（Duck Typing）很常见：

```python
for item in container:  # 只要能迭代就行
    ...
```

但有时候你想**显式声明**或**严格检查**一个对象是否是某种容器：

```python
isinstance(obj, collections.abc.Mapping)   # 是否是“字典类”容器？
isinstance(obj, collections.abc.Sequence)  # 是否是“序列”？
```

`collections.abc` 就是为此而生。

---

## 2. 常用抽象基类（ABC）一览

| ABC | 代表类型 | 关键方法 | 典型实现 |
|-----|----------|----------|----------|
| `Container` | 容器 | `__contains__` | `list`, `dict`, `set` |
| `Iterable` | 可迭代 | `__iter__` | 所有可 `for` 循环的对象 |
| `Sized` | 有大小 | `__len__` | `list`, `dict`, `str` |
| `Hashable` | 可哈希 | `__hash__` | `int`, `str`, `tuple` |
| `Sequence` | 序列 | `__getitem__`, `__len__` | `list`, `tuple`, `str` |
| `MutableSequence` | 可变序列 | 继承 `Sequence` + 增删改 | `list` |
| `Mapping` | 映射（字典） | `__getitem__`, `__len__`, `__iter__` | `dict` |
| `MutableMapping` | 可变映射 | 继承 `Mapping` + `__setitem__`, `__delitem__` | `dict` |
| `Set` | 集合 | `__contains__`, `__iter__`, `__len__` | `set` |
| `MutableSet` | 可变集合 | 继承 `Set` + `add`, `discard` | `set` |

---

## 3. 实际使用示例

### 示例 1：类型检查

```python
from collections.abc import Mapping, Sequence, Iterable

d = {'a': 1}
lst = [1, 2, 3]
s = {1, 2}

print(isinstance(d, Mapping))      # True
print(isinstance(lst, Sequence))   # True
print(isinstance(s, Iterable))     # True
print(isinstance(lst, Mapping))    # False
```

---

### 示例 2：自定义容器（继承 ABC）

```python
from collections.abc import MutableMapping

class MyDict(MutableMapping):
    def __init__(self):
        self._data = {}

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

# 自动获得 .keys(), .values(), .items() 等方法！
md = MyDict()
md['x'] = 10
print(list(md.keys()))   # ['x']
print(isinstance(md, Mapping))  # True
```

> **好处**：继承 `MutableMapping` 后，Python 会自动为你实现 `keys()`, `values()`, `items()`, `get()`, `pop()` 等方法！

---

### 示例 3：注册虚拟子类（不继承也能用 `isinstance`）

```python
from collections.abc import Sequence

class MyRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def __getitem__(self, i):
        if i < self.end - self.start:
            return self.start + i
        raise IndexError
    def __len__(self):
        return self.end - self.start

# 注册为 Sequence 的“虚拟子类”
Sequence.register(MyRange)

r = MyRange(0, 3)
print(isinstance(r, Sequence))  # True
print(len(r))                  # 3
print(r[1])                    # 1
```

---

## 4. `collections.abc` vs `abc` 模块

| 模块 | 作用 |
|------|------|
| `abc` | 通用抽象基类框架（`ABC`, `@abstractmethod`） |
| `collections.abc` | 专门为**容器类型**提供的 ABC，基于 `abc` 实现 |

```python
from abc import ABC, abstractmethod
from collections.abc import MutableMapping

# collections.abc 中的类其实都继承自 abc.ABC
print(issubclass(MutableMapping, ABC))  # True
```

---

## 5. 常见误区

| 误区 | 正确理解 |
|------|----------|
| `collections.abc` 是容器实现 | 不是！它是**接口定义** |
| 必须继承才能用 | 也可以用 `register()` 注册 |
| 普通 `dict` 不是 `Mapping` 子类？ | 是！`dict` **自动注册**为 `Mapping` 的子类 |

```python
print(issubclass(dict, collections.abc.Mapping))  # True
```

---

## 6. 快速参考表

```python
from collections.abc import *

# 类型检查
isinstance(obj, Iterable)      # 能 for 循环？
isinstance(obj, Sequence)      # 支持切片、索引？
isinstance(obj, Mapping)       # 像字典？
isinstance(obj, MutableMapping) # 可修改的字典？
```

---

## 7. 最佳实践建议

| 场景 | 推荐做法 |
|------|----------|
| 写函数接受“任何可迭代对象” | `def f(items: Iterable)` |
| 自定义字典类 | `class MyDict(MutableMapping)` |
| 想让类支持 `len()` 和 `in` | 继承 `Sized` + `Container` |
| 类型注解 | 使用 `typing.MutableMapping`（Python 3.9+ 推荐） |

> **Python 3.9+**：`list`, `dict` 等内置类型已支持直接用于类型注解，`collections.abc` 仍用于 `isinstance` 检查。

---

### 小结：一句话概括

> **`collections.abc` 是 Python 容器类型的“身份证系统”** ——  
> 它不提供实现，但定义了“什么才是字典、序列、可迭代”的标准，  
> 让你能**检查类型**、**自定义容器**、**写更健壮的代码**。

---

# 鸭子类型
## 什么是 **Duck Typing**？

> **“如果它走路像鸭子，叫声像鸭子，那它就是鸭子。”**  
> —— *If it walks like a duck and quacks like a duck, then it is a duck.*

这是 Python（以及其他动态语言）中一种核心的**编程哲学**，叫做 **Duck Typing**（鸭子类型）。

---

### 一句话定义：

> **Duck Typing 是一种“行为优先于类型”的动态类型检查策略**：  
> **只要一个对象实现了你需要的行为（方法/属性），就可以当作该类型使用，而无需显式继承或声明接口。**

---

## 核心思想

| 传统静态语言（Java/C++） | Duck Typing（Python） |
|--------------------------|------------------------|
| 必须声明 `implements Interface` | 不关心类型，只关心行为 |
| 编译时检查 | 运行时检查 |
| `Bird b = new Duck(); b.fly();` | `def fly(bird): bird.fly()` |

---

## 经典示例

```python
def make_it_quack(duck):
    duck.quack()   # 只要有 .quack() 方法就行！

class Duck:
    def quack(self):
        print("Quack!")

class Person:
    def quack(self):
        print("I'm pretending to be a duck!")

# 两个完全不同类的对象，都能“当鸭子用”
make_it_quack(Duck())    # Quack!
make_it_quack(Person())  # I'm pretending to be a duck!
```

> **关键**：`make_it_quack` 函数**不检查类型**，只调用 `.quack()`  
> 只要对象有这个方法，就能正常运行 → 这就是 Duck Typing！

---

## 常见 Duck Typing 协议（隐式接口）

| 行为 | 所需方法 | 典型对象 |
|------|----------|----------|
| 可迭代 | `__iter__()` 或 `__getitem__()` | `list`, `str`, `dict`, `generator` |
| 有长度 | `__len__()` | `list`, `dict`, `str` |
| 支持 `in` | `__contains__()` | `set`, `dict`, `list` |
| 可调用 | `__call__()` | 函数、`lambda`、类实例 |
| 上下文管理 | `__enter__()`, `__exit__()` | `with open(...)` |

```python
# 只要有 __len__ 和 __getitem__，就支持 for 循环和 len()
class MyRange:
    def __len__(self): return 5
    def __getitem__(self, i): 
        if i < 5: return i
        raise IndexError

for x in MyRange():
    print(x)  # 0 1 2 3 4
```

---

## Duck Typing vs 显式接口（对比）

| 方式 | 代码 |
|------|------|
| **Duck Typing（Python）** | ```python
| **显式接口（Java）** | ```java interface Flyable { void fly(); } ``` |

Python 更灵活，但也可能带来运行时错误：

```python
make_it_quack("hello")  # AttributeError: 'str' object has no attribute 'quack'
```

---

## 实际应用场景

| 场景 | Duck Typing 体现 |
|------|------------------|
| `for item in container:` | 只要可迭代就行 |
| `len(obj)` | 只要有 `__len__` |
| `with context:` | 只要有 `__enter__`/`__exit__` |
| `json.dump(obj, f)` | 只要可序列化（有 `.to_json()` 或协议） |

---

## 与 `collections.abc` 的关系

`collections.abc` 就是 **Duck Typing 的“官方协议定义”**：

```python
from collections.abc import Iterable, Mapping

def process_data(data: Iterable):
    for item in data: ...  # Duck Typing

isinstance(my_obj, Mapping)  # 检查是否“像字典”
```

> 你不需要继承 `Mapping`，只要实现 `__getitem__`, `__len__`, `__iter__`，`isinstance` 就返回 `True`！

---

## 优点 vs 缺点

| 优点 | 缺点 |
|------|------|
| 代码简洁、灵活 | 运行时才报错 |
| 易于组合、复用 | IDE 提示弱 |
| 适合快速原型 | 调试稍难 |

---

## 最佳实践建议

1. **写函数时，依赖行为而非类型**
   ```python
   def count_items(container):  # 不要写 list/dict
       return len(container)
   ```

2. **使用类型注解 + Duck Typing**
   ```python
   from typing import Iterable

   def sum_all(numbers: Iterable[float]) -> float:
       return sum(numbers)
   ```

3. **必要时用 `isinstance` 检查协议**
   ```python
   from collections.abc import Mapping

   if not isinstance(config, Mapping):
       raise TypeError("config must be dict-like")
   ```

---

## 一句话总结

> **Duck Typing = “我不管你是什么，只要你会叫（quack），我就当你是鸭子。”**

---

### 小彩蛋：Python 之禅（`import this`）

```python
>>> import this
...
Beautiful is better than ugly.
...
Although practicality beats purity.
```

Duck Typing 正是 **“实用性胜过纯理论”** 的体现！

---

需要我用图解或动画展示 Duck Typing 的执行流程吗？或者来个“鸭子 vs 飞机”实战案例？