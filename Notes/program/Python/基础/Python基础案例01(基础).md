# 数据类型
```python
#字符串 string
myStr = "hello world!" 
myStr1 = 'hello'
myStr2 = 'world'
myInt1 = 3
myStr3 = myStr1 + " " +myStr2 #字符串拼接
myStr4 = myStr1 +myStr2 + str(myInt1) #字符串和整型拼接
myStr5 = "my max points number:{}".format(myInt1)#字符串格式化
print(myStr3)
print(myStr1.title()) #首字母大写
print(myStr2.upper()) #全部大写
print(myStr1.lower()) #全部小写
print(myStr4)
print(myStr5)

string1 = "hello \nworld" #\n=换行
print(string1)

string2 = "hello \tworld" #\t=缩进（4个空格）
print(string2)

string3 = "hello \\world" #\\=\
print(string3)

#'a',"a",\"a\",\'a\'
string4 = "polySelectEdgesEveryN \"edgeRing\" 2;"
print(string4)

#格式化字符串
i = 'world'
a = '!!!'
string5 ='hello {} {}'.format(i,a)
print(string5)

myInt = 1 #整型 int
myFloat = 2.5 #浮点型 float
hasMaterial = True #布尔型 bool
print(myStr)
```
# list(列表)
```python
myListint = [1, 2, 3, 4, 5, 6]
myListStr = ["asd", "qwe", "zxc"]
myListint.append(8)  # append新增至最后
myListint.insert(2, 9)  # 在第几位插入某元素
del myListint[1]  # 删除第二项
a = myListint.pop(1)  # 取出第二项到a中
myListint.sort()  # 从小到大排序
myListLen = len(myListint)  # 列表位数
newList = myListint[0:3]  # 列表切片，只要前三项
newList = myListint[:-1]  # 列表切片，排除最后一项
newList = myListint[::2]  # 列表切片，步长为2
myListStr.remove("qwe")  # 列表中移除
print(myListint)
print(myListint[0])  # 0代表第一项
print(myListStr[-1])  # -1代表倒数第一项，-2代表倒是第二项。
print(myListLen)
print(newList)

"""-----append和extend的区别-----
在Python列表中，`append()`用于在列表末尾添加新的对象，而`extend()`用于向列表尾部添加另一个列表的元素，将两个列表合并成一个列表。"""

# append()例子
list_all = []
list1 = [1, 2, 'cc', 'dd']
list2 = ['e', 3]
list_all.append(list1)
list_all.append(list2)
print(list_all)
# [[1, 2, 'cc', 'dd'], ['e', 3]]

# extend()例子
list_all = []
list1 = [1, 2, 'cc', 'dd']
list2 = ['e', 3]
list_all.extend(list1)
list_all.extend(list2)
print(list_all)
# [1, 2, 'cc', 'dd', 'e', 3]

```
# dictionary(字典)
```python
polyCubeDict = {
    "name": "cube1",
    "position": [0.1, 5.2, 3.7],
    "points": 8,
    "edges": 12,
    "faces": 6,
    "material": "lambert1",
}  # 创建字典键值对

polyCubeDict["name"] = "cube2"  # 修改字典内容
polyCubeDict["hasUV"] = True  # 新增字典键值对
del polyCubeDict["faces"]  # 删除字典键值对

name = polyCubeDict["name"]
pos = polyCubeDict["position"]
mat = polyCubeDict["material"]
print(name)
print(pos)
print(mat)
print(polyCubeDict)
print(polyCubeDict.keys())  # 只打印键
print(polyCubeDict.values())  # 只打印值
print(polyCubeDict.items())  # 打印键和值
```
# loop(循环)
```python
# while循环
#案例1
correctPw = "123456"
inputPW = input("Input your password: ")

while inputPW != correctPw:
    print("Incorrect!!!")
    inputPW = input("Input your password: ")

print("Password correct")

#案例2
correctPw = "123456"
while True:
    inputPW = input("Input your password: ")
    if inputPW == correctPw:
        print("Password correct")
        break
    else:
        print("Incorrect!!!")
# for循环
import pymel.core as pm

myStr = "hello world!"
for letter in myStr:
    print("the letter is:")
    print(letter)

print("the end")


myInt = [3, 1, 9, 7, 4, 6]
for i in range(len(myInt)):
    print(myInt[i])




selList = pm.ls(sl=True)
for i in range(len(selList)):
    pos = selList[i].getTranslation()
    selList[i].setTranslation([pos.x, pos.y + i, pos.z])
print(selList)


polyCubeDict = {
    "name": "cube1",
    "position": [0.1, 5.2, 3.7],
    "points": 8,
    "edges": 12,
    "faces": 6,
    "material": "lambert1",
}
for k, v in polyCubeDict.items():
    print("key:{},value:{}".format(k, v))


"""枚举循环"""
import pymel.core as pm

obj = pm.selected()
# 枚举
for index, data in enumerate(obj):
    print(index, data)
```
# branch(分支)
```python
#案例1
a = 123
b = 124
if a > b:
    print("a>b")
elif a < b:
    print("a<b")
else:
    print("a=b")

#案例2
age1 = 20
age2 = 17
if (age1 >= 18) and (age2 >= 18):
    print("OK")
else:
    print("No")

#案例3
age1 = 20
age2 = 17
if (age1 >= 18) or (age2 >= 18):
    print("OK")
else:
    print("No")

#案例4
polyCube = ['cube1',[0.1,5.2,3.7],8,12,6,'lambert1']
if "cube1" in polyCube:
    print("Find Item!")
else:
    print("Not Found!")

#案例5
import pymel.core as pm

selList = pm.ls(sl=True)

cubePre = "pCube"
sphPre = "pSphere"

for sel in selList:
    name = sel.name()
    if name[:-1]==cubePre:
        sel.setParent("CubeGrp")
    elif name[:-1]==sphPre:
        sel.setParent("SphereGrp")
```
# iterator(迭代器)
```python
# iterator迭代器：可迭代对象(iterable):list, tuple, string, set, dict, bytes
my_list = [1, 2, 3, 4, 5, 6, 7]
list_iter = iter(my_list)
print(next(list_iter))
print(next(list_iter))
print(next(list_iter))
```
# generator(生成器)
```python
"""--------------------案例1-------------"""

from collections.abc import Iterable
# ()推导式表示生成器，tuple()推导式表示元组推导式
gen = (x for x in range(1, 101))
print(isinstance(gen, Iterable))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))

for i in gen:
    print(i)

"""--------------------案例2------------------"""


def fibonacci(n: int):
    """
    斐斐波那契数列
    Args:
        n: 数列迭代次数

    Returns:斐斐波那契数列列表

    """
    a, b = 0, 1
    res = []
    for count in range(0, n+1):
        res.append(a + b)
        a, b = b, a + b

    return res


print(fibonacci(10))


# 斐波那契数列生成器
def generator_fibonacci(n: int):
    """
    生成器方式实现斐波那契数列
    Args:
        n: 数列迭代次数

    Returns:斐斐波那契数列列表

    """
    a, b = 0, 1

    for count in range(0, n+1):
        yield a + b
        a, b = b, a + b


gen = generator_fibonacci(10)
next(gen)
for i in gen:
    print(i)
```
# 异常捕获
```python
try:
    print(a)
    print("123")
    a = 1/0
except NameError:
    print("变量没有声明")
except ZeroDivisionError:
    print("除等于零")
except Exception as e:
    print (e)

finally:
    print("hello world!!!")
```