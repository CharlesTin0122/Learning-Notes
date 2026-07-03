# NumPy 用法笔记 · numpy_02

本文档基于 `numpy_02.py` 整理，介绍 NumPy 的**维度变换、条件索引、数组合并、深拷贝、数组运算、广播、统计方法与轴（axis）**等核心用法。

```python
import numpy as np
```

---

## 1. 改变 / 扩展维度

### 1.1 `np.newaxis`

`np.newaxis` 本质就是 `None`，用在索引里表示**在该位置插入一个长度为 1 的新维度**。

```python
array_01 = np.arange(3)          # 一维数组 [0, 1, 2]，shape = (3,)

array_h = array_01[np.newaxis, :]  # 前面插入新轴 -> [[0, 1, 2]]，shape = (1, 3)
array_v = array_01[:, np.newaxis]  # 后面插入新轴 -> [[0], [1], [2]]，shape = (3, 1)
```

### 1.2 `np.expand_dims`

`np.expand_dims(a, axis=n)` 与 `np.newaxis` 等价，用 `axis` 参数指定插入位置，语义更明确。

```python
expanded   = np.expand_dims(array_01, axis=0)  # [[0, 1, 2]]，shape = (1, 3)
expanded_v = np.expand_dims(array_01, axis=1)  # [[0], [1], [2]]，shape = (3, 1)
```

| 方法 | 作用 | 结果形状 |
| --- | --- | --- |
| `a[np.newaxis, :]` / `expand_dims(a, 0)` | 前面加一行 | `(1, 3)` |
| `a[:, np.newaxis]` / `expand_dims(a, 1)` | 后面加一列 | `(3, 1)` |

---

## 2. 索引与切片（布尔条件索引）

先构造一个 3×3 数组：

```python
array_02 = np.arange(9).reshape(3, 3)
# [[0, 1, 2],
#  [3, 4, 5],
#  [6, 7, 8]]
```

### 2.1 布尔条件切片

用一个布尔表达式作为索引，会返回所有满足条件的元素（**结果为一维数组**）。

```python
even_nums = array_02[array_02 % 2 == 0]   # 所有偶数 -> [0 2 4 6 8]
less_3    = array_02[array_02 < 3]         # 所有小于 3 的数 -> [0 1 2]
```

### 2.2 多条件组合

多个条件要用位运算符 `&`（与）、`|`（或），**每个条件必须用括号括起来**（因运算符优先级问题）。

```python
mult_cond_nums = array_02[(array_02 % 2 == 0) & (array_02 > 5)]  # 偶数且大于 5 -> [6 8]
```

### 2.3 条件数组 与 `np.nonzero`

条件表达式本身会生成一个同形状的**布尔数组**：

```python
cond = (array_02 % 2 == 0) & (array_02 > 5)
# [[False False False],
#  [False False False],
#  [ True False  True]]
```

`np.nonzero` 返回**非零（True）元素的索引**，常用于根据条件获取坐标。返回值是一个元组，每个元素对应一个维度的索引数组：

```python
cond_index = np.nonzero(array_02 % 2 == 0)
# (array([0, 0, 1, 2, 2]),   # 行索引
#  array([0, 2, 1, 0, 2]))   # 列索引
```

---

## 3. 合并数组

```python
array_a = np.array([[1, 2], [3, 4]])
array_b = np.array([[4, 5], [6, 7]])
```

| 方法 | 说明 | 结果 |
| --- | --- | --- |
| `np.hstack((a, b))` | 水平堆叠（按列合并） | `[[1 2 4 5], [3 4 6 7]]` |
| `np.vstack((a, b))` | 垂直堆叠（按行合并） | `[[1 2], [3 4], [4 5], [6 7]]` |

```python
array_c = np.hstack((array_a, array_b))  # 水平堆叠
array_d = np.vstack((array_a, array_b))  # 垂直堆叠
```

> 注意：参数是**一个元组** `(a, b)`，不要漏掉外层括号。

---

## 4. 深拷贝 `.copy()`

NumPy 的切片默认是**视图（view）**，修改切片会影响原数组。需要独立副本时用 `.copy()` 做深拷贝。

```python
array_03 = np.arange(10)
array_slice = array_03[3:7].copy()  # 对切片深拷贝
array_slice[0] = 100                # 修改副本不会影响 array_03
```

---

## 5. 数组运算

### 5.1 逐元素算术

两个等长数组按对应位置逐元素运算。

```python
array_04 = np.array([1, 2, 3])
array_05 = np.array([4, 5, 6])

plus  = array_04 + array_05   # 加法 [5 7 9]
minus = array_04 - array_05   # 减法 [-3 -3 -3]
mul   = array_04 * array_05   # 乘法 [ 4 10 18]
div   = array_04 / array_05   # 除法 [0.25 0.4  0.5]
power = array_04 ** array_05  # 幂运算 [1 32 729]
```

### 5.2 聚合运算（`sum` / `prod` 与 axis）

```python
array_06 = np.array([[1, 2], [3, 4]])

array_06.sum()          # 全部求和 -> 10
array_06.sum(axis=0)    # 按列求和（垂直相加）-> [4 6]
array_06.sum(axis=1)    # 按行求和（水平相加）-> [3 7]

array_06.prod()         # 全部乘积 -> 24
array_06.prod(axis=0)   # 按列乘积（垂直相乘）-> [3 8]
array_06.prod(axis=1)   # 按行乘积（水平相乘）-> [2 12]
```

---

## 6. 广播（Broadcasting）

广播允许**形状不同但兼容**的数组一起运算，NumPy 会自动扩展较小的数组。

### 6.1 数组 × 标量

```python
mult_01 = 4
result = array_06 * mult_01   # 每个元素乘以 4 -> [[4 8], [12 16]]
```

### 6.2 形状兼容的数组相乘

`(2, 2)` 数组与 `(1, 2)` 数组相乘，后者会沿行方向广播：

```python
mult_02 = np.array([[2, 3]])
result_02 = array_06 * mult_02  # [[2 6], [6 12]]
```

### 6.3 形状不兼容会报错

```python
# mult_03 = np.array([[2, 3, 4]])   # (1, 3)
# result_03 = array_06 * mult_03    # 与 (2, 2) 不兼容 -> ValueError
```

> **广播规则**：从末尾维度对齐，对应维度要么相等，要么其中一个为 1，否则报错。

---

## 7. 常用统计方法

```python
ages = np.array([25, 30, 35, 40, 45])

ages.max()      # 最大值 -> 45
ages.min()      # 最小值 -> 25
ages.sum()      # 求和   -> 175
ages.mean()     # 平均值 -> 35.0
ages.prod()     # 乘积   -> 47250000
ages.std()      # 标准差 -> 7.0710678118654755
np.median(ages) # 中位数 -> 35.0
```

- **标准差 `std`**：衡量数据相对于平均值的离散程度，数据越分散标准差越大。
- **中位数 `median`**：注意它是 `np.median(a)` 的形式，**不是**数组方法 `a.median()`。

---

## 8. 轴（axis）的理解

以 4×4 矩阵为例：

```python
matrix = np.arange(1, 17).reshape(4, 4)
# [[ 1  2  3  4]
#  [ 5  6  7  8]
#  [ 9 10 11 12]
#  [13 14 15 16]]

matrix.max(axis=0)  # 按列取最大值 -> [13 14 15 16]
matrix.max(axis=1)  # 按行取最大值 -> [ 4  8 12 16]
```

**记忆要点**：

| `axis` | 方向 | 效果 |
| --- | --- | --- |
| `axis=0` | 沿行方向（竖直）压缩 | 得到**每一列**的结果 |
| `axis=1` | 沿列方向（水平）压缩 | 得到**每一行**的结果 |

> 直觉：`axis=n` 表示"消掉第 n 个维度"，运算沿该维度进行。

---

## 小结

- **维度变换**：`np.newaxis` / `np.expand_dims` 增加长度为 1 的新轴。
- **条件索引**：布尔数组切片返回一维结果；多条件用 `&`/`|` 并加括号；`np.nonzero` 取满足条件的索引。
- **合并**：`hstack` 按列、`vstack` 按行，参数为元组。
- **深拷贝**：切片是视图，`.copy()` 才独立。
- **运算与广播**：逐元素运算 + 兼容形状自动广播。
- **统计与轴**：`sum/prod/mean/std` 等配合 `axis` 控制聚合方向。
