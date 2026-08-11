---
tags:
  - Maya
  - Python
  - Rigging
  - 开源库
---

# cymel 使用指南

> 本篇基于官方英文文档 [Introduction to cymel](https://ryusas.github.io/cymel/en/gettingstarted.html)（文档版本 **0.35.2026072800**）整理，并核对了 GitHub 仓库 [ryusas/cymel](https://github.com/ryusas/cymel)（MIT，最后提交 2026-07-28）的实际目录结构。
> 定位对比（cymel vs cmdx vs PyMEL 该选哪个）见 [cymel与cmdx对比](cymel%E4%B8%8Ecmdx%E5%AF%B9%E6%AF%94.md)；本篇只讲**怎么用**。

## 一、cymel 解决什么问题

cymel 是佐々木隆二（ryusas，日本资深绑定 TA）写的 Maya Python 包裹库，官方三条目标（见 [Why cymel?](https://ryusas.github.io/cymel/en/whycymel.html)）：

1. **比 MEL 更面向对象**
2. **比 API 更顺手**
3. **比 PyMEL 更轻更快**

心智模型几乎照搬 PyMEL（`PyNode` → `CyObject`），但砍掉了 PyMEL 的沉重部分。名字里的 `C` 是 `C++` 的 C —— 远期核心要换成 C++ 实现，目前是纯 Python 的 preview 版，Python 版会长期保留并可随时切换。

明确的**不做**清单（写工具前必须知道）：

- **不包裹 cmds 命令**：需要 `polyCube`、`skinCluster` 之类仍然直接调 `cmds`
- **不支持组件（component）**：顶点、面、边、刷权重等操作要掉回 `cmds` / OpenMaya
- 不追求「给每个类塞满 API 等价功能」

同时它给了几条硬性行为保证，这点对发给动画师的工具很关键：

- 所有修改操作**保证可 undo**（包括通过 API 做的修改，见后文 `docmd`）
- 不改写 Maya 设置
- 不埋 `scriptJob` / `MMessage` 回调
- 设计上不持有 networked plug，也不推荐持有依赖 instance number 的 plug

## 二、安装

支持版本（[install](https://ryusas.github.io/cymel/en/installation.html)）：

| 实现 | 支持 Maya |
|---|---|
| Python 版（当前） | Maya 2015 及以后 |
| C++ 版（规划中） | Maya 2012 及以后 |

Maya 2022+ 的 Python 3 环境正常工作（Maya 2024 / Py3.10 实测可用）。

安装方式非常原始 —— **没有 PyPI 包**（`pip install cymel` 会 404，2026-08 核实）：

```bash
git clone https://github.com/ryusas/cymel.git
```

然后二选一：

1. 把仓库里的 `python` 目录加进 `PYTHONPATH`（该目录下只有一个 `cymel` 包 + 一个 `userSetup.py`）
2. 或者把 `python/cymel` 整个文件夹拷到已有的 Python 路径里（例如 `Documents/maya/scripts/`）

`cymel` 文件夹自带运行所需的全部文件，没有外部依赖。

### Maya 2022+ 的插件安全模式白名单

仓库里 `python/userSetup.py` 只做一件事：

```python
# Maya 2022+ UI 模式下，把 cymel 的插件路径加入 SafeModeAllowedlistPaths
try:
    import cymel.initmaya
    cymel.initmaya.addCymelPluginsPathToAllowedlist()
except:
    pass
```

cymel 自带插件（`cymel/plugins`，undo 支持等依赖它），2022 起的安全模式默认会拦下非白名单路径的插件。这个 `userSetup.py` 绕过了用户确认对话框直接加白名单 —— 官方也说明「如果觉得这种越权不合适，就别用这个 userSetup.py，规范做法是让每个用户自己在 UI 上放行」。团队统一部署时用它省事，个人洁癖就手动放行。

## 三、import 约定

三个入口模块：

| 模块 | 内容 |
|---|---|
| `cymel.main` | 除 UI 以外的全部功能 |
| `cymel.ui` | UI 相关功能 |
| `cymel.constants` | 极少量、适合展开到全局的常量 |

官方推荐写法：

```python
import cymel.main as cm
import cymel.ui as cmu
from cymel.constants import *
```

`cymel.constants` 的内容已经在 `cymel.main` 里展开过了，不想污染全局作用域就别 import 它（代价是要写 `cm.XYZ`、`cm.PI`）。

也可以一把梭：

```python
from cymel.all import *
```

`cymel.main` 里平铺展开了这些东西（读源码 `main.py` 确认）：

- 当前选择相关的 `sel` / `selection`
- `cymel.core` 全部（主要节点类、数据类型）
- `nt` —— `NodeTypes` 实例的别名，所有节点类的入口
- `cntm` —— Maya 新旧版本节点类型名兼容映射表
- `cymel.constants` / `cymel.pyutils` / `cymel.utils` / `cymel.initmaya` 全部

`cymel.constants` 里值得记住的几个（源码 `constants.py`）：

```python
PI                       # π
TO_DEG, TO_RAD           # 弧度/角度换算系数
XYZ YZX ZXY XZY YXZ ZYX  # rotateOrder 常量，值 0~5
AXIS_X AXIS_Y AXIS_Z     # 轴 ID 0/1/2
AXIS_NEG_X ...           # 负方向轴 ID（AXIS_NEG=0x10 加在轴 ID 上）
AVOID_ZERO_DIV_PRECISION # 1e-13，Maya 设 scale=0 时矩阵值实际只塌到 1e-12 左右，用它防除零
```

### standalone（mayapy）里的初始化

在 mayapy 里 import cymel 时，`cymel.initmaya` 会自动初始化 Maya。

> **和原生 `maya.standalone` 的差别**：原生 `initialize` 只调用 `userSetup.py`，**不调用 `userSetup.mel`**；cymel 的初始化把 `userSetup.mel` 也补上了。
>
> 另一方面，`import pymel.core` 做的事远超「启动 Maya UI」（比如自动加载一堆插件），cymel 刻意不走那么远，只做最低限度的事 —— 这就是它启动快的原因。

## 四、节点包裹类

### 4.1 拿到节点对象

cymel 为**所有**节点类型（含插件节点）提供包裹类，全部以 `CyObject` 为基类，并按节点类型树继承。

最省心的入口就是 `CyObject` 构造器（等价于 PyMEL 的 `PyNode`），别名 `O`：

```python
>>> cm.CyObject('persp')
Transform('persp')
>>> cm.O('persp')          # 别名，日常都用这个
Transform('persp')
```

取当前选择：

```python
>>> cmds.select(['persp', 'side'])
>>> cm.sel                 # 单个（多选时取第一个）
Transform('persp')
>>> cm.selobj(1)           # 按索引取
Transform('side')
>>> cm.selection           # 全部
[Transform('persp'), Transform('side')]
>>> cm.selected()          # pymel 风格，同上
[Transform('persp'), Transform('side')]
```

### 4.2 通过节点类操作

所有节点类都挂在 `cm.nt`（`NodeTypes` 实例）下，类名 = 节点类型名首字母大写。少数常用类也直接挂在 `cm` 上。

```python
>>> cm.nt.Joint
<class 'cymel.core.typeregistry.Joint'>
```

**不传已有节点名就是创建新节点**，关键字参数直接透传给 `createNode`：

```python
>>> cm.nt.Joint()
Joint('joint1')
>>> cm.nt.Joint(n='foo#')
Joint('foo1')
```

节点类同时是 `ls` 命令的包裹器（自动带上 `-type`，其他选项照常传）：

```python
>>> cm.nt.Joint.ls()
[Joint('foo1'), Joint('joint1')]
>>> cm.nt.Joint.ls('foo*')
[Joint('foo1')]
```

### 4.3 显式指定节点类拿对象

传已有节点名时，也可以直接指定具体类，而不用 `CyObject`：

```python
>>> cm.nt.Joint('foo1')
Joint('foo1')
>>> cm.nt.Transform('foo1')   # 指定兼容的父类也行，越抽象功能越少
Transform('foo1')
```

指定不兼容的类会报错（joint 是 transform 但不是 shape，所以给 `Shape` 会炸）。

日常还是 `cm.O()` 更省事也更可靠。显式指定类的用途有两个：用自定义节点类但不注册；或者**故意让它表现得更抽象**。例如 `DagNode` 派生类内部含 DAG path，同一节点的不同路径被视为不同对象；退化成 `Node` 就不含 path，因此相等：

```python
>>> cmds.file(f=True, new=True)
>>> cmds.polyCube()
[u'pCube1', u'polyCube1']
>>> cmds.instance()
[u'pCube2']
>>> cm.O('pCube1|pCubeShape1') == cm.O('pCube2|pCubeShape1')
False
>>> cm.Node('pCube1|pCubeShape1') == cm.Node('pCube2|pCubeShape1')
True
```

### 4.4 判断节点类型：别用 isinstance

看起来 `isinstance` 能用：

```python
>>> isinstance(cm.O('initialShadingGroup'), cm.nt.ObjectSet)
True
```

但因为**可以显式指定抽象类拿实例**，`isinstance` 就不可靠了：

```python
>>> isinstance(cm.nt.Node('initialShadingGroup'), cm.nt.ObjectSet)
False
```

这是设计阶段就明知并故意保留的取舍 —— 只要允许用户自由创建自定义节点类，「用 isinstance 判类型」这个前提就已经破了（PyMEL 同理）。

**可靠的做法是 `isType` 或 `hasFn`：**

```python
>>> cm.nt.Node('initialShadingGroup').isType('objectSet')
True
>>> cm.nt.Node('initialShadingGroup').hasFn(api.MFn.kSet)
True
```

`isinstance` 只在你真的想判断「是不是某派生类的实例」时才有意义（自定义节点类可以按节点类型之外的条件分派，这时才需要它）。

## 五、属性（Plug）包裹类

### 5.1 访问 plug

Plug 和 Node 一样是 `CyObject` 的派生类。直接当节点对象的成员访问，长短名都行：

```python
>>> cm.nt.Transform()
>>> cm.sel.t
Plug('transform1.t')
>>> cm.sel.translate
Plug('transform1.t')
```

和 MEL 命令一样，可以从 transform 直接访问 shape 的属性：

```python
>>> cm.O('persp').focalLength
Plug('perspShape.fl')
```

属性名和 Python 关键字或节点方法名撞车时，用 `plug()` 方法：

```python
>>> cm.sel.plug('t')
Plug('transform1.t')
```

复合属性的子属性可以逐层取，也可以直接从节点取：

```python
>>> cm.sel.t.tx
Plug('transform1.tx')
>>> cm.sel.tx      # 等价
Plug('transform1.tx')
```

### 5.2 坑：compound multi 直接取子 plug 会得到未解析索引

```python
>>> cmds.polyCube()
>>> cmds.select(cm.sel.shape())
>>> cm.sel.gcl
Plug('pCubeShape1.iog[-1].og[-1].gcl')     # -1 = 索引未解析
```

这种复杂情形要**逐层下钻并把 multi 索引写清楚**：

```python
>>> cm.sel.iog[0].og[0].gcl
Plug('pCubeShape1.iog[0].og[0].gcl')
```

其它等价写法：

```python
>>> cm.sel.plug('iog[0].og[0].gcl')
>>> cm.O('pCubeShape1.iog[0].og[0].gcl')
>>> cm.O('.iog[0].og[0].gcl')              # 省略节点名 = 用当前选择
```

### 5.3 取值 / 设值：注意是内部单位

```python
>>> cm.sel.t.get()
[0.0, 0.0, 0.0]
>>> cm.sel.t.set([1, 2, 3])
>>> cm.sel.t.get()
[1.0, 2.0, 3.0]
```

> **最重要的坑**：`set` / `get` 对带单位的类型一律按 **内部单位** 处理。

| 类型 | 属性类型 | 内部单位 |
|---|---|---|
| 距离 | `doubleLinear` | **厘米** |
| 角度 | `doubleAngle` | **弧度** |
| 时间 | `time` | **秒** |

所以 rotate 是弧度：

```python
>>> cm.sel.rx.set(PI * .5)
>>> cm.sel.rx.get()
1.5707963267948966
```

设计理由是「编程应当与场景设置（单位）无关」。确实想用 **UI 设置单位**，用 `setu` / `getu`：

```python
>>> cm.sel.rx.getu()
90.0
>>> cm.sel.rx.setu(180)
>>> cm.sel.rx.get()
3.141592653589793
```

官方建议：`setu` / `getu` 只用于在 Script Editor 里敲两行看结果的即兴脚本，**正式工具里一律用内部单位**。

### 5.4 编辑连接

连接用 `>>`、`<<` 或 `connect` 方法；查连接用 Node / Plug 的 `inputs` / `outputs`：

```python
>>> a = cm.nt.Transform(n='a')
>>> b = cm.nt.Transform(n='b')
>>> a.t >> b.t
>>> a.t.isSource(), a.t.isDestination()
(True, False)
>>> b.t.isSource(), b.t.isDestination()
(False, True)
>>> b.inputs(asPair=True)
[(Plug('b.t'), Plug('a.t'))]
```

> **注意**：`connect` 方法的参数顺序**和 pymel 相反**（cymel 是 `目标.connect(源)`），这是为了和 `disconnect` 的顺序统一。因此官方推荐**优先用 `<<` 而不是 `>>`**。

```python
>>> b.r.connect(a.r)   # 等价于 b.r << a.r
>>> b.r.inputs()
[Plug('a.r')]
>>> b.s << a.s
```

断开用 `//` 或 `disconnect`：

```python
>>> a.t // b.t         # 和 pymel 一样是「从左断到右」
>>> b.r.disconnect(a.s)
>>> b.s.disconnect()   # 输入 plug 可省略
```

由于 `//` 的方向和 `<<` 相反，一致性上更推荐 `disconnect` 方法。

### 5.5 world space plug：不要写索引

有些属性是输出世界空间值的 multi 属性（`Plug.isWorldSpace` 返回 `True`），例如 dagNode 的 `worldMatrix (wm)`、locator 的 `worldPosition (wp)`。

这类 plug 的索引取决于 DAG 节点的 instance 数量，而 instance 编号是**动态变化**的（删掉一个 instance 会自动补号）。因此 MEL 命令里也不推荐直连带索引的世界空间 plug —— Maya 会自动补上与 DAG path 一致的索引。cymel 沿用这个规范：**世界空间 plug 不要当作 multi 元素来用**。

```python
>>> a = cm.nt.Locator(n='a').transform()
>>> b = cm.O(cmds.instance(a)[0])
>>> a.t.set([1, 2, 3])
>>> b.t.set([4, 5, 6])
>>> a.wp.get()          # 推荐：不写索引
[1.0, 2.0, 3.0]
>>> b.wp.get()
[4.0, 5.0, 6.0]
>>> a.wp[0].get()       # 能用，但不推荐
[1.0, 2.0, 3.0]
>>> b.wp[1].get()
[4.0, 5.0, 6.0]
```

## 六、和命令 / API 混用

cymel 不像 PyMEL 那样包裹所有 Maya 命令，也不打算完整替代 API 或命令，更不包裹组件。它只提供「处理节点和 plug」的核心功能，**其余部分请配合 cmds 和 API 使用**。

衔接方式：

- `CyObject` 求值为字符串就是节点名 → **可以直接作为参数传给 cmds 命令**
- 命令返回值用 `O` / `Os` 接住 → 立刻变成 `Node` / `Plug`
- 拿等价的 API 对象：

| 方法 | 得到 |
|---|---|
| `Node.mnode` | API 2.0 的 `MObject` |
| `Node.mpath` | API 2.0 的 `MDagPath` |
| `Plug.mplug` | API 2.0 的 `MPlug` |
| `Node.mnode1` / `Node.mpath1` / `Plug.mplug1` | 对应的 API 1.0 版本 |

反过来，构造 `CyObject` 时除了名字，也可以传 API 2.0 的 `MObject` / `MDagPath` / `MPlug`（**API 1.0 的对象不支持**）。

## 七、数据类型（数学类）

cymel 的数学类是它最大的卖点 —— 作者是绑定 TA，这些类是按绑定痛点充实的。括号内是别名：

| 类 | 别名 | 对应 Maya API | 说明 |
|---|---|---|---|
| `BoundingBox` | `BB` | `MBoundingBox` | 包围盒 |
| `Vector` | `V` | `MPoint` + `MVector` | 三维向量（统一成一个类） |
| `Matrix` | `M` | `MMatrix` | 4x4 矩阵 |
| `Quaternion` | `Q` | `MQuaternion` | 四元数 |
| `EulerRotation` | `E` | `MEulerRotation` | 欧拉角旋转 |
| `Transformation` | `X` | `MTransformationMatrix`（更完善） | 变换信息 |

其中一部分可以直接作为 Plug 的值 set / get，类型之间也支持相互转换。

### 7.1 BoundingBox

用 `DagNode.boundingBox()` 取得；内部保存位置信息用的是 `Vector`。

### 7.2 Vector

API 里要按「表示位置还是方向」分用 `MPoint` / `MVector`，cymel **只有一个 `Vector`**。

`Vector` 像 `MPoint` 一样有齐次坐标的 `w`，但只要它是默认的 `1.0` 就被隐藏、基本不用管；当方向向量用时也不必置 0，方法会按语义正确处理。

```python
>>> cm.V(1, 2, 3) * cm.V(4, 5, 6)          # * 或 dot = 三维点积
32.0
>>> cm.V(1, 2, 3).dot(cm.V(4, 5, 6))
32.0
>>> cm.V(1, 2, 3).dot4(cm.V(4, 5, 6))      # 四维点积
33.0
>>> cm.V(1, 2, 3).dot4r(cm.V(4, 5, 6))     # 当作 4x1 · 1x4 的矩阵积
Matrix(((4, 5, 6, 1), (8, 10, 12, 2), (12, 15, 18, 3), (4, 5, 6, 1)))
>>> cm.V(1, 2, 3) ^ cm.V(4, 5, 6)          # ^ 或 cross = 三维叉积
Vector(-3.000000, 6.000000, -3.000000)
```

`w` 为默认 1.0 时，`Vector` 表现为长度 3 的序列 —— 当四维向量值用起来麻烦，当三维向量值用很顺手。所以能直接设给 `double3` 类型属性；get 回来是 list，包一层就是 Vector：

```python
>>> v = cm.V(1, 2, 3)
>>> cm.nt.Transform()
>>> cm.sel.t.set(v)
>>> v + cm.V(cm.sel.t.get())
Vector(2.000000, 4.000000, 6.000000)
```

### 7.3 Matrix

matrix 类型属性的 get / set 直接支持 `Matrix`，`DagNode` 也有 `getM` / `setM`。

```python
>>> a = cm.nt.Transform(n='a')
>>> a.t.set((1, 2, 3))
>>> a.r.setu((10, 20, 30))
>>> a.s.set((1.2, 1.4, 1.6))
>>> a.m.get()          # 从 plug 取局部矩阵
Matrix(((0.976557, 0.563816, -0.410424, 0), ..., (1, 2, 3, 1)))
>>> a.getM()           # 等价
Matrix(((0.976557, 0.563816, -0.410424, 0), ..., (1, 2, 3, 1)))
```

世界矩阵（记住 `wm` 不写索引）：

```python
>>> b = cm.nt.Transform(n='b', p=a)
>>> b.t.set((4, 5, 6))
>>> b.r.set((-10, -20, -30))
>>> b.wm.get()
>>> b.getM(ws=True)    # 等价
>>> c = cm.nt.Transform(n='c')
>>> c.setM(b.getM(ws=True))
```

矩阵乘法用 `*`，向量变换有两套：

```python
>>> b.m.get() * a.m.get()                  # 矩阵积
>>> m = c.getM()
>>> cm.V(1, 2, 3) * m                      # 位置变换（含平移）
Vector(8.375328, 14.068906, 10.691944)
>>> cm.V(1, 2, 3).xform4(m)                # 等价
Vector(8.375328, 14.068906, 10.691944)
>>> cm.V(1, 2, 3, 0) * m                   # 方向变换：手动把 w 置 0
Vector(2.922072, 3.462623, -0.692589, 0.000000)
>>> cm.V(1, 2, 3).xform3(m)                # 等价，但 w 保持默认 1.0
Vector(2.922072, 3.462623, -0.692589)
```

`Matrix` 到其他类型的转换（分解）：

| 方法 | 取出 |
|---|---|
| `asTM` / `asT` | 平移（矩阵形式 / 向量） |
| `asRM` / `asQ` / `asE` / `asD` | 旋转（矩阵 / 四元数 / 欧拉弧度 / 欧拉角度） |
| `asSM` / `asS` / `asSh` | 缩放、切变 |
| `asX` | 全部分解，得到 `Transformation` |

### 7.4 Quaternion

表现为长度 4 的序列。节点的 `getQ` 取旋转值：

```python
>>> a.getQ()
Quaternion(0.0381346, 0.189308, 0.239298, 0.951549)
>>> b.getQ(ws=True)
Quaternion(-0.691413, -0.473257, -0.399343, 0.372158)
>>> b.getQ() * a.getQ()       # * = 四元数积
Quaternion(-0.678253, -0.5056, -0.367246, 0.386616)
```

- `getQ` 默认**不含 `rotateAxis`**（但含 `jointOrient`；`ws=True` 时含上层变换）
- `getJOQ` 取**不含 `rotate`**（到 `jointOrient` 为止）的旋转。上例 b 是 transform 没有 jointOrient，所以等价于对父节点做 `getQ`
- `getQ(jo=False)` 可以排除 jointOrient

> **注意**：上例中 `b.getQ() * a.getQ()` 不等于 `b.getQ(ws=True)`，原因是 **a 有非等比缩放**。把 a 的 scale 归一后两者就相等了 —— 非等比缩放会破坏「局部四元数连乘 = 世界四元数」这个直觉，做空间切换/镜像工具时要当心。

转换：`Matrix.asQ` / `Quaternion.asM`、`EulerRotation.asQ` / `Quaternion.asE`、`asD`（角度制欧拉）、`asX`（→ Transformation）。

### 7.5 EulerRotation

带 `rotateOrder`，同时也表现为长度 3 的序列，因此很适合读写 `rotate` / `rotateAxis` / `jointOrient` 这类欧拉角属性。

```python
>>> cm.E(a.r.get(), a.ro.get())
EulerRotation(0.174533, 0.349066, 0.523599, XYZ)
>>> a.getQ(jo=False).asE()
EulerRotation(0.174533, 0.349066, 0.523599, XYZ)
>>> cm.degrot(10, 20, 30)          # 用角度制直接构造，非常常用
EulerRotation(0.174533, 0.349066, 0.523599, XYZ)
```

### 7.6 Transformation：比 MTransformationMatrix 更好用

Maya 的 matrix 类型属性能存两种格式：单纯的 **matrix**，或者 **transformation 信息**。对应 cymel 的 `Matrix` 和 `Transformation`。

`Transformation` 支持对 `Matrix` 的合成/分解，同时把「影响 transform / joint 局部矩阵的那些属性」当作自己的对象属性来处理。

> **关键差别**：把变换当 `Matrix` 处理会丢原始属性值（能分解出 translate/rotate/scale/shear，但 pivot、多重旋转属性之类无法完全还原）；当 `Transformation` 处理则**完整保留属性状态**。
>
> 例外：2020 起加入的 `offsetParentMatrix` 不算在局部矩阵里（被视作 `parentMatrix` 的一部分），因此**不是 `Transformation` 的对象属性**。

先造一个属性设得很细的节点：

```python
>>> a = cm.nt.Transform(n='a')
>>> a.t.set((1, 2, 3))
>>> a.rp.set((2, 3, 4))     # rotatePivot
>>> a.r.setu((10, 20, 30))
>>> a.ro.set(YXZ)           # rotateOrder
>>> a.ra.setu((3, 6, 9))    # rotateAxis
>>> a.sp.set((5, 6, 7))     # scalePivot
>>> a.s.set((1.2, 1.4, 1.6))
```

对比 `m` 和 `xm` 两个属性（都是 matrix 类型，但前者输出单纯矩阵，后者输出变换信息，cymel 都能原样取到）：

```python
>>> a.m.get()
Matrix(((0.784932, 0.76995, -0.480686, 0), ..., (0.260018, -1.52541, -0.437171, 1)))
>>> a.xm.get()
Transformation(rp=Vector(2, 3, 4), sp=Vector(5, 6, 7), sh=Vector(0, 0, 0),
               s=Vector(1.2, 1.4, 1.6), r=EulerRotation(0.185486, 0.343542, 0.586718, XYZ),
               ra=Quaternion(0.0219557, 0.0542077, 0.0769589, 0.995317), t=Vector(1, 2, 3))
```

含变换信息的属性也可以按单纯矩阵求值（就像 `getAttr` 那样）—— 显式用 `getM`，或取结果 `Transformation` 的 `m`：

```python
>>> a.xm.getM()
>>> a.xm.get().m
```

节点级用 `getX` / `setX`（`getX` 还能取世界空间值，这是 `xm` 属性做不到的）：

```python
>>> b = cm.nt.Transform(n='b', p=a)
>>> b.getX()
Transformation(s=..., sh=..., r=EulerRotation(-10, -20, -30, XYZ), t=Vector(4, 5, 6))
>>> b.getX(ws=True)
Transformation(q=Quaternion(...), s=Vector(1.567808, 1.300522, 1.318314),
               sh=Vector(0.047563, -0.101130, -0.171420), t=Vector(3.913720, 7.459003, 7.937241))
```

**`setM` 只对齐矩阵，`setX` 对齐每个 plug 值** —— 这是绑定工具里最实用的区别：

```python
>>> c = cm.nt.Transform(n='c')
>>> c.setM(a.getM())
>>> c.m.get().isEquivalent(a.m.get())          # 矩阵一致
True
>>> cm.V(c.t.get()).isEquivalent(cm.V(a.t.get()))   # 但 t / rp / r / ro / ra / sp 全不一致
False

>>> c.setX(a.getX())
>>> c.m.get() == a.m.get()      # 全部逐值相等，误差都没有，可以直接用 ==
True
>>> c.t.get() == a.t.get()      # t / rp / r / ro / ra / sp / s 同理，全 True
True
```

`Transformation` 还能**跨节点类型拷贝**（joint 和 transform 可用属性不同：joint 多了 `jointOrient` / `inverseScale`，但 pivot 不可改；shear 隐藏但可改 —— Maya 2019~2020.0 有过 shear 改不了的 bug，已修）。给 joint 设同一个 Transformation 时，可以看到 **pivot 保持不变，translate 被自动调整以对齐矩阵**：

```python
>>> d = cm.nt.Joint(n='d')
>>> d.setX(a.getX())
>>> d.m.get().isEquivalent(a.m.get())               # 矩阵一致
True
>>> cm.V(d.t.get()).isEquivalent(cm.V(a.t.get()))   # translate 被改过
False
>>> cm.V(d.rp.get()).isEquivalent(cm.V(a.rp.get())) # pivot 没跟着走（joint 不可改）
False
>>> cm.V(d.r.get()).isEquivalent(cm.V(a.r.get()))   # 旋转、rotateOrder、rotateAxis、scale 都对上了
True
```

### 7.7 用 Transformation 做矩阵分解

`Transformation` 不必从节点取，也可以当纯值构造：

```python
>>> cm.X(r=cm.degrot(10, 20, 30, YXZ), t=(1, 2, 3))
Transformation(r=EulerRotation(0.174533, 0.349066, 0.523599, YXZ), t=Vector(1, 2, 3))
>>> cm.X(q=cm.degrot(10, 20, 30, YXZ).asQ(), ro=YXZ, t=(1, 2, 3))   # 旋转也可以用四元数给
Transformation(q=Quaternion(0.0381346, 0.189308, 0.268536, 0.943714), ro=4, t=Vector(1, 2, 3))
```

直接把 `Matrix` 丢进构造器 = 调 `Matrix.asX()`，**这就是矩阵分解**：

```python
>>> r = cm.degrot(10, 20, 30, YXZ)
>>> m = r.asM() * cm.M.makeT((1, 2, 3))
>>> x = m.asX()          # 等价于 cm.X(m)
>>> x.t
Vector(1.000000, 2.000000, 3.000000)
>>> x.r
EulerRotation(0.185486, 0.343542, 0.586718, XYZ)
```

进阶用法：**先给定 pivot / jointOrient / rotateOrder 等辅助属性作为约束条件，再赋 matrix，让 cymel 反算出 t / r / q / s / sh**。这在写「把世界矩阵烘到带 jointOrient 和 pivot 的控制器上」这类工具时极其省事：

```python
>>> x = cm.X()
>>> x.rp = cm.V(2, 4, 6)
>>> x.jo = cm.degrot(5, 10, 15).asQ()
>>> x.ro = ZYX
>>> x.sp = cm.V(1, 2, 3)
>>> x.m  = m             # 最后再赋矩阵，触发反算
>>> x.t
Vector(0.865305, 2.632209, 2.573444)
>>> x.r
EulerRotation(-0.0165951, 0.207732, 0.291455, ZYX)
>>> x.q
Quaternion(0.00688977, 0.103775, 0.143573, 0.984159)
>>> x.s, x.sh
(Vector(1, 1, 1), Vector(0, 0, 0))
```

### 7.8 动态属性 + 数据类型

`Node.addAttr` 是 `addAttr` 命令的便捷包裹：

```python
>>> a = cm.nt.Transform(n='a')
>>> a.addAttr('testrot', 'double3', 'doubleAngle', cb=True)
>>> a.addAttr('foo', 'matrix')
>>> a.foo.get()          # None —— 数据类型属性初始值是 null
```

matrix 类型两种格式都能存：

```python
>>> a.foo.set(cm.M())
>>> a.foo.get()
Matrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
>>> a.foo.set(cm.X())
>>> a.foo.get()
Transformation(s=Vector(1, 1, 1), sh=Vector(0, 0, 0), r=EulerRotation(0, 0, 0, XYZ), t=Vector(0, 0, 0))
```

两个原生命令做不到、cymel 补上的能力（**都支持 undo**）：

```python
>>> a.foo.reset()                      # Plug.reset：回到默认值（这里是 null）
>>> a.foo.get()

>>> a.addAttr('bar', 'matrix', dv=cm.X())   # 原生命令只有数值属性能给默认值
>>> a.bar.get()
Transformation(...)
>>> a.bar.set(cm.M())
>>> a.bar.reset()
>>> a.bar.get()                        # 回到 Transformation 默认值
Transformation(...)
```

## 八、自定义类

### 8.1 自定义节点类（不注册，显式使用）

最简单的用法：继承对应节点类型的标准类，然后显式实例化。

```python
class MyTransform(cm.nt.Transform):
    def clearRestPose(self):
        self.mfn().clearRestPosition()

    def saveRestPose(self):
        self.mfn().setRestPosition(self.mfn().transformation())

    def gotoRestPose(self):
        mfn = self.mfn()
        r = mfn.restPosition()
        u = mfn.transformation()
        setx = mfn.setTransformation
        cm.docmd(lambda: setx(r), lambda: setx(u))   # 关键：让 API 修改也能 undo
```

这里用 `MFnTransform` 的 Rest Position 功能实现了「暂存当前姿势 / 回到该姿势」。该 API 特性只是 API 层的临时缓存，Maya 内部不用它，也不存进场景文件。**通常用 API 改场景是不能 undo 的，这里靠 cymel 的 `docmd`（传入 redo / undo 两个 lambda）拿回了 undo 支持** —— 这是 cymel 很值得抄的一个模式。

```python
>>> cmds.polyCube()
>>> obj = MyTransform(cmds.ls(sl=True)[0])
>>> obj.t.set((1, 2, 3)); obj.r.setu((10, 20, 30)); obj.s.set((2, 4, 6))
>>> obj.saveRestPose()
>>> obj.t.reset(); obj.r.reset(); obj.s.reset()
>>> obj.gotoRestPose()
>>> cmds.undo()
# Undo: obj.gotoRestPose() #
>>> cmds.redo()
# Redo: obj.gotoRestPose() #
```

**局限**：只有显式写 `MyTransform(...)` 才拿到自定义类。通过 `sel` / `selected`、或顺着父子层级 / 连接爬到的对象，永远是普通的 `Transform`。

### 8.2 注册带检查方法的节点类

要让 `sel` 等入口也自动返回自定义类，得用 `NodeTypes.registerNodeClass` 注册到 `cm.nt`。

问题是 `MyTransform` 继承的 `Transform` 已经对应 `transform` 节点类型 —— 直接注册就有两个类抢同一个类型。解决办法：**给节点打 tag，用 tag 区分同为 transform 类型的节点该不该用 `MyTransform`**。tag 形式随意，但通常用自定义属性最合适（能存进场景文件）。

类里加两个方法（这是 cymel 的约定规则）：

```python
class MyTransform(cm.nt.Transform):
    @staticmethod
    def _verifyNode(mfn, name):            # 必需：判断该节点是否属于本类
        return mfn.hasAttribute('myNodeTag')

    @classmethod
    def createNode(cls, **kwargs):         # 推荐：新建节点时自动打 tag
        nodename = super(MyTransform, cls).createNode(**kwargs)
        cmds.addAttr(nodename, ln='myNodeTag', at='message', h=True)
        return nodename

    # （前面已实现的方法继续保留）

cm.nt.registerNodeClass(MyTransform, 'transform')   # 第二参数 = 关联的节点类型名
```

- 只有检查方法 `_verifyNode` 是**必需**的，`createNode` 只是推荐
- 不实现 `_verifyNode` 就注册会报错，因为此时要求类继承关系和节点类型继承关系**严格一致**（Maya 里 transform 的父类型是 dagNode，所以类必须直接继承 `DagNode`）
- 反之，有检查方法的类关联就宽松了：只要不冲突，可以关联 `dagNode` 甚至 `node` 来覆盖大范围类型（那时继承的类也要相应换成 `DagNode` / `Node`；本例因为用了 `MFnTransform` 功能所以做不到）。也可以**多次调用 `registerNodeClass`** 绑定多个无继承关系的节点类型

注册后，不指定已有名字就走 `createNode`：

```python
>>> MyTransform()
# Result: MyTransform('myTransform1') #
>>> MyTransform(n='foo')
# Result: MyTransform('foo') #
>>> cm.sel                 # tag 已打上，普通入口也认得它了
# Result: MyTransform('foo') #
```

对**已经存在**的节点（比如先前建的 cube）还是不行，需要自己加个补 tag 的方法（这部分没有系统支持，随便怎么写）：

```python
class MyTransform(cm.nt.Transform):
    @classmethod
    def createNode(cls, **kwargs):
        nodename = super(MyTransform, cls).createNode(**kwargs)
        cls.addClassTag(nodename)
        return nodename

    @classmethod
    def addClassTag(cls, nodename):
        cmds.addAttr(nodename, ln='myNodeTag', at='message', h=True)

    # _verifyNode 等其余方法不变
```

```python
>>> MyTransform.addClassTag(cmds.polyCube()[0])
>>> cm.sel
# Result: MyTransform('pCube1') #
```

### 8.3 注册基础节点类（接管标准类）

cymel 为所有节点类型都提供了类，但**只有少数类真正实现了功能**，其余都是「首次访问时自动生成」的空壳，只为把节点类型层级映射成类层级。看类的出处就能区分：

```python
>>> cm.nt.DagNode
<class 'cymel.core.cyobjects.dagnode.DagNode'>      # 真实实现
>>> cm.nt.Transform
<class 'cymel.core.cyobjects.transform.Transform'>  # 真实实现
>>> cm.nt.Shape
<class 'cymel.core.cyobjects.shape.Shape'>          # 真实实现
>>> cm.nt.Joint
<class 'cymel.core.typeregistry.Joint'>             # 自动生成的空壳
>>> cm.nt.ObjectSet
<class 'cymel.core.typeregistry.ObjectSet'>         # 自动生成的空壳
```

自动生成的类都在 `cymel.core.typeregistry` 下（插件添加的节点类型同样如此，当然也没有专门功能）。**这些空壳可以自己实现掉。**

如果和节点类型是一对一关系，就**不需要** `_verifyNode` / `createNode`，直接 `registerNodeClass` 即可；但**类继承关系必须与真实节点类型层级严格一致**，用 `parentBasicNodeClass` 自动求解最省心：

```python
class ObjectSet(cm.nt.parentBasicNodeClass('objectSet')):
    def __contains__(self, item):
        return cmds.sets(item, im=self.name())

    def __len__(self):
        return cmds.sets(self.name(), q=True, s=True)

    def __getitem__(self, i):
        return cm.O(cmds.sets(self.name(), q=True, no=True)[i])

    def add(self, *items):
        cmds.sets(*items, add=self.name())

    def remove(self, *items):
        cmds.sets(*items, rm=self.name())

cm.nt.registerNodeClass(ObjectSet, 'objectSet')
```

> **坑**：如果该节点类型的类**已经被生成过**，会打印警告并覆盖注册：
>
> ```
> # Warning: node class deregistered: <class 'cymel.core.typeregistry.ObjectSet'> #
> ```
>
> 此时所有继承它的类会一并被注销。那些节点类型的类下次求值时会重新生成，但**已经创建出来的实例仍指向被注销的旧类**。因此**自定义类要尽早注册 —— Maya 启动后第一时间做**。

### 8.4 自定义 plug 类 / utility

官方文档标注为 **(under construction)**，暂无内容。

## 九、UI 控件类

cymel 包裹了所有 MEL UI 控件，类名 = MEL 命令名首字母大写（`window` → `Window`）。和 PyMEL 很像、演进不多（`with` 用起来更方便一点），用法基本相同：

```python
import cymel.ui as cmu

with cmu.Window() as wnd:
    with cmu.AutoLayout():
        cmu.Button(l='foo')
        cmu.Button(l='bar')
        cmu.Button(l='baz')
wnd.show()
```

（PySide 相关部分 cymel 不管；仓库另有 `cymel/qt` 提供 Qt 辅助。）

## 十、坑点速查

| # | 坑 | 对策 |
|---|---|---|
| 1 | `set` / `get` 用**内部单位**（cm / 弧度 / 秒），rotate 是弧度 | 正式工具用内部单位 + `PI` / `TO_RAD`；即兴脚本才用 `setu` / `getu` |
| 2 | `connect` 参数顺序**和 pymel 相反**（`目标.connect(源)`） | 统一用 `<<` 运算符；断开统一用 `disconnect` 方法（`//` 方向又是反的） |
| 3 | `isinstance` **判不出节点类型**（可显式取抽象类实例） | 用 `isType('nodeType')` 或 `hasFn(api.MFn.kXxx)` |
| 4 | compound multi 直接取子 plug 得到 `iog[-1].og[-1]`（索引未解析） | 逐层下钻写明索引：`node.iog[0].og[0].gcl` |
| 5 | world space plug（`wm` / `wp`）的索引随 instance 动态变化 | **不要写索引**，直接 `a.wm.get()` / `getM(ws=True)` |
| 6 | `setM` 只对齐矩阵，pivot / rotateOrder / rotateAxis 全丢 | 要完整复制属性状态就用 `getX` / `setX`（`Transformation`） |
| 7 | 非等比缩放下「局部四元数连乘 ≠ 世界四元数」 | 做空间切换 / 镜像前检查 scale；必要时走矩阵而非四元数 |
| 8 | `offsetParentMatrix`（2020+）不属于 `Transformation` | 它被算进 `parentMatrix`，需单独处理 |
| 9 | 数据类型属性（matrix 等）初始值是 **null**，`get()` 返回 `None` | 先 `set` 或 `addAttr(..., dv=...)` 给默认值 |
| 10 | 覆盖注册已生成的节点类会注销其所有子类，且旧实例仍指向旧类 | 自定义类在 Maya 启动后**尽早注册** |
| 11 | **不支持组件**，也不包裹 cmds 命令 | 刷权重、顶点级操作掉回 `cmds` / OpenMaya；`CyObject` 可直接当名字传给 cmds |
| 12 | **没有 PyPI 包**，`pip install cymel` 会 404 | clone 仓库，把 `python/` 加进 PYTHONPATH 或拷 `python/cymel` 到 scripts |
| 13 | Maya 2022+ 安全模式会拦 cymel 自带插件 | 用仓库的 `userSetup.py` 调 `initmaya.addCymelPluginsPathToAllowedlist()`，或手动在 UI 放行 |

## 相关

- [cymel与cmdx对比](cymel%E4%B8%8Ecmdx%E5%AF%B9%E6%AF%94.md) —— 选型层面的对比（哲学、性能、体量），本篇是它的 API 使用篇
- [什么是API，何时使用API](%E4%BB%80%E4%B9%88%E6%98%AFAPI%EF%BC%8C%E4%BD%95%E6%97%B6%E4%BD%BF%E7%94%A8API.md) —— cymel 定位在 cmds 与 OpenMaya 之间，该篇讲何时该往下掉一层
- [基于矩阵运算的父约束](%E5%9F%BA%E4%BA%8E%E7%9F%A9%E9%98%B5%E8%BF%90%E7%AE%97%E7%9A%84%E7%88%B6%E7%BA%A6%E6%9D%9F.md) —— 用 cymel 的 `Matrix` / `Transformation` 实现会显著简化

## 参考链接

- 官方文档：[English](https://ryusas.github.io/cymel/en/index.html) / [日本語](https://ryusas.github.io/cymel/ja/index.html)
- 本篇主要来源：[Introduction to cymel](https://ryusas.github.io/cymel/en/gettingstarted.html)
- [install](https://ryusas.github.io/cymel/en/installation.html) / [Why cymel?](https://ryusas.github.io/cymel/en/whycymel.html) / [Module reference manual](https://ryusas.github.io/cymel/en/modules.html)
- 仓库：https://github.com/ryusas/cymel （MIT）
