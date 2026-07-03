import numpy as np

# 改变维度
array_01 = np.arange(3)  # 生成一维数组: [0, 1, 2]，形状 shape = (3,)
# np.newaxis 本质就是 None,用在索引里表示"在这个位置插入一个长度为 1 的新维度
# 在最前面插入一行（一个新轴）,变成二维数组: [[0, 1, 2]]，形状 shape = (1, 3)
array_h = array_01[np.newaxis, :]
# 在最后面插入一列（一个新轴）,变成二维数组: [[0], [1], [2]]，形状 shape = (3, 1)
array_v = array_01[:, np.newaxis]
# 扩展维度
# 在最前面插入一行（一个新轴）,变成二维数组: [[0, 1, 2]]，形状 shape = (1, 3)
expanded = np.expand_dims(array_01, axis=0)
# 在最后面插入一列（一个新轴）,变成二维数组: [[0], [1], [2]]，形状 shape = (3, 1)
expanded_v = np.expand_dims(array_01, axis=1)

# 索引和切片
# 生成二维数组: [[0, 1, 2], [3, 4, 5], [6, 7, 8]]，形状 shape = (3, 3)
array_02 = np.arange(9).reshape(3, 3)
# 用条件切片，切片获取所有偶数[0 2 4 6 8]
even_nums = array_02[array_02 % 2 == 0]
# 用条件切片，切片获取所有小于 3 的数[0 1 2]
less_3 = array_02[array_02 < 3]
# 用条件切片，切片获取所有偶数且大于 5 的数[6 8]
mult_cond_nums = array_02[(array_02 % 2 == 0) & (array_02 > 5)]
# 生成条件数组: [[False False False],[False False False],[ True False  True]]
cond = (array_02 % 2 == 0) & (array_02 > 5)
# nonzero,返回非零元素的索引.也可用于根据条件获取索引，切片获取所有偶数的索引(array([0, 0, 1, 2, 2]), array([0, 2, 1, 0, 2]))
cond_index = np.nonzero(array_02 % 2 == 0)

# 合并数组
array_a = np.array([[1, 2], [3, 4]])
array_b = np.array([[4, 5], [6, 7]])
# 水平堆叠，将两个数组按列合并,[[1 2 4 5][3 4 6 7]]
array_c = np.hstack((array_a, array_b))
# 垂直堆叠，将两个数组按行合并,[[1 2][3 4][4 5][6 7]]
array_d = np.vstack((array_a, array_b))

# 深拷贝
array_03 = np.arange(10)
# 切片拷贝，对原数组的切片进行拷贝，修改切片不会影响原数组
array_slice = array_03[3:7].copy()
array_slice[0] = 100

# 数组运算
array_04 = np.array([1, 2, 3])
array_05 = np.array([4, 5, 6])
# 计算
plus = array_04 + array_05  # 加法[5 7 9]
minus = array_04 - array_05  # 减法[-3 -3 -3]
mul = array_04 * array_05  # 乘法[ 4 10 18]
div = array_04 / array_05  # 除法 [0.25 0.4  0.5 ]
power = array_04**array_05  # 幂运算[  1  32 729]
# 自身计算
array_06 = np.array([[1, 2], [3, 4]])
sum = array_06.sum()  # 求和：10
sum_01 = array_06.sum(axis=0)  # 按列求和，垂直相加：[4 6]
sum_02 = array_06.sum(axis=1)  # 按行求和，水平相加：[3 7]
prod = array_06.prod()  # 乘积：24
prod_01 = array_06.prod(axis=0)  # 按列乘积，垂直相乘：[3 8]
prod_02 = array_06.prod(axis=1)  # 按行乘积，水平相乘：[2 12]
# 广播运算
# 将数组的每个元素乘以 multiplier
mult_01: int = 4
result = array_06 * mult_01  # [[4  8][12 16]]
# 两个（2,2）数组相乘，将数组的每个元素与另一个数组的对应元素相乘
mult_02 = np.array([[2, 3]])
result_02 = array_06 * mult_02  # [[ 2  6][ 6 12]]
# （2,2）数组与（2,3）数组相乘，形状不符会报错
# mult_03 = np.array([[2, 3, 4]])
# result_03 = array_06 * mult_03

# 常用方法
ages = np.array([25, 30, 35, 40, 45])
max = ages.max()  # 最大值：45
min = ages.min()  # 最小值：25
sum = ages.sum()  # 求和：175
mean = ages.mean()  # 平均值：35.0
prod = ages.prod()  # 乘积：47250000
# 用来衡量这组年龄数据相对于平均值的离散程度（数据越分散，标准差越大）
std = ages.std()  # 标准差：7.0710678118654755
median = np.median(ages)  # 中位数：35.0

# 轴
matrix = np.arange(1, 17).reshape(4, 4)
"""
[[ 1  2  3  4]
 [ 5  6  7  8]
 [ 9 10 11 12]
 [13 14 15 16]]
"""
max_0 = matrix.max(axis=0)  # 按列最大值：[13 14 15 16]
max_1 = matrix.max(axis=1)  # 按行最大值：[ 4  8 12 16]

