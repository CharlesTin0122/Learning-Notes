# NumPy 用法笔记 · numpy_03

本文档基于 `numpy_03.py` 整理，介绍 NumPy 的**矩阵切片与运算、随机矩阵、去重、转置、反转、扁平化、数据保存与读取**等核心用法。

```python
import numpy as np
```

---

## 1. 矩阵切片

先构造一个 3×2 矩阵：

```python
data = np.array([[1, 2], [3, 4], [5, 6]])
# [[1 2]
#  [3 4]
#  [5 6]]
```

二维数组的索引格式为 `data[行, 列]`，行、列均支持切片：

```python
sel_0 = data[0]        # 第 0 行 -> [1 2]
sel_1 = data[1:3]      # 第 1~2 行 -> [[3 4], [5 6]]
sel_2 = data[1:3, 0]   # 第 1~2 行的第 0 列 -> [3 5]
sel_3 = data[1, 1]     # 第 1 行第 1 列的单个元素 -> 4
```

| 写法 | 含义 | 结果 |
| --- | --- | --- |
| `data[0]` | 取一行 | 一维数组 |
| `data[1:3]` | 行切片 | 二维数组 |
| `data[1:3, 0]` | 行切片 + 列索引 | 一维数组 |
| `data[1, 1]` | 单元素 | 标量 |

---

## 2. 矩阵逐元素运算

形状相同的矩阵可以直接进行逐元素（element-wise）运算：

```python
d1 = np.arange(1, 5).reshape(2, 2)  # [[1 2], [3 4]]
d2 = np.arange(5, 9).reshape(2, 2)  # [[5 6], [7 8]]

d3 = d1 + d2  # [[ 6  8], [10 12]]
```

> `-`、`*`、`/` 同理，均为对应位置逐元素运算（矩阵乘法要用 `@` 或 `np.matmul`）。

---

## 3. 随机矩阵

新版 NumPy 推荐使用 `default_rng()` 创建随机数生成器（Generator），代替旧的 `np.random.rand` 等函数：

```python
rng = np.random.default_rng()

# 随机浮点数矩阵，取值范围 [0, 1)
rnd = rng.random((4, 4))

# 随机整数矩阵：0~10，4×4，endpoint=True 表示包含上界 10
rnd1 = rng.integers(10, size=(4, 4), endpoint=True)
```

- `rng.random(shape)`：均匀分布的浮点数，`[0, 1)`。
- `rng.integers(high, size=..., endpoint=...)`：随机整数，默认**不包含** `high`，`endpoint=True` 时包含。
- `default_rng(seed)` 可传入种子以获得可复现的结果。

---

## 4. 去除重复元素 `np.unique`

### 4.1 一维数组去重

```python
array = np.array([1, 2, 3, 3, 4, 5, 5, 5])

# return_index=True：同时返回每个唯一值首次出现的索引
unique, indices = np.unique(array, return_index=True)
# unique  -> [1 2 3 4 5]
# indices -> [0 1 2 4 5]

# return_counts=True：同时返回每个唯一值出现的次数
unique, counts = np.unique(array, return_counts=True)
# unique -> [1 2 3 4 5]
# counts -> [1 1 2 1 3]
```

### 4.2 二维数组按轴去重

```python
matrix = np.array([[1, 1, 2], [1, 1, 2], [6, 6, 7]])

unique1 = np.unique(matrix, axis=0)  # 按行去重 -> [[1 1 2], [6 6 7]]
unique2 = np.unique(matrix, axis=1)  # 按列去重 -> [[1 2], [1 2], [6 7]]
```

> 不指定 `axis` 时，`np.unique` 会先扁平化再去重，返回一维结果。

---

## 5. 转置

```python
data = np.zeros((5, 2))

transpose1 = data.transpose()  # shape (5, 2) -> (2, 5)
transpose2 = data.T            # 简化写法，效果相同
```

> 转置返回的是**视图**而非副本，修改转置结果会影响原数组。

---

## 6. 反转 `np.flip`

`np.flip(a, axis=n)` 沿指定轴反转元素顺序：

```python
arr = np.arange(12).reshape(3, 4)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

reversed_arr1 = np.flip(arr, axis=0)  # 上下反转（行顺序倒置）
# [[ 8  9 10 11]
#  [ 4  5  6  7]
#  [ 0  1  2  3]]

reversed_arr2 = np.flip(arr, axis=1)  # 左右反转（列顺序倒置）
# [[ 3  2  1  0]
#  [ 7  6  5  4]
#  [11 10  9  8]]
```

> 不指定 `axis` 时会沿**所有轴**反转。

---

## 7. 扁平化 `flatten`

`flatten()` 把任意维度的数组展开成一维，**返回新数组（副本）**：

```python
ones = np.ones((2, 2, 2), dtype=int)
flattened = ones.flatten()  # [1 1 1 1 1 1 1 1]
```

> 类似的 `ravel()` 返回的是视图（尽可能不复制），`flatten()` 总是复制。

---

## 8. 保存与读取数据

### 8.1 单个数组：`np.save` / `np.load`

保存为 `.npy` 二进制文件：

```python
data = np.array([[1, 2, 3], [4, 5, 6]])

np.save("data.npy", data)         # 保存到当前工作目录
loaded_data = np.load("data.npy") # 读取，得到原数组
```

### 8.2 多个数组：`np.savez`

保存为 `.npz` 文件（多个 `.npy` 的打包），用**关键字参数**命名各数组：

```python
data1 = np.array([[1, 2, 3], [4, 5, 6]])
data2 = np.array([[7, 8, 9], [10, 11, 12]])

np.savez("data.npz", data1=data1, data2=data2)

loaded_data = np.load("data.npz")
files = loaded_data.files          # 数组名列表 -> ['data1', 'data2']
loaded_data1 = loaded_data["data1"]  # 按名称取出
loaded_data2 = loaded_data["data2"]
```

- `.npy`：单个数组，`load` 直接返回数组。
- `.npz`：多个数组，`load` 返回类字典对象，通过 `files` 属性查看名称，按键取值。
- 需要压缩时可用 `np.savez_compressed`。

---

## 小结

- **矩阵切片**：`data[行, 列]`，行列均可用切片或单索引。
- **矩阵运算**：同形状矩阵 `+ - * /` 逐元素运算。
- **随机矩阵**：`default_rng()` 生成器，`random` 出浮点、`integers` 出整数（`endpoint` 控制是否含上界）。
- **去重**：`np.unique` 配合 `return_index` / `return_counts` / `axis`。
- **转置与反转**：`.T` 转置；`np.flip(a, axis)` 沿轴反转。
- **扁平化**：`flatten()` 返回一维副本。
- **存取**：`save`/`load` 存单个数组（`.npy`），`savez` 存多个（`.npz`）。
