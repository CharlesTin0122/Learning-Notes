# function(函数)
```python
"""函数 function"""

def myfunc(name, age):  # 括号内为形参
    print("Hello! " + name)
    print(str(age) + " years old")

myfunc("Charles", 18)  # 括号内为实参


"""return返回值"""

def maxNum(num1, num2):
    if num1 > num2:
        return num1
    else:
        return num2

c = maxNum(6, 3)
print(c)

"""函数闭包"""

def outer(num1):  # 外部函数
    def inner(num2):  # 内部函数
        nonlocal num1  # 调用外部函数变量为可修改，类似于global
        num1 += num2  # 内外部函数参数相加等于外部函数参数
        print(num1)  # 输出外部函数参数

    return inner  # 返回内部函数

fn = outer(10)  # 外部函数实例化后成为内部函数
fn(10)  # 实例化内部函数
fn(10)  # 实例化内部函数

"""函数装饰器"""

def outer(func):
    def inner():
        print("I`m ly down")
        func()
        print("I`m get up")

    return inner

@outer  # 意为将下sleep函数作为参数填入outer函数，并执行返回inner函数
def sleep():
    import random
    import time

    time.sleep(random.randint(1, 5))
    print("I`m sleepping")

sleep()

"""以上案例和以下案例等同"""

def outer(func):
    def inner():
        print("I`m ly down")
        func()
        print("I`m get up")

    return inner


def sleep():
    import random
    import time

    time.sleep(random.randint(1, 5))
    print("I`m sleepping")

fn = outer(sleep)
fn()

""" 可变参数，关键字参数，参数的打包和解包"""

def print_info(name, age):
    print(f"my name is {name},and my age is {age}")

info_list = ["charles", 16]
print_info(*info_list)  # ‘*’可将参数列表解包成参数

info_dict = {"name": "tom", "age": 18}
print_info(**info_dict)  # "**"可将参数字典解包成参数

def print_args(*args):
    """
    可变参数
    """
    print(args)

print_args(1, 2, 3)  # 将多个参数打包成元组

def print_kwargs(**kwargs):
    print(kwargs)
    print("my name: ", kwargs.get("name"))
    print("my language: ", kwargs.get("language"))

print_kwargs(name="charles")
print_kwargs(name="tom", language="english")

```
## 匿名函数
```python
"""--------------------------------------# 案例1----------------------------------"""

f = lambda x, y: x + y
print(f(1, 2))

"""#------------------------------------------- 案例2-----------------------------------"""

d = lambda x, y: x if x > y else y
print(d(1, 2))


"""---------------------------------------------# 案例3----------------------------------------"""

my_list = [("a", 7), ("b", 9), ("c", 5), ("d", 1), ("e", 8), ("f", 3)]

# sorted（）是一个排序迭代器（iterator），会迭代列表中的每一项进行升序排序，
# 参数1：为可迭代对象
# 参数key: 提供自定义键函数来自定义排序顺序，此处用匿名函数lambda将列表中每一项中的第二项为迭代key
# 参数reverse: 可以设置反向标志以降序请求结果。

sort_list = sorted(my_list, key=lambda x: x[1], reverse=True)
print(sort_list)

"""------------------------------------# 案例4 map 映射 lambda---------------------------------"""
# map()创建一个迭代器，使用来自每个可迭代对象的参数计算函数。
# 参数1：为一个函数
# 参数2：为一个可迭代对象
my_list1 = [1, 2, 3, 4, 5, 6, 7]
my_list2 = [7, 6, 5, 4, 3, 2, 1]

res1 = map(lambda x: x**2, my_list1)
print(list(res1))

res2 = map(lambda x, y: x + y, my_list1, my_list2)
print(list(res2))

"""-------------------------------reduce 归约--------------------------------"""
# 将两个参数的函数从左到右累积地应用于序列的项目，以便将序列减少为单个值。
# 例如，reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) 计算 ((((1+2)+3)+4)+5)。
# 参数1：为要使用的函数，参数2：为可迭代对象，参数3：为基础值
from functools import reduce

res = reduce(lambda x, y: x + y, range(1, 101))
print(res)


my_list3 = ["a", "b", "c", "d", "e", "f", "g"]
res = reduce(lambda x, y: x + y, my_list3, "xyz")
print(res)

"""-----------------------------------------filter过滤---------------------------------"""
# filter()返回一个迭代器，产生那些 function(item) 为真的可迭代对象。
# 如果 function 为 None，则返回为 true 的项
my_list4 = [1, 0, 0, 1, 0, 1, 0]
res = filter(lambda x: True if x == 1 else False, my_list4)
print(list(res))
```
## 递归函数
```python
"""递归:在满足条件的情况下，函数自己调用自己的一中特殊的的编程技巧"""
import os


def test_os():
    print(os.listdir(r"G:\Code\Python"))
    print(os.path.isdir(r"G:\Code\Python"))
    print(os.path.exists(r"G:\Code\Python"))


# 获取文件夹下所有文件
def get_files_recursion(path):
    """
    从指定的文件夹中使用递归方式获取全部的文件列表
    :param path:被判断的文件夹
    :return:包含全部的文件,如果目录无文件或者不存在则返回空
    """
    print(f"当前判断的文件夹是:{path}")
    fileList = []
    if os.path.exists(path):  # 判断目录是存在
        for f in os.listdir(path):  # 遍历目录下所有文件
            newPath = path + "/" + f  # 文件名转换为路径
            if os.path.isdir(newPath):  # 判断文件为文件夹
                fileList += get_files_recursion(newPath)  # 调用函数递归，继续遍历文件夹，并添加到文件列表
            else:  # 判断文件不是文件夹
                fileList.append(newPath)  # 添加到路径变量

    else:  # 判断目录不存在
        print(f"指定的目录{path}不存在")  # 打印信息
        return []  # 返回空列表

    return fileList  # 返回文件列表


if __name__ == "__main__":  # 判断为本文件运行
    print(get_files_recursion(r"G:\Code\Python"))  # 运行函数
```
