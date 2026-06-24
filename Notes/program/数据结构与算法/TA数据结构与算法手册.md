# 游戏动画绑定 TA · 数据结构与算法手册

> 写给绑定 / 动画方向技术美术的实战手册。
> 这里不讲红黑树怎么旋转、不背八大排序——讲的是**你每天在 Maya/UE 里真正会碰到的层级、矩阵、几何与数值求解**。
> 技术栈假设:Python 3.11 · Maya(cmds / OpenMaya) · UE5(ChaosCloth / Dynamic Animation)。

---

## 目录

**第一部分:数据结构(地基)**
1. [树与层级 Hierarchy](#1-树与层级-hierarchy)
2. [DAG 与 DG:Maya 的两张图](#2-dag-与-dgmaya-的两张图)
3. [数组与矩阵:NumPy 向量化](#3-数组与矩阵numpy-向量化)
4. [哈希表 / 字典](#4-哈希表--字典)

**第二部分:核心算法(日常)**
5. [图遍历:DFS / BFS](#5-图遍历dfs--bfs)
6. [拓扑排序](#6-拓扑排序)
7. [线性代数:变换数学](#7-线性代数变换数学)
8. [四元数与旋转插值](#8-四元数与旋转插值)
9. [插值与样条曲线](#9-插值与样条曲线)

**第三部分:进阶算法(造工具)**
10. [IK 求解](#10-ik-求解)
11. [蒙皮算法:LBS / DQS](#11-蒙皮算法lbs--dqs)
12. [最小二乘与数值优化](#12-最小二乘与数值优化)
13. [空间加速结构:KD-tree / BVH / 八叉树](#13-空间加速结构kd-tree--bvh--八叉树)
14. [物理积分与约束求解:Verlet / PBD](#14-物理积分与约束求解verlet--pbd)
15. [RBF 散点插值:PSD / 修形驱动](#15-rbf-散点插值psd--修形驱动)
16. [重心坐标 Barycentric](#16-重心坐标-barycentric)

**附录**
- [A. 复杂度速查](#附录-a-复杂度速查)
- [B. 学习路径](#附录-b-学习路径)
- [C. TA 专属踩坑清单](#附录-c-ta-专属踩坑清单)

---

# 第一部分:数据结构(地基)

## 1. 树与层级 Hierarchy

### 是什么
**树**是没有环的连接结构:一个根(root),每个节点有 0 或 1 个父、任意多个子。绑定的整个世界观就是一棵树。

```
root
└─ pelvis
   ├─ spine_01
   │  └─ spine_02
   │     └─ head
   ├─ leg_L
   └─ leg_R
```

### 为什么对你重要
- **骨骼层级**、**Outliner**、**变换父子关系**全是树。
- 子节点的世界变换 = 自身局部变换 × 父链上所有变换的累积。**父动则子动**,本质就是树的传播。
- 90% 的绑定脚本第一步都是"拿到某个根,遍历它的子树"。

### 代码示例:遍历骨骼层级
```python
import maya.cmds as cmds

def iter_hierarchy(root):
    """深度优先生成整棵子树的全路径名"""
    yield root
    children = cmds.listRelatives(root, children=True,
                                  type='transform', fullPath=True) or []
    for child in children:
        yield from iter_hierarchy(child)   # 递归 = 树遍历的天然写法

# 用法:统计某根骨骼下所有 joint
joints = [n for n in iter_hierarchy('|root') if cmds.objectType(n) == 'joint']
print(f"子树共 {len(joints)} 根骨骼")
```

### 踩坑提醒
- **同名节点**:Maya 允许不同层级下重名,所以脚本里**永远用全路径(`fullPath=True`)** 作为唯一标识,短名会咬你。
- **递归深度**:正常骨架几十层没问题,但对超大场景层级别用纯递归(Python 默认递归上限 1000),改用下一节的显式栈/队列。

---

## 2. DAG 与 DG:Maya 的两张图

Maya 里有**两张不同的图**,新人最容易混。理解它们的区别,是从"会点按钮"到"懂 Maya 怎么运转"的分水岭。

### DAG(有向无环图,Directed Acyclic Graph)
- 管的是**空间层级**:谁是谁的父、变换怎么继承、形状(shape)挂在哪个变换(transform)下。
- 它是"树"的超集——因为 Maya 的**实例(instance)** 允许一个节点有多个父,所以严格说是 DAG 而非纯树。
- 关键约束:**无环**。A 不能既是 B 的祖先又是 B 的后代,否则变换无法求值。

### DG(依赖图,Dependency Graph)
- 管的是**数据流与求值**:节点的属性(attribute)通过连接(connection)互相驱动。
- 你连的每一条 `connectAttr`、每个约束、每个变形器,都是在 DG 里加边。
- DAG 节点其实是 DG 节点的**子类**——变换节点既在空间层级里,也在数据流里。

```
DAG(空间):  pelvis ── spine ── head        (父子关系)

DG(数据流):  multMatrix.output ──► joint.offsetParentMatrix
             curveInfo.arcLength ──► stretchNode.input   (属性连接)
```

### 为什么对你重要
- **"为什么这个属性不刷新?"** —— 几乎都是 DG 求值顺序或脏标记(dirty propagation)问题。
- 自己做**节点式工具**(重定向、程序化绑定、自定义变形)时,你就是在编织 DG。
- 理解 DAG/DG 分离,才明白为什么 `parent` 和 `connectAttr` 是两回事。

### 代码示例:遍历 DG 上游(找某属性的数据来源)
```python
import maya.cmds as cmds

def trace_upstream(plug, depth=0):
    """逆着连接往上游走,看一个属性的数据是谁喂进来的"""
    print("  " * depth + plug)
    sources = cmds.listConnections(plug, source=True, destination=False,
                                   plugs=True) or []
    for s in sources:
        trace_upstream(s, depth + 1)

# 例:看某 joint 的平移到底被什么驱动
trace_upstream('joint1.translateX')
```

### 踩坑提醒
- **环**:DG 里如果连出循环(cycle),Maya 会报 cycle warning 且求值结果不可靠。约束互相驱动时最常见。
- **求值模式**:Maya 有 DG / Parallel 两种求值模式,Parallel 下脏传播行为不同,做高性能绑定时要留意。

---

## 3. 数组与矩阵:NumPy 向量化

### 是什么
- **数组**:连续内存里的同类型元素,`O(1)` 随机访问。
- **矩阵**:二维数组;在绑定里它几乎总是指**4×4 变换矩阵**或 **N×3 顶点表**。

### 为什么对你重要
处理几何 = 处理**成千上万个顶点**。用 Python 原生 `for` 循环逐点算,会慢到无法接受;**NumPy 向量化**能快 1~2 个数量级。

### 代码示例:逐点循环 vs 向量化
```python
import numpy as np

# 假设 10 万个顶点,要整体平移 + 缩放
verts = np.random.rand(100_000, 3).astype(np.float64)

# ❌ 慢:Python 层逐点循环
def slow(verts):
    out = []
    for v in verts:
        out.append([(v[0] + 1) * 2, (v[1] + 1) * 2, (v[2] + 1) * 2])
    return out

# ✅ 快:整块向量化,底层走 C / SIMD
def fast(verts):
    return (verts + 1.0) * 2.0

# fast 通常比 slow 快几十倍
```

### 代码示例:把顶点批量乘上一个变换矩阵
```python
import numpy as np

def transform_points(points, matrix4x4):
    """points: (N,3);matrix4x4: (4,4) 行主序。返回 (N,3)"""
    n = points.shape[0]
    # 升到齐次坐标 (N,4),最后一列填 1
    homo = np.hstack([points, np.ones((n, 1))])
    # 行向量约定:p' = p · M
    out = homo @ matrix4x4
    return out[:, :3]    # 丢掉 w 分量
```

### 踩坑提醒
- **主序(row-major vs column-major)是头号大坑**:Maya / OpenMaya 用**行主序、行向量**(`v * M`),很多数学库 / 教科书用**列主序、列向量**(`M * v`)。两者矩阵互为转置。跨库搬数据(比如喂给 `py-dem-bones`、对接 UE)时,**先确认主序约定**,否则旋转会莫名其妙地转错方向。
- **拷贝 vs 视图**:NumPy 切片是视图(共享内存),改它会改原数组。需要独立数据用 `.copy()`。
- **dtype**:Maya 给的点数据常是 float;和 float64 混算会有精度/性能问题,统一 dtype。

---

## 4. 哈希表 / 字典

### 是什么
键→值的映射,平均 `O(1)` 查找/插入。Python 的 `dict` 和 `set` 就是。

### 为什么对你重要
- **名字 → 节点对象**的映射:重定向时把源骨架名映射到目标骨架名。
- **缓存**:权重表、矩阵缓存,避免重复查询 Maya(查询 Maya 很慢)。
- **去重**:`set` 判断顶点/节点是否已处理。

### 代码示例:骨骼重定向映射表
```python
# 源骨架 → 目标骨架 的名字映射,O(1) 查
RETARGET_MAP = {
    "mixamorig:Hips":     "pelvis",
    "mixamorig:Spine":    "spine_01",
    "mixamorig:Head":     "head",
    # ...
}

def retarget_name(src):
    return RETARGET_MAP.get(src)   # 查不到返回 None,而不是报错
```

### 代码示例:用字典缓存昂贵查询
```python
import maya.cmds as cmds

_skin_cache = {}
def get_skincluster(mesh):
    """查 mesh 的 skinCluster,带缓存——避免重复遍历历史"""
    if mesh not in _skin_cache:
        history = cmds.listHistory(mesh) or []
        sc = cmds.ls(history, type='skinCluster')
        _skin_cache[mesh] = sc[0] if sc else None
    return _skin_cache[mesh]
```

### 踩坑提醒
- 字典查询是 `O(1)`,但**查询 Maya 本身很慢**——能缓存就缓存,批处理时尤其明显。
- 键必须可哈希:别拿 NumPy 数组当键,用 `tuple` 或字符串。

---

# 第二部分:核心算法(日常)

## 5. 图遍历:DFS / BFS

### 是什么
- **DFS(深度优先)**:一条路走到黑再回头。用**栈**(或递归)。
- **BFS(广度优先)**:一层一层向外扩。用**队列**。

```
       A
      / \         DFS 顺序: A B D E C F
     B   C        BFS 顺序: A B C D E F
    / \   \
   D   E   F
```

### 为什么对你重要
绑定脚本里出现频率最高的算法。"收集子层级""找根""按层处理"全是它。

### 代码示例:显式栈 DFS(避免递归深度限制)
```python
import maya.cmds as cmds

def dfs_iterative(root):
    """用显式栈做 DFS,适合超深层级"""
    stack = [root]
    while stack:
        node = stack.pop()           # 栈:后进先出 → 深度优先
        yield node
        children = cmds.listRelatives(node, children=True,
                                      type='transform', fullPath=True) or []
        stack.extend(reversed(children))   # reversed 保持从左到右的视觉顺序
```

### 代码示例:BFS 按层处理
```python
from collections import deque
import maya.cmds as cmds

def bfs(root):
    """队列:先进先出 → 一层层向外。适合'离根越近越先处理'的需求"""
    queue = deque([root])
    while queue:
        node = queue.popleft()
        yield node
        children = cmds.listRelatives(node, children=True,
                                      type='transform', fullPath=True) or []
        queue.extend(children)
```

### 何时用哪个
| 需求 | 选择 |
|------|------|
| 收集整棵子树、深度无所谓 | DFS(递归最省事) |
| 按"离根的距离"分层(如逐级烘焙父矩阵) | BFS |
| 层级极深、怕爆栈 | 显式栈 DFS |

---

## 6. 拓扑排序

### 是什么
对**有向无环图**的节点排个线性顺序,使得**每条边都从前指向后**——即"先算依赖,再算被依赖的"。

### 为什么对你重要
- **DG 求值顺序**的本质:Maya 必须先算上游节点,才能算下游。
- 你做**自定义节点式工具**(批量构建驱动关系、烘焙)时,要自己确定"先处理谁"。
- 父矩阵必须在子矩阵之前算好 —— 这就是按拓扑序(从根到叶)处理。

### 代码示例:Kahn 算法
```python
from collections import deque, defaultdict

def topo_sort(nodes, edges):
    """
    nodes: 节点列表
    edges: [(a, b), ...] 表示 a 必须在 b 之前(a 是 b 的依赖)
    返回:满足依赖的线性顺序;若有环则抛错
    """
    graph = defaultdict(list)
    indeg = {n: 0 for n in nodes}
    for a, b in edges:
        graph[a].append(b)
        indeg[b] += 1

    # 入度为 0 的(无依赖的)先入队
    queue = deque([n for n in nodes if indeg[n] == 0])
    order = []
    while queue:
        n = queue.popleft()
        order.append(n)
        for m in graph[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                queue.append(m)

    if len(order) != len(nodes):
        raise ValueError("图里有环,无法拓扑排序(检查循环依赖)")
    return order
```

### 踩坑提醒
- **检测到环 = 你的 DG 里有循环依赖**,正是 Maya 报 cycle warning 的场景。拓扑排序天然能帮你定位它。

---

## 7. 线性代数:变换数学

> **如果这本手册只让你精通一章,就是这一章。** 绑定 TA 的天花板,基本由矩阵功底决定。

### 4×4 变换矩阵的结构
一个 4×4 矩阵同时编码了**旋转、缩放、平移**(行主序 / 行向量约定下):

```
| Rxx Rxy Rxz 0 |   ← 上 3×3 是旋转+缩放
| Ryx Ryy Ryz 0 |
| Rzx Rzy Rzz 0 |
| Tx  Ty  Tz  1 |   ← 最后一行是平移
```

### TRS 组合顺序
变换的**乘法顺序决定结果**,且不可交换(`A·B ≠ B·A`)。Maya 行向量约定下:

```
M = Scale · Rotate · Translate      # 先缩放,再旋转,最后平移
p' = p · M
```

### 局部空间 ↔ 世界空间(最高频操作)
```
世界矩阵 = 局部矩阵 · 父的世界矩阵          (worldMatrix = localMatrix · parentWorldMatrix)
局部矩阵 = 世界矩阵 · inverse(父的世界矩阵)  (反解局部)
```
这俩公式你会用一辈子:把一个物体"对齐"到另一个、把世界坐标的点转到某骨骼的局部空间、计算偏移(offset)。

### 代码示例:NumPy 实现核心操作
```python
import numpy as np

def make_translation(t):
    """t = (tx,ty,tz) → 4x4 平移矩阵(行主序)"""
    M = np.eye(4)
    M[3, :3] = t
    return M

def world_to_local(world_mat, parent_world_mat):
    """把世界矩阵转成相对父的局部矩阵"""
    return world_mat @ np.linalg.inv(parent_world_mat)

def local_to_world(local_mat, parent_world_mat):
    """局部矩阵 → 世界矩阵"""
    return local_mat @ parent_world_mat

# 求 A 相对 B 的偏移矩阵(常用于 maintain offset)
def compute_offset(child_world, target_world):
    """child 相对 target 的偏移:offset · target = child"""
    return child_world @ np.linalg.inv(target_world)
```

### 代码示例:对接 OpenMaya
```python
import maya.api.OpenMaya as om

def get_world_matrix(node):
    """取节点世界矩阵为 MMatrix"""
    sel = om.MSelectionList()
    sel.add(node)
    dag = sel.getDagPath(0)
    return dag.inclusiveMatrix()      # 世界矩阵

def matrix_to_numpy(mmatrix):
    """MMatrix → numpy (4,4),保持行主序"""
    import numpy as np
    return np.array(mmatrix, dtype=np.float64).reshape(4, 4)
```

### 踩坑提醒
- **乘法顺序 + 主序**双重陷阱:换库就要重新确认。记住 Maya = 行向量 `v*M`、左乘父在右(`local · parent`)。
- **非均匀缩放 + 旋转**会产生**剪切(shear)**,分解(`decompose`)时要小心。
- **求逆代价**:`inv()` 不便宜;纯刚体变换(只有旋转+平移)可用"转置旋转部分 + 反向平移"快速求逆,别动用通用 `inv`。

---

## 8. 四元数与旋转插值

### 是什么
**四元数(Quaternion)** 是表示 3D 旋转的 4 个数 `(x, y, z, w)`。比欧拉角更稳:**没有万向锁、能平滑插值**。

### 为什么对你重要
- **欧拉角会万向锁(Gimbal Lock)**,且插值会抽搐;四元数解决这两点。
- **旋转插值用 slerp(球面线性插值)**,平移/权重才用 lerp。**用错会让旋转走捷径穿模或变速。**
- 重定向、动画混合、注视(aim)约束底层都靠它。

### lerp vs slerp
```
lerp(线性):  适合平移、缩放、权重 —— 沿直线匀速
slerp(球面):适合旋转 —— 沿球面大圆弧匀速,角速度恒定
```

### 代码示例:四元数 slerp
```python
import numpy as np

def slerp(q0, q1, t):
    """球面线性插值,q0/q1 为单位四元数 (x,y,z,w),t∈[0,1]"""
    q0 = q0 / np.linalg.norm(q0)
    q1 = q1 / np.linalg.norm(q1)
    dot = np.dot(q0, q1)

    # 取最短路径:点积为负说明走的是大弧,翻转一个
    if dot < 0.0:
        q1 = -q1
        dot = -dot

    # 几乎共线时退化为 lerp,避免除零
    if dot > 0.9995:
        return (q0 + t * (q1 - q0)) / np.linalg.norm(q0 + t * (q1 - q0))

    theta_0 = np.arccos(dot)
    theta = theta_0 * t
    q2 = q1 - q0 * dot
    q2 = q2 / np.linalg.norm(q2)
    return q0 * np.cos(theta) + q2 * np.sin(theta)
```

### 代码示例:用 OpenMaya 的四元数(生产推荐)
```python
import maya.api.OpenMaya as om

q0 = om.MQuaternion(0, 0, 0, 1)
q1 = om.MEulerRotation(0, 1.57, 0).asQuaternion()

# 内置 slerp,别自己造轮子
q_mid = om.MQuaternion.slerp(q0, q1, 0.5)
euler = q_mid.asEulerRotation()
print([round(a, 3) for a in (euler.x, euler.y, euler.z)])
```

### 踩坑提醒
- **`q` 和 `-q` 表示同一个旋转**,但插值时方向相反——一定要做"最短路径"判断(上面 `dot < 0` 那段)。
- 四元数必须**归一化**;累乘后会漂移,定期 normalize。
- 和欧拉角互转时,**旋转顺序(rotateOrder)** 必须对齐 Maya 节点设置,否则结果错。

---

## 9. 插值与样条曲线

### 是什么
- **插值**:在已知点之间"补"出中间值。
- **样条曲线**:用少量控制点定义一条光滑曲线。

### 为什么对你重要
- **动画曲线**(F-Curve)、**IK 拉伸**、**沿曲线分布关节**(spline IK、触手、脊柱)。
- 程序化布线、缆线/链条工具。

### 常用曲线对比
| 曲线 | 特点 | 典型用途 |
|------|------|---------|
| **线性 Lerp** | 最简单,折线 | 权重、淡入淡出 |
| **Bezier** | 控制点不一定在曲线上,手柄直观 | UI 缓动、路径 |
| **Catmull-Rom** | **曲线穿过所有控制点**,局部可控 | 沿点放关节、相机路径 |
| **B-Spline** | 最光滑,但不穿过控制点 | 平滑变形、Spline IK |

### 代码示例:Catmull-Rom(穿过控制点,最实用)
```python
import numpy as np

def catmull_rom(p0, p1, p2, p3, t):
    """在 p1→p2 段插值,p0/p3 为前后邻居控制切线。t∈[0,1]"""
    t2, t3 = t * t, t * t * t
    return 0.5 * (
        (2 * p1) +
        (-p0 + p2) * t +
        (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 +
        (-p0 + 3 * p1 - 3 * p2 + p3) * t3
    )

def catmull_rom_chain(points, samples_per_seg=10):
    """对一串控制点生成光滑曲线上的采样点"""
    pts = np.asarray(points, dtype=np.float64)
    out = []
    for i in range(1, len(pts) - 2):
        for s in range(samples_per_seg):
            t = s / samples_per_seg
            out.append(catmull_rom(pts[i-1], pts[i], pts[i+1], pts[i+2], t))
    return np.array(out)

# 用途:沿这条曲线均匀放 20 根 joint 做触手
```

### 踩坑提醒
- **弧长参数化**:`t` 均匀≠曲线上间距均匀。沿曲线**等距**放关节,需要按弧长重新参数化(累积弧长查表反查 `t`)。Maya 的 `pointOnCurveInfo` 有 `turnOnPercentage` 帮你做这件事。
- Catmull-Rom 需要首尾各多一个"幽灵控制点"来定义端点切线。

---

# 第三部分:进阶算法(造工具)

## 10. IK 求解

### 是什么
**正向运动学(FK)**:给关节角度,算末端位置。
**逆向运动学(IK)**:给末端目标位置,**反解**各关节角度。

### 主流算法对比
| 算法 | 原理 | 特点 |
|------|------|------|
| **解析 IK(双骨)** | 余弦定理直接求解 | 最快、最稳,腿/臂的标配 |
| **CCD** | 从末端逐关节朝目标转 | 简单,适合长链(尾巴),可能抖 |
| **FABRIK** | 来回前后拉点,无需角度 | 快、自然,长链/绳索热门 |
| **Jacobian** | 用雅可比矩阵迭代逼近 | 通用、能加约束,计算重 |

### 代码示例:双骨解析 IK(余弦定理)
```python
import numpy as np

def two_bone_ik(root, mid_len, end_len, target, pole_vector):
    """
    经典双骨 IK(肩-肘-腕 / 髋-膝-踝)
    root: 根关节世界位置 (3,)
    mid_len: 上段长度(如大臂);end_len: 下段长度(如小臂)
    target: 末端目标位置 (3,)
    pole_vector: 极向量,决定肘/膝朝向
    返回:中间关节(肘)位置
    """
    root = np.asarray(root, float)
    target = np.asarray(target, float)

    to_target = target - root
    dist = np.linalg.norm(to_target)
    # 够不着就伸直,避免 NaN
    dist = min(dist, mid_len + end_len - 1e-4)
    dist = max(dist, abs(mid_len - end_len) + 1e-4)

    # 余弦定理:求根关节处的弯曲角
    cos_angle = (mid_len**2 + dist**2 - end_len**2) / (2 * mid_len * dist)
    cos_angle = np.clip(cos_angle, -1, 1)
    angle = np.arccos(cos_angle)

    # 在 root→target 与 pole 决定的平面内,把肘摆出来
    axis = to_target / dist
    pole_dir = np.asarray(pole_vector, float) - root
    pole_dir = pole_dir - np.dot(pole_dir, axis) * axis   # 投影到垂直分量
    pole_dir /= (np.linalg.norm(pole_dir) + 1e-9)

    mid_pos = root + axis * (np.cos(angle) * mid_len) \
                   + pole_dir * (np.sin(angle) * mid_len)
    return mid_pos
```

### 代码示例:FABRIK(长链,无三角函数)
```python
import numpy as np

def fabrik(points, target, lengths, iterations=10, tol=1e-3):
    """
    points: 初始关节位置列表 (N,3);target: 末端目标
    lengths: 各段固定长度 (N-1,)
    """
    pts = [np.asarray(p, float) for p in points]
    root = pts[0].copy()
    total = sum(lengths)

    # 够不着:直接朝目标伸直
    if np.linalg.norm(target - root) > total:
        dir_ = (target - root) / np.linalg.norm(target - root)
        for i in range(1, len(pts)):
            pts[i] = pts[i-1] + dir_ * lengths[i-1]
        return pts

    for _ in range(iterations):
        # 后向:末端拉到 target,逐节回拉
        pts[-1] = np.asarray(target, float)
        for i in range(len(pts) - 2, -1, -1):
            d = (pts[i] - pts[i+1])
            d /= np.linalg.norm(d)
            pts[i] = pts[i+1] + d * lengths[i]
        # 前向:根固定回原位,逐节往外推
        pts[0] = root
        for i in range(1, len(pts)):
            d = (pts[i] - pts[i-1])
            d /= np.linalg.norm(d)
            pts[i] = pts[i-1] + d * lengths[i-1]
        if np.linalg.norm(pts[-1] - target) < tol:
            break
    return pts
```

### 踩坑提醒
- **目标够不着**时务必 clamp(伸直),否则 `arccos` 出 NaN、链条乱飞。
- **极向量(pole vector)** 决定肘/膝朝向,是双骨 IK 体验好坏的关键。
- FABRIK / CCD 是位置解,转回关节**旋转**时仍要构造朝向矩阵。

---

## 11. 蒙皮算法:LBS / DQS

### 是什么
蒙皮:让顶点跟着骨骼变形。每个顶点绑定到若干骨骼,带权重。

### 线性混合蒙皮(LBS, Linear Blend Skinning)
最常用。顶点最终位置 = 各骨骼变换结果的**加权平均**:

```
v' = Σ wᵢ · (Mᵢ · Bᵢ⁻¹) · v
     i
wᵢ : 第 i 根骨骼对该点的权重(Σwᵢ = 1)
Mᵢ : 骨骼当前世界矩阵
Bᵢ⁻¹: 骨骼绑定姿势(bind pose)的逆
```

### 代码示例:LBS 核心(NumPy 向量化)
```python
import numpy as np

def linear_blend_skinning(verts, weights, bone_mats, bind_inv):
    """
    verts:     (N,3) 绑定姿势下的顶点
    weights:   (N,B) 每点对每骨的权重
    bone_mats: (B,4,4) 各骨当前世界矩阵(行主序)
    bind_inv:  (B,4,4) 各骨绑定逆矩阵
    返回:      (N,3) 变形后顶点
    """
    N = verts.shape[0]
    B = bone_mats.shape[0]
    skin = bone_mats @ bind_inv             # (B,4,4) 每骨的蒙皮变换
    homo = np.hstack([verts, np.ones((N, 1))])  # (N,4)

    out = np.zeros((N, 3))
    for b in range(B):                      # 骨骼数远小于顶点数,这层循环可接受
        transformed = homo @ skin[b]        # (N,4)
        out += weights[:, b:b+1] * transformed[:, :3]
    return out
```

### 双四元数蒙皮(DQS, Dual Quaternion Skinning)
- **解决 LBS 的"糖纸 / 塌陷"问题**:LBS 在大角度扭转(手腕、肩膀)时体积会瘪。
- DQS 用对偶四元数插值,保体积更好,代价是计算贵、缩放支持差。

| | LBS | DQS |
|---|-----|-----|
| 速度 | 快 | 慢 ~1.5x |
| 扭转保体积 | 差(糖纸) | 好 |
| 非均匀缩放 | 支持 | 不支持 |
| 普及度 | 默认 | 关节处补强用 |

### 踩坑提醒
- **权重归一化**:每点权重和必须为 1,否则顶点漂移。
- **绑定逆矩阵 `Bᵢ⁻¹` 只算一次**缓存好,别每帧求逆。
- 手腕扭转塌陷是 LBS 的固有缺陷,靠**矫正形(corrective)** 或局部 DQS 补,不是你权重刷得不够好。

---

## 12. 最小二乘与数值优化

### 是什么
当方程**多于未知数**(超定),无法精确求解时,找一个让"总误差平方和最小"的解。

```
求 x 使 ‖A·x − b‖² 最小
```

### 为什么对你重要
- **`py-dem-bones` 的内核就是这个**:给定一堆动画帧的顶点位置,**反解**出骨骼变换 + 蒙皮权重,使重建误差最小。
- 姿态拟合、约束求解、曲线拟合、传感器/动捕数据降噪。

### 代码示例:最小二乘拟合
```python
import numpy as np

# 例:已知若干 (输入特征 → 目标位移),反解线性映射权重
A = np.random.rand(200, 5)     # 200 个观测,5 个未知权重
b = np.random.rand(200)        # 200 个目标值

# 最小二乘解(底层是 SVD,数值稳定)
x, residuals, rank, sv = np.linalg.lstsq(A, b, rcond=None)
print("解:", x)
print("残差:", residuals)
```

### 代码示例:带边界/约束的优化(scipy)
```python
from scipy.optimize import least_squares
import numpy as np

def residual(params, observed):
    """残差函数:返回 (预测 - 观测) 向量,优化器会最小化其平方和"""
    a, b, c = params
    x = np.linspace(0, 1, len(observed))
    predicted = a * x**2 + b * x + c
    return predicted - observed

observed = np.random.rand(50)
result = least_squares(residual, x0=[1, 1, 1], args=(observed,),
                       bounds=([-10, -10, -10], [10, 10, 10]))
print("拟合参数:", result.x)
```

### 踩坑提醒
- **超定 vs 欠定**:观测够多(超定)解才稳;观测不足(欠定)会过拟合或多解,需要正则化(如 Ridge,加 `λ‖x‖²`)。
- 权重求解要加**非负 + 归一化**约束(权重不能为负),纯 `lstsq` 不保证,得用约束优化或 NNLS。

---

## 13. 空间加速结构:KD-tree / BVH / 八叉树

### 是什么
把空间中的点/物体组织起来,让"找最近的""查范围内的""检测碰撞"从 `O(N)` 降到 `O(log N)`。

| 结构 | 擅长 | 典型用途 |
|------|------|---------|
| **KD-tree** | 点的最近邻 / K 近邻查询 | 权重传递、最近点对齐、点云 |
| **BVH** | 物体的碰撞 / 求交 | 射线检测、布料自碰撞 |
| **八叉树/网格** | 均匀空间的范围查询 | 体素化、邻域查找 |

### 为什么对你重要
- **权重传递 / 投影**:把 A 模型的蒙皮权重传到 B 模型——对每个 B 顶点找 A 上最近点。10 万 × 10 万暴力是 `O(N²)`,KD-tree 让它能跑。
- **ChaosCloth 自碰撞**底层就是 BVH。

### 代码示例:KD-tree 做最近点权重传递
```python
import numpy as np
from scipy.spatial import cKDTree

def transfer_weights(src_verts, src_weights, dst_verts):
    """
    把源网格的蒙皮权重,按最近点传到目标网格
    src_verts: (M,3)  src_weights: (M,B)  dst_verts: (N,3)
    返回 dst 上的权重 (N,B)
    """
    tree = cKDTree(src_verts)           # 建树 O(M log M)
    # 对每个目标点查最近的源点,O(N log M)
    dist, idx = tree.query(dst_verts, k=1)
    return src_weights[idx]             # 直接搬最近点的权重

# 进阶:k=3 取最近 3 点按距离加权,过渡更平滑
def transfer_weights_smooth(src_verts, src_weights, dst_verts, k=3):
    tree = cKDTree(src_verts)
    dist, idx = tree.query(dst_verts, k=k)
    w = 1.0 / (dist + 1e-6)             # 距离倒数做权重
    w /= w.sum(axis=1, keepdims=True)
    # 加权混合 k 个邻居的蒙皮权重
    return np.einsum('nk,nkb->nb', w, src_weights[idx])
```

### 踩坑提醒
- 最近点传权重,**遇到薄片/对穿**(如腋下、裙摆)会传错——空间近不代表拓扑近。必要时按法线方向过滤,或用测地距离。
- 建树有成本,**一次建树多次查询**才划算;单次查询用不上。

---

## 14. 物理积分与约束求解:Verlet / PBD

### 是什么
- **数值积分**:由受力/速度推进粒子位置(布料、头发、动力学)。
- **PBD(Position Based Dynamics)**:不直接管力,而是**直接修正位置**去满足约束(如"这两点距离必须是 L")。稳定、好控,游戏物理主流。

### 为什么对你重要
**ChaosCloth、UE Dynamic Animation(KawaiiPhysics 类弹骨)** 底层就是这套。理解它,才知道参数(stiffness、iteration、damping)为什么那样影响表现。

### 代码示例:Verlet 积分
```python
import numpy as np

def verlet_step(pos, prev_pos, accel, dt, damping=0.99):
    """
    Verlet:不存速度,用'当前位置 - 上一帧位置'隐式表达速度
    pos, prev_pos, accel: (N,3)
    """
    velocity = (pos - prev_pos) * damping
    new_pos = pos + velocity + accel * (dt * dt)
    return new_pos, pos      # 返回新位置 + 把当前位置变成"上一帧"
```

### 代码示例:PBD 距离约束(布料的核心)
```python
import numpy as np

def satisfy_distance_constraints(pos, edges, rest_len,
                                 stiffness=1.0, iterations=8):
    """
    迭代投影:把每条边的两端点拉/推回到静止长度
    pos: (N,3) 粒子位置;edges: [(i,j),...];rest_len: 每条边静止长度
    iterations 越多越'硬'(越不可拉伸)
    """
    for _ in range(iterations):           # 多次迭代逼近全局满足
        for (i, j), L in zip(edges, rest_len):
            delta = pos[j] - pos[i]
            d = np.linalg.norm(delta)
            if d < 1e-9:
                continue
            # 误差的一半各自分摊(假设等质量)
            correction = (d - L) / d * 0.5 * stiffness
            pos[i] += delta * correction
            pos[j] -= delta * correction
    return pos
```

### 踩坑提醒
- **迭代次数 = 刚度**:iteration 越多布料越"硬"/越不可拉伸,但越慢。这就是 ChaosCloth 里调 iteration 的本质。
- **固定点(pin)**:被约束钉住的点(如裙子腰部)在投影后要强制设回原位,否则会被拉走。
- Verlet 的 `damping` 控制能量衰减——太低会永远抖,太高像在糖浆里。

---

## 15. RBF 散点插值:PSD / 修形驱动

### 是什么
**径向基函数(Radial Basis Function)**:已知一批"输入姿态 → 输出值(形变/位移)"的样本,对**任意新输入**插值出合理输出。本质是"离哪个已知样本近,就更像哪个"。

### 为什么对你重要
- **姿态空间变形(PSD / Pose Space Deformation)**:手肘弯到某角度触发某矫正形,中间角度平滑过渡。
- **MetaHuman 表情、矫正形驱动、辅助关节**(你 memory 里的 DNA 修形场景)。
- RBF 节点(如 Maya 的 `weightDriver`/SHAPES、UE 的 RBF Solver)就是它。

### 数学骨架
```
f(x) = Σ wᵢ · φ(‖x − cᵢ‖)
       i
cᵢ : 第 i 个样本姿态(中心)
φ  : 基函数(高斯 e^(−(εr)²) / 薄板样条 r²·log r 等)
wᵢ : 待解权重 —— 用样本"精确命中"这个条件解线性方程组
```

### 代码示例:RBF 插值器
```python
import numpy as np

class RBFInterpolator:
    """散点插值:训练样本 (姿态→值),对新姿态预测"""

    def __init__(self, kernel='gaussian', epsilon=1.0):
        self.kernel = kernel
        self.eps = epsilon

    def _phi(self, r):
        if self.kernel == 'gaussian':
            return np.exp(-(self.eps * r) ** 2)
        elif self.kernel == 'thin_plate':
            return np.where(r > 0, r ** 2 * np.log(r + 1e-9), 0)
        return r   # linear

    def fit(self, centers, values):
        """centers: (K, in_dim) 样本姿态;values: (K, out_dim) 对应输出"""
        self.centers = np.asarray(centers, float)
        K = len(self.centers)
        # 样本两两距离矩阵 → 基函数矩阵 Φ
        dists = np.linalg.norm(
            self.centers[:, None, :] - self.centers[None, :, :], axis=2)
        Phi = self._phi(dists)               # (K,K)
        # 解 Φ · w = values,使插值精确穿过样本
        self.weights = np.linalg.solve(Phi, np.asarray(values, float))

    def predict(self, x):
        """x: (in_dim,) 新姿态 → 插值输出"""
        x = np.asarray(x, float)
        r = np.linalg.norm(self.centers - x, axis=1)
        return self._phi(r) @ self.weights

# 用途示例:手肘角度 → 矫正形混合权重
rbf = RBFInterpolator(kernel='gaussian', epsilon=0.5)
rbf.fit(centers=[[0.0], [1.57], [3.14]],          # 0°/90°/180°
        values=[[0, 0], [1, 0], [0, 1]])          # 各角度的矫正形权重
print(rbf.predict([0.8]))                          # 约 45°,插值出过渡权重
```

### 踩坑提醒
- **核函数 + epsilon(影响半径)** 决定过渡软硬:epsilon 太大过渡糊、太小样本间出现"凹陷"。需要调。
- 样本姿态用**四元数距离**而非欧拉差,才符合旋转的真实远近。
- 样本太密 / 重复会让 Φ 矩阵接近奇异,`solve` 不稳——加一点正则项(对角线 `+λ`)。

---

## 16. 重心坐标 Barycentric

### 是什么
用三角形三个顶点的**加权比例 `(u, v, w)`(u+v+w=1)** 来表达三角形内任意一点。它是"点在面上哪个位置"的标准语言。

```
P = u·A + v·B + w·C        (u+v+w = 1)
```

### 为什么对你重要
- **属性传递 / 投影**:把 UV、颜色、权重从一个网格搬到另一个——找到点落在目标三角形里,用重心坐标插值三个顶点的属性。
- **Wrap / 缠绕变形**:把高模"贴"在低模上随动。
- **点贴合表面**:饰品/扣子吸附到角色皮肤并跟随变形。

### 代码示例:计算重心坐标 + 插值属性
```python
import numpy as np

def barycentric(p, a, b, c):
    """求点 p 在三角形 abc 内的重心坐标 (u,v,w)。全为正 → 在三角形内"""
    v0, v1, v2 = b - a, c - a, p - a
    d00 = np.dot(v0, v0); d01 = np.dot(v0, v1); d11 = np.dot(v1, v1)
    d20 = np.dot(v2, v0); d21 = np.dot(v2, v1)
    denom = d00 * d11 - d01 * d01
    v = (d11 * d20 - d01 * d21) / denom
    w = (d00 * d21 - d01 * d20) / denom
    u = 1.0 - v - w
    return np.array([u, v, w])

def interpolate_attr(bary, attr_a, attr_b, attr_c):
    """用重心坐标插值三个顶点上的任意属性(UV/权重/颜色)"""
    u, v, w = bary
    return u * attr_a + v * attr_b + w * attr_c

# 用途:点 p 落在三角形里,插出它的 UV
A = np.array([0, 0, 0.]); B = np.array([1, 0, 0.]); C = np.array([0, 1, 0.])
P = np.array([0.25, 0.25, 0.])
bary = barycentric(P, A, B, C)
uv = interpolate_attr(bary, np.array([0, 0]), np.array([1, 0]), np.array([0, 1]))
print("重心坐标:", bary, " 插值UV:", uv)
```

### 踩坑提醒
- **点不在三角形所在平面内**时,先投影到平面再求;重心坐标本身是 2D 概念。
- 三个分量**任一为负 → 点在三角形外**,传递属性前要先判断,否则会外插出错误值。

---

# 附录

## 附录 A. 复杂度速查

| 操作 | 复杂度 | 备注 |
|------|--------|------|
| 字典 / set 查找 | O(1) | 缓存首选 |
| 数组随机访问 | O(1) | NumPy 索引 |
| DFS / BFS 遍历 | O(V + E) | V 节点 E 边 |
| 拓扑排序 | O(V + E) | Kahn |
| 矩阵乘法 (4×4) | O(1) | 固定大小,常数 |
| N 点暴力最近点 | O(N²) | ⚠️ 大数据会炸 |
| KD-tree 最近点 | O(log N) | 建树 O(N log N) |
| 最小二乘 (SVD) | O(m·n²) | m 观测 n 未知 |
| PBD 一次迭代 | O(E) | ×迭代次数 |

## 附录 B. 学习路径

```
① 线性代数(矩阵 + 四元数)   ← 地基,优先级最高,投入产出比最大
        │
② 树/图遍历 + DAG/DG 理解     ← Maya 日常工作的语言
        │
③ NumPy 向量化 + 字典缓存     ← 让脚本从"能跑"到"跑得快"
        │
   ┌────┴────┐
④ IK / 蒙皮   ⑤ 最小二乘 / RBF / PBD   ← 造高级工具与物理时深入
```

- **前三层**:看懂别人的绑定、写出干净高效脚本的门槛。
- **后两层**:自研求解器、程序化绑定、物理工具的门槛。

## 附录 C. TA 专属踩坑清单

1. **矩阵主序 / 乘法顺序**:Maya = 行向量 `v·M`、`local·parent`。跨库(dem-bones、UE、scipy)必先确认,否则旋转错乱。
2. **同名节点**:脚本一律用 `fullPath`,短名会咬人。
3. **欧拉 vs 四元数**:旋转插值用 slerp;互转时 rotateOrder 必须对齐。
4. **Python 循环处理顶点**:能向量化就别 for,差几十倍。
5. **查询 Maya 很慢**:能缓存就缓存,批处理时尤甚。
6. **权重必须归一化**:LBS 权重和不为 1 → 顶点漂移。
7. **绑定逆矩阵只算一次**:别每帧求逆。
8. **够不着的 IK**:务必 clamp,否则 NaN 乱飞。
9. **最近点传权重的对穿问题**:空间近 ≠ 拓扑近,薄片处会传错。
10. **PBD 迭代次数 = 刚度**:这是 ChaosCloth 调参的本质。

---

> 本手册聚焦"绑定 / 动画 TA 真正高频用到"的子集。需要把某一章展开成**完整可运行的 Maya / UE 工具**(比如 Spline IK 构建器、权重传递工具、RBF 修形驱动节点),随时找我。
