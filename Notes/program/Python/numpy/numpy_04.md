#  线性代数（向量 / 矩阵 / 四元数）

本文档介绍 NumPy 在**线性代数**方面的用法，围绕绑定 / Tech Art 日常工作（Maya、MotionBuilder、UE5）中最常用的三类对象展开：**向量、矩阵、四元数**，并附实战案例（Pole Vector 定位、LookAt 矩阵、Twist 提取、Slerp 插值、批量蒙皮权重处理）。

```python
import numpy as np
```

---

## 0. DCC 坐标系约定（重要前提）

写工具前先确认坐标系，否则算出来的结果"差一个轴"：

| 软件 | 上方向 | 手性 | 向量约定 | 单位 |
| --- | --- | --- | --- | --- |
| Maya | Y-up | 右手系 | **行向量**：`p' = p @ M` | cm |
| MotionBuilder | Y-up | 右手系 | 行向量 | cm |
| UE5 | Z-up | **左手系** | 行向量（`FMatrix`） | cm |

- Maya 的 `MMatrix` / `xform -matrix` 返回的 16 个数是**行主序**，平移在**第 4 行**（`m[12], m[13], m[14]`）。
- 本笔记统一采用**行向量右乘**约定：`p' = p @ M`，与 Maya / UE 一致。
- Maya → UE 的坐标转换（常见做法）：`(x, y, z) → (x, z, y)`，即交换 Y/Z 并由右手系变为左手系。

---

## 1. 向量运算

### 1.1 基础：长度、归一化、点积、叉积

```python
v1 = np.array([1.0, 2.0, 3.0])
v2 = np.array([4.0, 5.0, 6.0])

length = np.linalg.norm(v1)          # 向量长度（模）-> 3.7417
v1_n = v1 / np.linalg.norm(v1)       # 归一化（单位向量）

dot = np.dot(v1, v2)                 # 点积 -> 32.0
cross = np.cross(v1, v2)             # 叉积 -> [-3.  6. -3.]
```

绑定中的几何意义：

- **点积**：衡量两向量方向的相似度。`dot > 0` 同向、`= 0` 垂直、`< 0` 反向。常用于判断关节朝向、驱动 Corrective BlendShape 权重（如 `dot(骨骼轴, 参考轴)` 映射到 0~1）。
- **叉积**：得到垂直于两向量的向量，方向遵循右手定则（Maya）。常用于**构建正交坐标系**、计算法线、判断左右侧。

```python
def normalize(v: np.ndarray) -> np.ndarray:
    """归一化向量，长度接近 0 时原样返回避免除零。"""
    n = np.linalg.norm(v)
    return v if n < 1e-8 else v / n
```

### 1.2 向量夹角

```python
def angle_between(v1: np.ndarray, v2: np.ndarray) -> float:
    """计算两向量夹角（弧度）。clip 防止浮点误差导致 arccos 越界。"""
    cos_theta = np.dot(normalize(v1), normalize(v2))
    return float(np.arccos(np.clip(cos_theta, -1.0, 1.0)))

np.degrees(angle_between(np.array([1, 0, 0]), np.array([0, 1, 0])))  # 90.0
```

> 用途：肘/膝弯曲角度检测（驱动 RBF / SDK）、判断骨骼链是否共线（IK 极向量退化检测）。

### 1.3 向量投影

把 `v` 投影到 `onto` 方向上（Twist 提取、把点吸附到轴线上都会用到）：

```python
def project(v: np.ndarray, onto: np.ndarray) -> np.ndarray:
    """v 在 onto 方向上的投影分量。"""
    d = normalize(onto)
    return np.dot(v, d) * d
```

### 1.4 案例：计算 IK Pole Vector 位置

经典问题：已知肩、肘、腕三个关节位置，求极向量控制器应放的位置（在肘部弯曲平面内、垂直于肩腕连线向外）。

```python
def pole_vector_position(
    shoulder: np.ndarray, elbow: np.ndarray, wrist: np.ndarray, offset: float = 30.0
) -> np.ndarray:
    """根据三关节位置计算 Pole Vector 控制器位置。

    Args:
        shoulder: 肩关节世界坐标.
        elbow: 肘关节世界坐标.
        wrist: 腕关节世界坐标.
        offset: 控制器沿弯曲方向推出的距离（cm）.

    Returns:
        Pole Vector 控制器的世界坐标.
    """
    start_to_end = wrist - shoulder
    start_to_mid = elbow - shoulder
    # 肘部在肩腕连线上的投影点
    t = np.dot(start_to_mid, start_to_end) / np.dot(start_to_end, start_to_end)
    projection = shoulder + start_to_end * t
    # 由投影点指向肘部的方向即弯曲方向
    pole_dir = normalize(elbow - projection)
    return elbow + pole_dir * offset


# Maya 中配合使用：
# import pymel.core as pm
# pos = [np.array(pm.xform(j, q=True, ws=True, t=True)) for j in joints]
# pv = pole_vector_position(*pos)
# pm.xform(pv_ctrl, ws=True, t=pv.tolist())
```

---

## 2. 矩阵运算

### 2.1 矩阵乘法：`@`

注意 `*` 是逐元素相乘，**矩阵乘法要用 `@`**（或 `np.matmul`）：

```python
m1 = np.array([[1, 2], [3, 4]])
m2 = np.array([[5, 6], [7, 8]])

m1 * m2   # 逐元素 -> [[ 5 12], [21 32]]（这不是矩阵乘法！）
m1 @ m2   # 矩阵乘法 -> [[19 22], [43 50]]
```

### 2.2 常用 `np.linalg` 函数

```python
m = np.array([[2.0, 0.0], [0.0, 4.0]])

np.eye(4)               # 4×4 单位矩阵
np.linalg.inv(m)        # 逆矩阵 -> [[0.5 0], [0 0.25]]
np.linalg.det(m)        # 行列式 -> 8.0
m.T                     # 转置
np.linalg.solve(a, b)   # 解线性方程组 a @ x = b（比 inv(a) @ b 更快更稳定）
```

绑定中的对应关系：

- **逆矩阵** = Maya 节点的 `worldInverseMatrix`。求相对变换：`local = child_world @ np.linalg.inv(parent_world)`（行向量约定下顺序如此）。
- **行列式** < 0 说明矩阵含**镜像/负缩放**——检查镜像骨骼、修复蒙皮翻转时很有用。
- **纯旋转矩阵**满足 `inv(R) == R.T`（正交矩阵），可用转置代替求逆以提高效率。

### 2.3 4×4 变换矩阵（TRS）

Maya / UE 的世界矩阵都是 4×4 齐次矩阵。行向量约定下的布局：

```python
# [ Xx  Xy  Xz  0 ]   <- X 轴方向（含缩放）
# [ Yx  Yy  Yz  0 ]   <- Y 轴方向
# [ Zx  Zy  Zz  0 ]   <- Z 轴方向
# [ Tx  Ty  Tz  1 ]   <- 平移

def compose_matrix(
    translate: np.ndarray, rotation: np.ndarray, scale: np.ndarray
) -> np.ndarray:
    """由平移向量、3×3 旋转矩阵、缩放向量组装 4×4 变换矩阵（行向量约定）。"""
    m = np.eye(4)
    m[:3, :3] = np.diag(scale) @ rotation  # 先缩放后旋转
    m[3, :3] = translate
    return m


def transform_point(point: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    """用 4×4 矩阵变换一个 3D 点（w=1，受平移影响）。"""
    p = np.append(point, 1.0)
    return (p @ matrix)[:3]


def transform_vector(vector: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    """用 4×4 矩阵变换一个方向向量（w=0，不受平移影响）。"""
    return vector @ matrix[:3, :3]
```

从矩阵中**提取 TRS**：

```python
def decompose_matrix(m: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """分解 4×4 矩阵为 (translate, rotation_3x3, scale)。不处理斜切。"""
    translate = m[3, :3].copy()
    scale = np.array([np.linalg.norm(m[i, :3]) for i in range(3)])
    rotation = m[:3, :3] / scale[:, np.newaxis]  # 每行除以自身长度
    return translate, rotation, scale
```

### 2.4 与 Maya / UE 的互转

```python
# Maya: MMatrix / xform 返回 16 个 float（行主序），直接 reshape 即可
# import maya.api.OpenMaya as om
# m_np = np.array(om.MMatrix(mm)).reshape(4, 4)      # MMatrix -> numpy
# mm = om.MMatrix(m_np.flatten().tolist())            # numpy -> MMatrix

# UE5 Python: unreal.Matrix 同为行主序
# import unreal
# m_np = np.array([list(unreal.Vector4(*row)) for row in ue_matrix.to_tuple()])
# 更常用的是 unreal.Transform 的 translation/rotation/scale3d 三段分别转换
```

### 2.5 绕轴旋转矩阵

```python
def rotation_matrix(axis: str, angle: float) -> np.ndarray:
    """构建绕主轴的 3×3 旋转矩阵（行向量约定：p' = p @ R）。

    Args:
        axis: 'x' / 'y' / 'z'.
        angle: 旋转角（弧度）.
    """
    c, s = np.cos(angle), np.sin(angle)
    if axis == "x":
        return np.array([[1, 0, 0], [0, c, s], [0, -s, c]])
    if axis == "y":
        return np.array([[c, 0, -s], [0, 1, 0], [s, 0, c]])
    if axis == "z":
        return np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]])
    raise ValueError(f"未知轴: {axis}")


# 欧拉角 XYZ 顺序（Maya 默认 rotateOrder=xyz，行向量约定）：
# R = Rx @ Ry @ Rz
```

### 2.6 案例：构建 LookAt（Aim）矩阵

Aim Constraint 的核心算法——让物体的某个轴指向目标，用 up 向量稳定另一个轴：

```python
def look_at_matrix(
    eye: np.ndarray, target: np.ndarray, up: np.ndarray = np.array([0.0, 1.0, 0.0])
) -> np.ndarray:
    """构建 LookAt 矩阵：X 轴指向目标，Y 轴尽量对齐 up（Maya 风格 aim=X, up=Y）。

    Args:
        eye: 物体位置.
        target: 目标位置.
        up: 世界 up 参考向量.

    Returns:
        4×4 变换矩阵（行向量约定）.
    """
    x_axis = normalize(target - eye)
    z_axis = normalize(np.cross(x_axis, up))   # aim 与 up 共线时会退化，需业务上规避
    y_axis = np.cross(z_axis, x_axis)

    m = np.eye(4)
    m[0, :3] = x_axis
    m[1, :3] = y_axis
    m[2, :3] = z_axis
    m[3, :3] = eye
    return m
```

> 用途：眼球注视绑定、肋骨/纽扣朝向批量摆放、无约束节点的程序化 Aim。UE5 里对应 Control Rig 的 `Aim` 节点 / `FindLookAtRotation`。

---

## 3. 四元数

NumPy 没有内置四元数类型，用长度为 4 的数组表示。**本笔记采用 `(x, y, z, w)` 顺序**——与 Maya API（`MQuaternion`）和 UE（`FQuat`）一致；注意 SciPy 的 `Rotation` 也是 `(x, y, z, w)`，但部分数学库（如 numpy-quaternion）是 `(w, x, y, z)`，跨库时务必确认。

### 3.1 基本构造与运算

```python
QUAT_IDENTITY = np.array([0.0, 0.0, 0.0, 1.0])  # 单位四元数（无旋转）


def quat_from_axis_angle(axis: np.ndarray, angle: float) -> np.ndarray:
    """由旋转轴和角度（弧度）构造四元数 (x, y, z, w)。"""
    half = angle * 0.5
    xyz = normalize(axis) * np.sin(half)
    return np.array([xyz[0], xyz[1], xyz[2], np.cos(half)])


def quat_mul(q1: np.ndarray, q2: np.ndarray) -> np.ndarray:
    """四元数乘法：先应用 q1 再应用 q2 的旋转（与 Maya MQuaternion 乘序一致）。"""
    x1, y1, z1, w1 = q1
    x2, y2, z2, w2 = q2
    return np.array([
        w2 * x1 + x2 * w1 + y2 * z1 - z2 * y1,
        w2 * y1 - x2 * z1 + y2 * w1 + z2 * x1,
        w2 * z1 + x2 * y1 - y2 * x1 + z2 * w1,
        w2 * w1 - x2 * x1 - y2 * y1 - z2 * z1,
    ])


def quat_conjugate(q: np.ndarray) -> np.ndarray:
    """共轭（单位四元数的共轭即逆旋转）。"""
    return np.array([-q[0], -q[1], -q[2], q[3]])


def quat_rotate_vector(q: np.ndarray, v: np.ndarray) -> np.ndarray:
    """用四元数旋转向量：v' = q^-1 * v * q（行向量约定下的等价式）。"""
    qv = np.array([v[0], v[1], v[2], 0.0])
    return quat_mul(quat_mul(quat_conjugate(q), qv), q)[:3]
```

### 3.2 四元数 ↔ 旋转矩阵

```python
def quat_to_matrix(q: np.ndarray) -> np.ndarray:
    """单位四元数 (x, y, z, w) 转 3×3 旋转矩阵（行向量约定）。"""
    x, y, z, w = q
    return np.array([
        [1 - 2 * (y * y + z * z), 2 * (x * y + z * w), 2 * (x * z - y * w)],
        [2 * (x * y - z * w), 1 - 2 * (x * x + z * z), 2 * (y * z + x * w)],
        [2 * (x * z + y * w), 2 * (y * z - x * w), 1 - 2 * (x * x + y * y)],
    ])


def matrix_to_quat(m: np.ndarray) -> np.ndarray:
    """3×3 纯旋转矩阵转四元数 (x, y, z, w)，Shepperd 方法保证数值稳定。"""
    trace = m[0, 0] + m[1, 1] + m[2, 2]
    if trace > 0.0:
        s = 0.5 / np.sqrt(trace + 1.0)
        return np.array([
            (m[1, 2] - m[2, 1]) * s,
            (m[2, 0] - m[0, 2]) * s,
            (m[0, 1] - m[1, 0]) * s,
            0.25 / s,
        ])
    i = int(np.argmax([m[0, 0], m[1, 1], m[2, 2]]))
    j, k = (i + 1) % 3, (i + 2) % 3
    s = 2.0 * np.sqrt(max(1.0 + m[i, i] - m[j, j] - m[k, k], 0.0))
    q = np.empty(4)
    q[i] = 0.25 * s
    q[j] = (m[i, j] + m[j, i]) / s
    q[k] = (m[i, k] + m[k, i]) / s
    q[3] = (m[j, k] - m[k, j]) / s
    return q
```

### 3.3 案例：Slerp 球面插值

四元数最大的优势——旋转插值均匀、无万向锁。做姿态过渡、程序化动画混合时使用：

```python
def slerp(q1: np.ndarray, q2: np.ndarray, t: float) -> np.ndarray:
    """球面线性插值，t 在 [0, 1] 之间。

    自动选择短弧（dot < 0 时取反），小角度退化为线性插值避免除零。
    """
    q1, q2 = normalize(q1), normalize(q2).copy()
    dot = np.dot(q1, q2)
    if dot < 0.0:          # 保证走最短路径
        q2, dot = -q2, -dot
    if dot > 0.9995:       # 夹角过小，用 lerp 近似
        return normalize(q1 + t * (q2 - q1))
    theta = np.arccos(np.clip(dot, -1.0, 1.0))
    sin_theta = np.sin(theta)
    return (np.sin((1 - t) * theta) * q1 + np.sin(t * theta) * q2) / sin_theta
```

> Maya 对应 `MQuaternion.slerp`，UE 对应 `FQuat::Slerp`；自己实现的价值在于可以对**批量数据**（如整段动画曲线重采样）做向量化处理。

### 3.4 案例：Twist 提取（Swing-Twist 分解）

前臂/大腿扭转（twist）关节的核心算法：把一个旋转分解为"绕指定轴的扭转"和"剩余摆动"，取扭转部分按比例分配给 twist 骨骼。

```python
def swing_twist(q: np.ndarray, twist_axis: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """把四元数 q 分解为 swing * twist（先 twist 后 swing）。

    Args:
        q: 待分解的单位四元数 (x, y, z, w).
        twist_axis: 扭转轴（如骨骼的 X 轴 [1, 0, 0]）.

    Returns:
        (swing, twist) 两个单位四元数.
    """
    axis = normalize(twist_axis)
    # 把 q 的向量部分投影到扭转轴上，与 w 一起构成 twist
    proj = project(q[:3], axis)
    twist = np.array([proj[0], proj[1], proj[2], q[3]])
    norm = np.linalg.norm(twist)
    if norm < 1e-8:                      # 旋转 180° 且垂直于轴的退化情况
        twist = QUAT_IDENTITY.copy()
    else:
        twist = twist / norm
    swing = quat_mul(quat_conjugate(twist), q)  # q = twist * swing
    return swing, twist


def twist_angle(q: np.ndarray, twist_axis: np.ndarray) -> float:
    """提取绕指定轴的扭转角（弧度，带符号），可直接驱动 twist 骨骼。"""
    _, twist = swing_twist(q, twist_axis)
    angle = 2.0 * np.arccos(np.clip(twist[3], -1.0, 1.0))
    sign = 1.0 if np.dot(twist[:3], normalize(twist_axis)) >= 0.0 else -1.0
    # 归一到 [-pi, pi]
    if angle > np.pi:
        angle, sign = 2.0 * np.pi - angle, -sign
    return sign * angle


# 使用：wrist 相对 forearm 的局部旋转 -> 提取 X 轴 twist -> 乘 0.5 给中段 twist 骨骼
# t = twist_angle(local_quat, np.array([1.0, 0.0, 0.0]))
# pm.setAttr(twist_joint + ".rotateX", np.degrees(t) * 0.5)
```

> UE5 中对应 Control Rig 的 `Twist Bones` / AnimBP 的 `Twist Corrective`；理解这套数学后可以在任何 DCC 里手写等价实现。

---

## 4. 批量向量化计算（性能要点）

NumPy 的真正价值在于**一次算一批**。比如对蒙皮网格的 5 万个顶点做矩阵变换，避免 Python 层循环：

```python
# points: (N, 3) 顶点数组，matrix: 4×4
points_h = np.hstack([points, np.ones((len(points), 1))])  # (N, 4) 齐次坐标
transformed = (points_h @ matrix)[:, :3]                    # 一次性变换全部顶点

# 批量求每个顶点到某点的距离（做衰减权重）
dists = np.linalg.norm(points - center, axis=1)             # (N,)
weights = np.clip(1.0 - dists / radius, 0.0, 1.0)           # 线性衰减权重
```

> 实测数量级：5 万顶点的矩阵变换，Python for 循环约需秒级，NumPy 向量化在毫秒级。写蒙皮权重工具、Delta 修型（corrective extraction：`delta = (sculpted - skinned) @ inv(skin_matrix)`）时必用。

---

## 5. 实战：批量蒙皮权重计算（Maya）

蒙皮权重是 NumPy 在 Maya 中最典型的应用场景：一个 5 万顶点 × 60 根骨骼的角色，权重数据就是 300 万个 float。用 `pm.skinPercent` 逐顶点读写要几分钟，而 **`MFnSkinCluster` 一次性读写 + NumPy 矩阵化处理**只要不到一秒。

### 5.1 权重数据的形状：(N 顶点, M 骨骼) 矩阵

把整个 skinCluster 的权重看成一个二维矩阵，所有操作都变成矩阵运算：

```python
# weights.shape = (vtx_count, inf_count)
# weights[i, j] = 第 i 个顶点受第 j 根骨骼影响的权重
# 约束：每行之和 == 1.0（归一化）
```

### 5.2 用 OpenMaya 批量读写权重

`MFnSkinCluster.getWeights` 一次调用返回**全部**权重（一维扁平数组），配合 `reshape` 直接得到权重矩阵；写回用 `setWeights` 同样一次完成。

```python
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import numpy as np


def get_skin_data(mesh_name: str, skin_name: str):
    """获取蒙皮权重矩阵及相关句柄。

    Returns:
        (skin_fn, mesh_dag, components, weights, inf_names)
        weights 形状为 (顶点数, 骨骼数)。
    """
    sel = om.MSelectionList()
    sel.add(mesh_name)
    sel.add(skin_name)
    mesh_dag = sel.getDagPath(0)
    skin_fn = oma.MFnSkinCluster(sel.getDependNode(1))

    # 全部顶点组件
    comp_fn = om.MFnSingleIndexedComponent()
    components = comp_fn.create(om.MFn.kMeshVertComponent)
    vtx_count = om.MFnMesh(mesh_dag).numVertices
    comp_fn.addElements(range(vtx_count))

    # 一次性读出全部权重（扁平的 MDoubleArray）
    flat_weights, inf_count = skin_fn.getWeights(mesh_dag, components)
    weights = np.array(flat_weights).reshape(vtx_count, inf_count)

    inf_names = [dag.partialPathName() for dag in skin_fn.influenceObjects()]
    return skin_fn, mesh_dag, components, weights, inf_names


def set_skin_weights(skin_fn, mesh_dag, components, weights: np.ndarray) -> None:
    """把 (N, M) 权重矩阵一次性写回 skinCluster。"""
    inf_count = weights.shape[1]
    inf_indices = om.MIntArray(range(inf_count))
    skin_fn.setWeights(
        mesh_dag,
        components,
        inf_indices,
        om.MDoubleArray(weights.flatten().tolist()),
        False,  # normalize=False，我们自己保证每行归一
    )
```

> 关键点：`getWeights` 返回的扁平数组按**顶点优先**排列（`[v0j0, v0j1, ..., v0jM, v1j0, ...]`），所以 `reshape(vtx_count, inf_count)` 恰好得到权重矩阵；`setWeights` 接收同样的排列。

### 5.3 常用的权重矩阵操作（全部向量化）

拿到 `(N, M)` 矩阵后，常见的权重处理都是几行 NumPy：

```python
# --- 归一化：每行除以行和（防止除零）---
row_sum = weights.sum(axis=1, keepdims=True)          # (N, 1)
weights = weights / np.where(row_sum < 1e-8, 1.0, row_sum)

# --- 剪掉微小权重（清理噪声）并重新归一 ---
weights[weights < 0.001] = 0.0
weights /= weights.sum(axis=1, keepdims=True)

# --- 限制每顶点最大影响数为 4（游戏引擎标配）---
def prune_to_max_influences(weights: np.ndarray, max_inf: int = 4) -> np.ndarray:
    """每行只保留最大的 max_inf 个权重，其余清零后重新归一化。"""
    pruned = weights.copy()
    if weights.shape[1] > max_inf:
        # argpartition 找出每行第 max_inf 大之外的列索引，整行批量清零
        drop_idx = np.argpartition(pruned, -max_inf, axis=1)[:, :-max_inf]
        np.put_along_axis(pruned, drop_idx, 0.0, axis=1)
    return pruned / pruned.sum(axis=1, keepdims=True)

# --- 两根骨骼间转移权重（如合并 twist 骨骼回主骨）---
weights[:, main_idx] += weights[:, twist_idx]
weights[:, twist_idx] = 0.0

# --- 镜像/复制权重：交换左右骨骼对应的列 ---
weights[:, [l_idx, r_idx]] = weights[:, [r_idx, l_idx]]

# --- 统计诊断 ---
influence_per_vtx = (weights > 1e-6).sum(axis=1)      # 每顶点实际影响数
bad_vtx = np.where(np.abs(weights.sum(axis=1) - 1.0) > 1e-5)[0]  # 未归一的顶点
unused_joints = np.where(weights.sum(axis=0) < 1e-6)[0]          # 完全没权重的骨骼
```

> `prune_to_max_influences` 用 `argpartition`（部分排序）而不是 `sort`，5 万顶点也只需几毫秒——这类"每行取 Top-K"的操作是 Python 循环最慢、NumPy 提速最明显的典型。

### 5.4 案例：按距离衰减批量生成初始权重

给一串关节链（如飘带、尾巴）快速生成平滑初始权重：每个顶点对每根骨骼的权重与"顶点到骨骼的距离"成反比，一次算完整张权重矩阵。

```python
def distance_falloff_weights(
    points: np.ndarray, joint_positions: np.ndarray, power: float = 2.0
) -> np.ndarray:
    """按反距离幂衰减计算权重矩阵。

    Args:
        points: (N, 3) 顶点位置.
        joint_positions: (M, 3) 骨骼位置.
        power: 衰减指数，越大权重越"硬"（过渡越锐利）.

    Returns:
        (N, M) 已归一化的权重矩阵.
    """
    # 广播出 (N, M, 3) 的差值，再沿最后一轴求距离 -> (N, M)
    diff = points[:, np.newaxis, :] - joint_positions[np.newaxis, :, :]
    dists = np.linalg.norm(diff, axis=2)
    weights = 1.0 / np.maximum(dists, 1e-6) ** power   # 反距离幂，防除零
    return weights / weights.sum(axis=1, keepdims=True)


# 顶点位置同样用 API 批量获取，不要逐点 xform：
# mesh_fn = om.MFnMesh(mesh_dag)
# points = np.array(mesh_fn.getPoints(om.MSpace.kWorld))[:, :3]  # (N, 3)
```

这里的核心技巧是 **`np.newaxis` 广播**：`(N, 1, 3) - (1, M, 3)` 得到 `(N, M, 3)`，等价于 N×M 次双重循环，但一行完成。

### 5.5 案例：用 NumPy 验证 LBS 蒙皮公式

线性混合蒙皮（Linear Blend Skinning）的公式：

```text
p' = Σ_j  w_ij · (p @ B_j⁻¹ @ W_j)
```

其中 `B_j` 是骨骼 j 的绑定姿势矩阵（`bindPreMatrix` 的逆），`W_j` 是当前世界矩阵。`p @ B_j⁻¹ @ W_j` 就是 Maya skinCluster 里的 **skin matrix**。用 `einsum` 一次算完所有顶点：

```python
def lbs_deform(
    points: np.ndarray, weights: np.ndarray, skin_matrices: np.ndarray
) -> np.ndarray:
    """线性混合蒙皮：批量计算全部顶点的变形结果。

    Args:
        points: (N, 3) 绑定姿势下的顶点位置.
        weights: (N, M) 权重矩阵.
        skin_matrices: (M, 4, 4) 每根骨骼的 skin matrix
            （= inv(bind_world) @ current_world，行向量约定）.

    Returns:
        (N, 3) 变形后的顶点位置.
    """
    points_h = np.hstack([points, np.ones((len(points), 1))])   # (N, 4)
    # 每个顶点经每根骨骼变换的结果：(N, M, 4)
    per_joint = np.einsum("nk,mkl->nml", points_h, skin_matrices)
    # 按权重混合：(N, M) 与 (N, M, 4) 加权求和 -> (N, 4)
    blended = np.einsum("nm,nml->nl", weights, per_joint)
    return blended[:, :3]
```

`np.einsum` 的下标语义：

| 表达式 | 含义 |
| --- | --- |
| `"nk,mkl->nml"` | 顶点 n（4 维 k）× 骨骼 m 的 4×4 矩阵（k 行 l 列）→ 每顶点每骨骼的变换结果 |
| `"nm,nml->nl"` | 权重 (n, m) 对第二个数组的 m 维加权求和 → 混合后的顶点 |

> 用途：不依赖 Maya 求变形结果——提取 corrective 修型的 delta（`delta = sculpted_local - lbs_deform(...)`）、导出前验证权重、离线批处理动画顶点缓存。同一公式在 UE5 里就是 GPU skinning 的 CPU 参考实现。

### 5.6 性能对比（量级参考）

| 操作（5 万顶点 × 60 骨骼） | 逐顶点 `skinPercent` / Python 循环 | API 批量 + NumPy |
| --- | --- | --- |
| 读全部权重 | 分钟级 | < 0.5 s |
| 归一化 / 剪裁 / Top-4 | 秒~分钟级 | 毫秒级 |
| 写回全部权重 | 分钟级 | < 0.5 s |
| LBS 全网格变形 | 秒级 | 毫秒级 |

经验法则：**和 Maya 的交互（读/写）只做两次，中间所有处理都留在 NumPy 里完成**。

---

## 小结

- **向量**：`norm` 求长、`dot` 判方向/投影、`cross` 建正交系；案例——Pole Vector 定位。
- **矩阵**：`@` 矩阵乘（勿用 `*`）、`inv` 对应 `worldInverseMatrix`、`det < 0` 说明有镜像；4×4 行向量约定与 Maya/UE 一致，平移在第 4 行；案例——LookAt 矩阵、TRS 组装/分解。
- **四元数**：`(x, y, z, w)` 顺序与 Maya/UE 一致；乘法即旋转叠加、共轭即逆；案例——Slerp 插值、Swing-Twist 分解提取扭转角。
- **向量化**：批量顶点/权重计算用 `(N, 3)` 数组一次算完，避免 Python 循环。
- **蒙皮权重**：`MFnSkinCluster.getWeights/setWeights` 一次读写全部权重，`reshape(N, M)` 成矩阵后归一化、剪裁、Top-K、镜像都是几行向量化代码；`einsum` 可直接实现 LBS 公式；与 Maya 只交互两次（读、写），处理全部留在 NumPy。
- 生产环境若允许第三方库，`scipy.spatial.transform.Rotation` 提供了经过验证的四元数/欧拉角/矩阵互转，可减少手写数学的出错面。
