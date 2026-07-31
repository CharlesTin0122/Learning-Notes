---
tags:
  - Maya
  - Rigging
  - SkinWeights
  - 第三方插件
---

# brTransferWeights 使用指南

> brTransferWeights 是 braverabbit（Ingo Clemens）出品的**骨骼间权重定向传输笔刷**，与 [brSmoothWeights](brSmoothWeights使用指南.md) 打包在同一个插件中（装一个即得两个工具）。

## 一、它解决什么问题

Maya 自带的 Paint Skin Weights 一次只能对**单个** influence 做 add / replace / scale——改动一根骨骼的权重后，多出或缺少的部分会按归一化规则**不受控地**分给其他所有骨骼，经常污染已经刷好的区域。

brTransferWeights 的思路完全不同：

- **权重只在指定的一对骨骼（Source → Destination）之间流动**
- 其他所有 influence 的权重**原封不动**
- 相当于"定向输血"，不会弄脏第三方骨骼

### 典型场景

1. **多骨交界区调整归属**：如肩膀/锁骨区域，把一部分权重从 `clavicle` 挪到 `shoulder`，而不影响 `spine` 上已刷好的权重
2. **扭转骨（twist joint）与主骨之间重新分配比例**
3. **修复自动绑定结果**：某根骨骼"抢"了邻近骨骼权重的区域，定向搬回去

## 二、安装

1. 从 [Gumroad](https://braverabbit.gumroad.com/l/brSmoothWeightsMaya) 下载（**注意：原 GitHub 仓库 IngoClemens/brSmoothWeights 已停止维护**，插件含全部源码已迁移至 Gumroad 发布）
2. 解压后把 `dragDropInstaller.py` 拖进 Maya 主窗口，按向导安装（模块化安装，所有文件集中管理，并生成安装日志）
3. 重启 Maya 后，**Rigging 菜单集 → Skin 菜单**下会出现两个新菜单项：
   - **Paint Smooth Weights Tool**
   - **Paint Transfer Weights Tool** ← 本工具
4. 如果菜单项没出现（启动脚本未被执行），运行 MEL 命令：

```mel
brSmoothWeightsCreateMenuItems
```

该命令也可用来创建工具架（shelf）按钮。

## 三、基本使用流程

1. **选中蒙皮网格**，激活 **Paint Transfer Weights Tool**（网格必须在激活工具时处于选中状态）
2. 打开工具设置（Tool Settings），在 **influence 列表中多选两项**，即指定 Source 和 Destination 骨骼
3. 两个 influence 输入框之间有一个**方向箭头按钮**，点击可快速反转传输方向（Source ⇄ Destination）
4. 在网格上**左键拖拽刷权重**：每一笔按 Strength 把笔刷范围内顶点的权重从 Source 挪到 Destination
5. 传输模式两种：
   - **Add（默认）**：Source 的权重*叠加*到 Destination 已有权重上
   - **Replace**：直接用传输值*完全替换* Destination 原有权重

## 四、笔刷交互（与 brSmoothWeights 一致）

| 操作 | 功能 |
|---|---|
| 左键拖拽 | 刷权重传输 |
| 中键左右拖拽 | 调整笔刷大小（Size） |
| 中键上下拖拽 | 调整笔刷强度（Strength） |
| Shift + 拖拽 | 框选顶点（限制作用范围） |
| Ctrl + 拖拽 | 减选顶点 |
| Shift + Ctrl + 左键 | 清空顶点选择 |

> 注：笔刷圆圈只在按住鼠标时显示（Qt 实现限制，官方已知问题）。

## 五、主要工具选项

以下选项与 brSmoothWeights 共用同一套笔刷框架：

- **Size / Strength**：笔刷大小（世界单位）/ 每笔传输强度
- **Affect Selected**：只作用于已选顶点；关闭时则只作用于*未选中*顶点（用选区当"遮罩"保护区域）
- **Ignore Lock**：无视 influence 的锁定状态强制修改
- **Flood**：对当前选择（未选则全网格）按 Strength 一次性整体执行传输，适合批量精确操作
- **Depth Start / Depth**：穿透深度。Depth Start=2 可跳过最前面一层只刷背面；Depth=2 可同时刷正反两面（如手臂内侧贴合处，姿势网格可能需要 3+）
- **Volume / Range**：体积采样模式（原理同 [brSmoothWeights 的 VolumeSmoothing](brSmoothWeights使用指南.md)），按空间距离而非拓扑连接采样邻居，可跨 shell 传输；Range 为相对笔刷尺寸的采样半径比例。慎用——空间贴近但逻辑分离的部位（嘴唇、并拢手指）容易串权重
- **Draw Brush / Brush Color / Line Width**：笔刷圈显示开关、颜色、线宽

## 六、与 brSmoothWeights 的组合拳

实际刷权重工作流中两个工具配合使用：

1. **brTransferWeights** 先把权重在正确的骨骼之间分配到位 → 解决**权重归属**问题
2. **brSmoothWeights** 再把过渡刷顺 → 解决**权重梯度**问题

两者共同优点：尊重 influence 锁定、完整撤销支持、多线程实现，大网格上性能远好于 Maya 原生笔刷。

## 参考

- 官方 Wiki：https://github.com/IngoClemens/brSmoothWeights/wiki （仓库已归档但文档仍可读）
- 下载页：https://braverabbit.gumroad.com/l/brSmoothWeightsMaya
- 功能演示视频（brSmoothWeights）：https://youtu.be/cT5zW-byR_c
