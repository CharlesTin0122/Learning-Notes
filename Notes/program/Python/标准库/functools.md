下面为你 **系统、全面地介绍** Python 的 `functools` 模块 —— **函数式编程的瑞士军刀**。

---

## 一、`functools` 模块概述

`functools` 是 Python 标准库中的一个模块，**专为高阶函数和函数操作设计**，主要用于：

> **“让函数更强大、更高效、更可复用”**

```python
import functools
```

> 所有工具都围绕 **函数对象** 展开，符合函数式编程思想。

---

## 二、核心功能分类（共 12 个主要工具）

| 类别 | 工具 | 用途 |
|------|------|------|
| 累积计算 | `reduce` | 迭代归约 |
| 函数缓存 | `lru_cache`, `cache` | 记忆化（加速递归/重复调用） |
| 函数包装 | `wraps`, `partial` | 装饰器、参数预绑定 |
| 函数属性 | `update_wrapper` | 保留原函数元信息 |
| 比较与排序 | `cmp_to_key` | 将旧式 `cmp` 转为 `key` |
| 通用函数 | `singledispatch` | 单分派泛型函数 |

---

## 三、详细讲解（带实战示例）

---

### 1. `functools.reduce(function, iterable[, initializer])`

> **累积计算**：把可迭代对象“折叠”成一个值。

```python
from functools import reduce

# 求阶乘
def factorial(n):
    return reduce(lambda x, y: x * y, range(1, n+1), 1)

print(factorial(5))  # 120
```

> 替代 `sum`, `max`, `min` 的高级用法。

---

### 2. `@functools.lru_cache(maxsize=128, typed=False)`

> **函数结果缓存**（LRU = Least Recently Used）

```python
@functools.lru_cache(maxsize=32)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

print(fib(100))  # 瞬间返回（无缓存会超慢）
```

#### 参数说明
| 参数 | 说明 |
|------|------|
| `maxsize` | 缓存条数，`None` = 无限制 |
| `typed=True` | `fib(3)` 和 `fib(3.0)` 视为不同 |

#### 查看缓存信息
```python
print(fib.cache_info())
# CacheInfo(hits=98, misses=101, maxsize=32, currsize=32)
```

> Python 3.9+ 还有 `@functools.cache`（无限制缓存，简化版）

---

### 3. `functools.partial(func, *args, **kwargs)`

> **参数预绑定**：创建一个“部分应用”的新函数。

```python
from functools import partial

# 原函数
def power(base, exponent):
    return base ** exponent

# 绑定 exponent=2
square = partial(power, exponent=2)
# 绑定 base=2
pow2 = partial(power, 2)

print(square(3))  # 9
print(pow2(5))    # 32
```

#### 常见用途
- GUI 回调：`button.clicked.connect(partial(func, arg1))`
- `map(partial(operator.add, 10), nums)`

---

### 4. `@functools.wraps(wrapped)`

> **装饰器必备**：保留原函数的 `__name__`, `__doc__` 等元信息。

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("调用前")
        result = func(*args, **kwargs)
        print("调用后")
        return result
    return wrapper

@my_decorator
def greet(name):
    """问候函数"""
    return f"Hello, {name}!"

print(greet.__name__)  # greet（不是 wrapper）
print(greet.__doc__)   # 问候函数
```

> 不写 `@wraps` → `__name__` 会变成 `wrapper`

---

### 5. `functools.update_wrapper(wrapper, wrapped)`

> 手动复制函数元信息（`@wraps` 底层实现）

```python
def wrapper(func):
    def inner():
        return func()
    update_wrapper(inner, func)
    return inner
```

---

### 6. `functools.cmp_to_key(func)`

> 将 Python 2 的 `cmp` 函数转为 Python 3 的 `key` 函数，用于 `sorted()`

```python
from functools import cmp_to_key

def cmp(a, b):
    return (a > b) - (a < b)  # -1, 0, 1

sorted_list = sorted(['aa', 'a', 'aaa'], key=cmp_to_key(lambda x,y: len(x)-len(y)))
print(sorted_list)  # ['a', 'aa', 'aaa']
```

---

### 7. `@functools.singledispatch`

> **单分派泛型函数**：根据**第一个参数的类型**选择不同实现。

```python
from functools import singledispatch

@singledispatch
def process(obj):
    print("默认处理:", obj)

@process.register
def _(obj: int):
    print("整数 × 2:", obj * 2)

@process.register
def _(obj: list):
    print("列表长度:", len(obj))

process(5)        # 整数 × 2: 10
process([1,2,3])  # 列表长度: 3
process("hello")  # 默认处理: hello
```

> 类似 C++ 重载、Java 多态，但基于类型。

---

## 四、高级工具（Python 3.8+）

| 工具 | 说明 |
|------|------|
| `@functools.cached_property` | 将方法转为**缓存属性**（只计算一次） |
| `@functools.cache` | 简化版 `lru_cache(maxsize=None)` |

```python
from functools import cached_property

class Circle:
    def __init__(self, r):
        self.r = r

    @cached_property
    def area(self):
        print("正在计算...")
        return 3.14 * self.r ** 2

c = Circle(5)
print(c.area)  # 正在计算... 78.5
print(c.area)  # 78.5（不再计算）
```

---

## 五、实战案例：函数式管道（Pipeline）

```python
from functools import reduce, partial
import operator

data = ["  apple  ", "BANANA", "", "  cherry  "]

pipeline = [
    partial(filter, None),                    # 去空
    partial(map, str.strip),                  # 去空格
    partial(map, str.lower),                  # 小写
    partial(sorted, key=len),                 # 按长度排序
    partial(reduce, operator.add)             # 拼接
]

result = reduce(lambda x, f: f(x), pipeline, data)
print(result)  # applebananacherry
```

---

## 六、性能对比：`lru_cache` vs 无缓存

```python
import time

def fib_no_cache(n):
    return n if n < 2 else fib_no_cache(n-1) + fib_no_cache(n-2)

@functools.lru_cache()
def fib_cache(n):
    return n if n < 2 else fib_cache(n-1) + fib_cache(n-2)

start = time.time()
fib_no_cache(35)  # 可能要 2~3 秒
print("无缓存:", time.time() - start)

start = time.time()
fib_cache(35)     # 瞬间完成
print("有缓存:", time.time() - start)
```

---

## 七、官方文档 & 版本兼容

| 工具 | 最低版本 |
|------|----------|
| `reduce` | Python 3.0（从内置移入） |
| `lru_cache` | Python 3.2 |
| `singledispatch` | Python 3.4 |
| `cached_property` | Python 3.8 |
| `cache` | Python 3.9 |

> 文档：https://docs.python.org/3/library/functools.html

---

## 八、总结：`functools` 核心工具速查表

| 工具 | 一句话总结 | 推荐指数 |
|------|-----------|----------|
| `reduce` | 迭代归约 | ★★★★ |
| `lru_cache` / `cache` | 加速递归 | ★★★★★ |
| `partial` | 参数预绑定 | ★★★★ |
| `wraps` | 装饰器必备 | ★★★★★ |
| `singledispatch` | 类型分派 | ★★★ |
| `cached_property` | 延迟计算属性 | ★★★★ |

---

## 九、彩蛋：你可以用 `functools` 写出“黑魔法”

```python
from functools import partial

# 一行实现“链式调用”
chain = partial(reduce, lambda f, g: lambda x: f(g(x)))

add1 = lambda x: x + 1
mul2 = lambda x: x * 2

pipeline = chain(mul2, add1)  # mul2(add1(x))
print(pipeline(5))  # (5+1)*2 = 12
```

---

