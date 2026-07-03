import numpy as np

# 数组
vector = np.array([1, 2, 3, 4, 5, 6])
matrix = np.array([[1, 2, 3], [4, 5, 6]])
# 数组中的所有元素必须为同一类型数据，如果数据类型不同，np会强行转化
vec_01 = np.array([1, 2, 3, 4, 5, 6, "x"])  # 所有元素都转化为字符串
vec_02 = np.array([1, 2, 3, 4, 5, 6, 7.5])  # 所有元素转化为浮点数
# 一个数组一旦被创建，数组的长度就不能改变了，如果想要改变长度，只能创建新数组
new_vec = np.append(vector, [10, 20])
# 矩阵的每个元素的长度必须相同，否则会出错
# mat_01 = np.array([[1, 2, 3], [4, 5, 6, 7]])  # 会报错

# 访问元素
ele_01 = vector[1]  # 访问第二个元素，值为2
ele_02 = matrix[1, 2]  # 访问第二行第三列元素，值为6
# 修改元素
vector[2] = 999
matrix[0, 1] = 888
# 切片,获取数组的一部分，并非创建独立副本，修改切片即修改原始数据。
slice_vec = vector[1:4]  # [2 3 4]
slice_vec_02 = vector[::2]  # Step2 [1 3 5]
slice_mat = matrix[:, 1]  # 所有行中的第二列 [2 5]

# 数组属性
dimensions = matrix.ndim  # 矩阵的维度，2
size = matrix.size  # 矩阵的元素总数，6
shape = matrix.shape  # 矩阵的形状，(2, 3)
type = matrix.dtype  # 矩阵的数据类型，int64
# 如果要指定元素类型
type_02 = np.array([1, 2, 3], dtype=np.int16)  # 指定元素类型为int16,占用内存小

# 特殊创建方法,构建一个全0数字，元素类型为float64
zeros_01 = np.zeros(5)  # 创建一个全零数组
zeros_02 = np.zeros((2, 3), dtype=np.int64)  # 创建一个2行3列int类型全零矩阵
ones = np.ones((2, 3))  # 创建一个2行3列全1矩阵
# 创建随机数数组
empty = np.empty((2, 3))  # 创建一个2行3列空矩阵
# range范围创建数组
range_arry = np.arange(0, 10, 2)  # 0-9,步长为2,[0 2 4 6 8]
# 线性排列数组
linspace_arry = np.linspace(0, 10, 5)  # 0-10,5个元素[0, 2.5, 5, 7.5, 10]

# 重塑数组
sort_array = np.array([1, 3, 2, 5, 4])
sort_array.sort()  # 排序[1 2 3 4 5]
# 拼接数组，除了随手拼两个小数组用`np.append`，其余场景一律用 `np.concatenate`
array_a = np.array([1, 2, 3])
array_b = np.array([4, 5, 6])
array_c = np.array([7, 8, 9])
conc_array = np.concatenate((array_a, array_b, array_c))  # 拼接为[1 2 3 4 5 6 7 8 9]
# 重塑数组,返回一个新的数组对象，重塑的行列数相乘必须为数组元素个数
reshape_array = conc_array.reshape((3, 3))  # 重塑为3行3列的矩阵
arrat_1d = reshape_array.reshape(-1)  # 展平为一维数组
print(arrat_1d)
