1.导入模块

```python
from maya.cmds import *
polySphere()
```

```python
import maya.cmds as mc
mc.polySphere()
```

```python
from maya.cmds import polySphere as ps
ps()
```

2.命令结构

```python
from maya.cmds import parentConstraint
parentConstraint('pCube1','pSphere1',mo=True,weight=1)
```

2.5

```python
#定义数组
test_list=[1,2,3,4,5,6,7,8,9]
#末尾添加
test_list.append(10)
#在某位插入
test_list.insert(0,0)
#移除某数
test_list.remove(5)
#移除某位
test_list.pop(0)
#数组大小排序
test_list.sort()
#显示数组内容
test_list[2]
#test_list[开始:结束:步长]
test_list[0:4:2]
#原组，无法修改
test_tuple=(1,2,3)
```

2.6字典

```
#字典
test_dict={'a':1,'b':'abs'}
#查询a键的值
test_dict['a']

#查询键是否在字典中
'a' in test_dict
'w' in test_dict
#查询键列表和值列表
test_dict.keys()
test_dict.values()
```

```
#集合
test_set1={0,1}
test_set2={1,2}
#在前方添加
test_set1.add(-1)
#移除
test_set1.remove(-1)
#取交集
test_set1 & test_set2
#取并集
test_set1 | test_set2
```

2.7条件语句

```
val = 5
if val ==0:
    print 0
elif val == 1:
    print 1
else:
    print 'error'
```

```
if 'abc' in 'abcd':
    print True
else:
    print False
```

2.8循环语句

```python
'''for i in 字符串，列表，元组，字典，集合...:
    执行语句
'''
#列表
for i in [0,1,2,3,4,5]:
    print i
#字符串   
for i in 'abcde':
    print i    
#字典打印键    
for i in {'a':1,'b':2,'c':3}:
    print i
#字典打印值
test_dict = {'a':1,'b':2,'c':3}
for i in test_dict:
    print test_dict[i]  
```

```
import maya.cmds as cm
list_a = cm.ls(sl = True)
list_b = cm.ls(sl = True)
print list_a
print list_b
print zip(list_a,list_b)

#len查询有多少个，range列出每一个
for i in range(len(list_a)):
    print list_a[i]
    print list_b[i]
    
#设置i,t两个变量分别替代list_a和list_b    
for i,t in zip(list_a,list_b):
    print i
    print t
```

2.9函数

```
import maya.cmds as mc
def printselect():
    lis_obj = mc.ls(sl = True)
    for i in lis_obj:
        print i
        
printselect()
```

2.10字符串操作

```
#声明字符串变量
test_str = 'a_b_c_d'
#分割字符串
test_str.split('_')
#创建字符串变量
list_str = test_str.split('_')
#组合成一个字符串
''.join(list_str)
#组合字符串时插入内容
'|'.join(list_str)
#搜索并替换字符串
test_str.replace('_','|')
#拆分字符串
test_str[0:6]
test_str[::-1]
#查询字符串
test_str.find('d')
test_str.rfind('c')
```

2.11常用函数

```
#类型
bool() #布尔型
int() #整形
str() #字符型
tuple() #元组型
dict() #字典型
list() #列表型
float() #浮点型
set() # 集合类型
#......
#数据
abs() #绝对值
min() #最小
max() #最大
len() #参数元素个数
#查询
type() #返回实例的类型
help() #查询帮助
dir() #查询内容
#其他
hash() # 返回对象的哈希码
id() #返回一个对象的标识
exec() #动态执行Python代码
callable() #判断对象是否可调用
format() #对象格式化为字符串
```

2.12常用命令

```
import maya.cmds as cmds
#列出选定对象
cmds.ls(sl=True,fl=False)
#设置位移
cmds.xform('pSphere1',t=(1,1,1))
#查询位移，旋转，缩放
cmds.xform('pSphere1',q=True,t=True)
cmds.xform('pSphere1',q=True,ro=True)
cmds.xform('pSphere1',q=True,s=True)
#获取属性，设置属性
cmds.getAttr('pSphere1.t')
cmds.setAttr('pSphere1.t',1,2,3)
#查询子物体
cmds.listRelatives('group1',c=True)
#查询父物体
cmds.listRelatives('group1',p=True)
#查询两个子物体
cmds.listRelatives('group1',ad=True)
#查询物体形节点
cmds.listRelatives('pSphere1',s=True)
#查询输入连接
cmds.listConnections('pSphere1')
#查询是否存在
cmds.objExists('pSphere1')
#查询对象类型
cmds.objectType('pSphereShape1')
#执行mel命令
mel.eval('select -r pSphere1;')
```

2.13传递点位置工具范例

```
import maya.cmds as mc
def set_vtx():
    in_mesh,out_mesh = mc.ls(sl=True)
    in_mesh_vtx = mc.ls('%s.vtx[*]'%in_mesh,fl=True)
    out_mesh_vtx = mc.ls('%s.vtx[*]'%out_mesh,fl=True)
    for i,t in zip(in_mesh_vtx,out_mesh_vtx):
        pos = mc.xform(i,q=True,t=True)
        mc.xform(t,t=pos)
set_vtx()
```

```
import pymel.core as pm
in_node,out_node = pm.selected()
out_node.setPoints(in_node.getPoints())
```

3.3窗口

```
import maya.cmds as cmds

window = cmds.window( title="Long Name", iconName='Short Name', widthHeight=(200, 55) )
cmds.columnLayout( adjustableColumn=True )
cmds.button( label='Do Nothing' )
cmds.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') )
cmds.setParent( '..' )
cmds.showWindow( window )
```