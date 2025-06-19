# 1导入模块

```
#添加运行路径
import sys
sys.path.append(r'G:\Code\Python')
#导入模块
from tool import impFbx
reload(impFbx)
impFbx.mainUI()
#如果作为模块导入maya,此行代码下的不会运行
if __name__ == '__main__':
   print('程序自身在运行')
else:
   print('我来自另一模块')
	
```

# 1.4数据类型

```
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
myInt = 1 #整型 int
myFloat = 2.5 #浮点型 float
hasMaterial = True #布尔型 bool
print(myStr)
```

# 1.5列表

```
myListint = [1,2,3,4,5,6]
myListStr = ['asd','qwe','zxc']
myListint.append(8) #append新增至最后
myListint.insert(2,9)#在第几位插入某元素
del myListint[1]#删除第二项
a = myListint.pop(1) #取出第二项到a中
myListint.sort() #从小到大排序
myListLen = len(myListint)#列表位数
newList = myListint[0:3]#列表切片，只要前三项
newList = myListint[:-1]#列表切片，排除最后一项
newList = myListint[::2]#列表切片，步长为2
myListStr.remove('qwe')#列表中移除
print(myListint)
print(myListint[0]) #0代表第一项
print(myListStr[-1]) #-1代表倒数第一项，-2代表倒是第二项。
print(myListLen)
print(newList)
```

# 1.6字典

```
polyCubeDict = {
    'name':'cube1',
    'position':[0.1,5.2,3.7],
    'points':8,
    'edges':12,
    'faces':6,
    'material':'lambert1'
    } #创建字典键值对
polyCubeDict['name'] = 'cube2' #修改字典内容
polyCubeDict['hasUV'] = True #新增字典键值对
del polyCubeDict['faces'] #删除字典键值对
name = polyCubeDict['name']
pos = polyCubeDict['position']
mat = polyCubeDict['material']
print(name)
print(pos)
print(mat)
print(polyCubeDict)
print(polyCubeDict.keys()) #只打印键
print(polyCubeDict.values()) #只打印值
print(polyCubeDict.items())#打印键和值
```

```
import maya.cmds as mc
#创建一一对应列表
attrList = ['translateX','translateY','translateZ','rotateX','rotateY','rotateZ','scaleX','scaleY','scaleZ']
attrVal = [1.046,1.712,3.438,-14.464,15.652,50.186,1,1,1]
#将两个列表压缩成一一对应的元组列表
zipList = zip(attrList,attrVal)
#将一一对应的元组列表生成字典
data = dict(zipList)

import json
#设置保存路径和写入的变量
path = r'C:\Users\tianc\Documents\maya\2020\prefs\scripts\pSphere1.json'
jsonData = json.dumps(data)
#写入
with open(path,'w') as f:
	f.write(jsonData)
#读取
with open(path,'r') as f:
	sourceData = f.read()
#编码为maya可用
targetData = json.JSONDecoder().decode(sourceData)
#字典循环使用方法
for key,value in targetData.items():
	print(key,value)
```

# 1.7for循环

```
myStr = "hello world!"
for letter in myStr:
    print("the letter is:")
    print(letter)
print("the end")
```

```
myInt = [3,1,9,7,4,6]
for i in range(len(myInt)):
    print(myInt[i])
```

```
import pymel.core as pm
selList = pm.ls(sl=True)
for i in range(len(selList)):
    pos = selList[i].getTranslation()
    selList[i].setTranslation([pos.x,pos.y + i,pos.z])
print(selList)
```

```
polyCubeDict = {
    'name':'cube1',
    'position':[0.1,5.2,3.7],
    'points':8,
    'edges':12,
    'faces':6,
    'material':'lambert1'
    } 
for k, v in polyCubeDict.items():
    print("key:{},value:{}".format(k,v))
```

```

import maya.cmds as mc

obj = cmds.ls(sl=True)
objAttr = ['translate','rotate','scale']

#方法1
attValList = []
for att in objAttr:
	attVal = mc.getAttr('{}.{}'.format(obj[0],att))
	attValList.append(attVal)
print(attValList)
	
#方法2
attValList = [mc.getAttr('{}.{}'.format(obj[0],att)) for att in objAttr]
print(attValList)
```

# 枚举循环

```
obj = pm.selected()
#枚举
for index,data in enumerate(obj):
	print(index,data)
```

# 1.8判断

```
a = 124
b = 124
if a > b:
    print("a>b")
elif a < b:
    print("a<b")
else:
    print("a=b")
```

```
age1 = 20
age2 = 17
if (age1 >= 18) and (age2 >= 18):
    print("OK")
else:
    print("No")
```

```
age1 = 20
age2 = 17
if (age1 >= 18) or (age2 >= 18):
    print("OK")
else:
    print("No")
```

```
polyCube = ['cube1',[0.1,5.2,3.7],8,12,6,'lambert1']
if "cube1" in polyCube:
    print("Find Item!")
else:
    print("Not Found!")
```

```
#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 例3：if语句多个条件
num = 9
if num >= 0 and num <= 10:    # 判断值是否在0~10之间
    print 'hello'
# 输出结果: hello
 
num = 10
if num < 0 or num > 10:    # 判断值是否在小于0或大于10
    print 'hello'
else:
    print 'undefine'
# 输出结果: undefine
 
num = 8
# 判断值是否在0~5或者10~15之间
if (num >= 0 and num <= 5) or (num >= 10 and num <= 15):    
    print 'hello'
else:
    print 'undefine'
# 输出结果: undefine
```

1.9判断案例

```
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

# 1.10while循环

```
correctPw = "123456"
inputPW = input("Input your password: ")
while inputPW != correctPw:
    print("Incorrect!!!")
    inputPW = input("Input your password: ")
print("Password correct")
```

```python
correctPw = "123456"
while True:
    inputPW = input("Input your password: ")
    if inputPW == correctPw:
        print("Password correct")
        break
    else:
        print("Incorrect!!!")
```

# 1.11函数

```python
def myfunc(name,age): #括号内为形参
    print("Hello! " + name)
    print(str(age) + " years old")
myfunc("Charles",18) #括号内为实参
```

```python
#范例2 return返回值
def maxNum(num1,num2):
    if num1 > num2:
        return num1
    else:
        return num2
c = maxNum(6,3)
print(c)
```

```
#lambda匿名函数
test = lambda x:x*x
a(9)

map(test,[1,2,3,4,5,6])

map(lambda x:x*x,[1,2,3,4,5,6])
```

# 1.12类

```python
#类 Class 面向对象 面向过程
class Player():
    def __init__(self,id,pos,speed,heal):
        self.Id = id
        self.Position = pos
        self.Speed = speed
        self.Health = heal
pl1 = Player("xiaoming", [1.2, 1.3, 2.5], 1.0, 100.0)
pl2 = Player("xiaohong", [1.0, 0.3, 7.5], 1.5, 100.0)
print(pl1.Id)
print(pl1.Position)
print(pl2.Id)
print(pl2.Position)
```

```python
class Human():
    def __init__(self,name,age,sex): #构造函数 初始化函数
        self.name = name #成员变量
        self.age = age
        self.sex = sex
    def info(self): #类方法，成员函数
        print("My name is {}, {} years old and I'm a {}".format(self.name, self.age, self.sex))
Xiaoming = Human("xiao ming", 17, "male") #实例化
Xiaohong = Human("xiao hong", 19, "female")
print(Xiaoming.name)
Xiaohong.info()
```

# 1.13模块和标准库

```python
import class02 as cl
HM1 = cl.Human("lao wang", 37, "male")
print(HM1.name)
cl.sayHello()
```

```python
from class02 import sayHello
sayHello()
```

# 2.1pymel

```python
import pymel.core as pm
import maya.cmds as mc

list1 = pm.ls(selection=True)
list2 = mc.ls(selection=True)

trans1 = list1[0].getTranslation()
trans2 = cmds.getAttr(list2[0]+".translate")

trans1 += trans1
trans2 += trans2

print(trans1)
print(trans2)

list1[0].setTranslation(trans1)
```

```python
import pymel.core as pm
selList = pm.ls(sl=True)
firstSel = selList[0]
mesh = firstSel.getChildren()
pos = firstSel.getTranslation()
firstSel.setTranslation([2,3,5])
```

# 2.4模型合并工具

```python
#模型合并工具
import pymel.core as pm
def main():
    selList = pm.ls(sl=True)
    lastSel = selList[-1]
    p = lastSel.getParent()
    #polyUnite合并模型
    a = pm.polyUnite(selList)[0]
    #设置父级
    a.setParent(p)
    #删除历史
    pm.delete(a,ch=True)
    #重命名
    a.rename("combMesh")
```

```python
import combine
reload(combine)
combine.main()
```

# 2.5获取选择的关键帧范围

```
import pymel.core as pm
pm.timeControl('timeControl1',q=1,range=1)
import pymel.core as pm


aPlayBackSliderPython = pm.mel.eval('$tmpVar=$gPlayBackSlider')
pm.timeControl(aPlayBackSliderPython,q=1,range=1)
```

# 2.6获取locator世界坐标并创建骨骼

```
loc = pm.spaceLocator()
posLoc = loc.getPivots(ws=True)[0]
ToeJnt = pm.joint(n='Toe_JNT',p=posLoc)
```

# 2.7窗口布局

```python
import pymel.core as pm

UI = pm.window(title="tool")
               
pm.columnLayout(columnAttach=('both', 5),
                rowSpacing=10,
                columnWidth=250,
                adj=True)
                
pm.button()
pm.button()
pm.button()

pm.rowLayout(nc=3,adj=2)

pm.button()
pm.button()
pm.button()


pm.showWindow(UI)
```

```python
import pymel.core as pm
#创建窗口
UI = pm.window(title="tool")
#创建布局和按钮变量
formL = pm.formLayout()
btA = pm.text(label="My Tools",h=30) #文本控件
btB = pm.iconTextScrollList( #复选框控件
    allowMultiSelection=True,
    append=("A","B","C","D","E")
    )
colLay = pm.columnLayout(adj=True,rs=5)
#创建按钮
pm.textField(text="Input") #输入控件
pm.floatSlider(min=0, max=100, value=0, step=1) #滑杆控件
pm.checkBox(label="OK") #确认勾选控件
#设置按钮父级
pm.setParent("..")
btC = pm.button(label="Do it!",h=50)
#创建布局
#attachForm：调整控件与边框的关系，
#attachControl：调整控件与控件关系
pm.formLayout(
    formL,edit=True,
    attachForm=[
        (btA,"top",5),(btA,"left",5),(btA,"right",5),
        (btB,"left",5),(btB,"bottom",5),
        (colLay,"right",5),
        (btC,"bottom",5),(btC,"right",5)
    ],
    attachControl=[
        (btB,"top",5,btA),
        (colLay,"top",5,btA),(colLay,"left",5,btB),
        (btC,"top",5,colLay),(btC,"left",5,btB)
    ]
)
#显示窗口
pm.showWindow(UI)
```