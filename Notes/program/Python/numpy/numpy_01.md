# 概述

> NumPy 是 Python 科学计算的基础库，核心是高效的多维数组对象 `ndarray`。

```python
import numpy as np
```

---

## 一、创建数组

### 基础创建

```python
vector = np.array([1, 2, 3, 4, 5, 6])          # 一维数组（向量）
matrix = np.array([[1, 2, 3], [4, 5, 6]])       # 二维数组（矩阵）
```

**关键特性：**

- 数组中所有元素**必须为同一类型**，类型不同时 NumPy 会自动向上转换：

  ```python
  np.array([1, 2, 3, "x"])   # 全部转为字符串
  np.array([1, 2, 3, 7.5])   # 全部转为浮点数
  ```

- 数组长度一旦创建**不可改变**；若要“改变长度”，本质是创建新数组：

  ```python
  new_vec = np.append(vector, [10, 20])  # 返回新数组
  ```

- 矩阵每一行的长度必须相同，否则报错：

  ```python
  np.array([[1, 2, 3], [4, 5, 6, 7]])  # ❌ 报错
  ```

### 特殊创建方法

| 方法 | 说明 | 示例 |
| --- | --- | --- |
| `np.zeros(shape)` | 全 0 数组，默认 `float64` | `np.zeros(5)`、`np.zeros((2, 3), dtype=np.int64)` |
| `np.ones(shape)` | 全 1 数组 | `np.ones((2, 3))` |
| `np.empty(shape)` | 未初始化的空数组（值随机，速度快） | `np.empty((2, 3))` |
| `np.arange(start, stop, step)` | 按步长生成，**不含 stop** | `np.arange(0, 10, 2)` → `[0 2 4 6 8]` |
| `np.linspace(start, stop, num)` | 均匀线性排列，**含 stop** | `np.linspace(0, 10, 5)` → `[0 2.5 5 7.5 10]` |

---

## 二、访问与修改元素

```python
# 访问
vector[1]      # 第二个元素，值为 2
matrix[1, 2]   # 第二行第三列，值为 6

# 修改
vector[2] = 999
matrix[0, 1] = 888
```

### 切片（Slicing）

> ⚠️ 切片返回的是**视图（view）**，并非独立副本。修改切片会同步修改原始数据；如需副本请使用 `.copy()`。

```python
vector[1:4]   # [2 3 4]
vector[::2]   # 步长为 2 → [1 3 5]
matrix[:, 1]  # 所有行的第二列 → [2 5]
```

---

## 三、数组属性

```python
matrix.ndim    # 维度数，2
matrix.size    # 元素总数，6
matrix.shape   # 形状，(2, 3)
matrix.dtype   # 数据类型，int64
```

指定元素类型可节省内存：

```python
np.array([1, 2, 3], dtype=np.int16)  # 指定为 int16
```

---

## 四、排序、拼接与重塑

### 排序

```python
sort_array = np.array([1, 3, 2, 5, 4])
sort_array.sort()  # 原地排序 → [1 2 3 4 5]
```

### 拼接

> 随手拼接两个小数组可用 `np.append`；其余场景一律用 `np.concatenate`。

```python
array_a = np.array([1, 2, 3])
array_b = np.array([4, 5, 6])
array_c = np.array([7, 8, 9])
conc_array = np.concatenate((array_a, array_b, array_c))  # [1 2 3 4 5 6 7 8 9]
```

### 重塑（Reshape）

> `reshape` 返回**新的数组对象**；重塑后的行 × 列必须等于原元素总数。

```python
reshape_array = conc_array.reshape((3, 3))  # 重塑为 3×3 矩阵
arr_1d = reshape_array.reshape(-1)          # -1 表示自动推断 → 展平为一维
```

---

## 五、常用速查表

| 需求 | 方法 |
| --- | --- |
| 创建数组 | `np.array` |
| 全 0 / 全 1 / 空数组 | `np.zeros` / `np.ones` / `np.empty` |
| 按步长 / 按数量生成 | `np.arange` / `np.linspace` |
| 追加元素 | `np.append`（返回新数组） |
| 拼接多个数组 | `np.concatenate` |
| 排序 | `.sort()`（原地） |
| 改变形状 | `.reshape()`（返回新数组，`-1` 自动推断） |
| 查看形状 / 维度 / 类型 | `.shape` / `.ndim` / `.dtype` |
