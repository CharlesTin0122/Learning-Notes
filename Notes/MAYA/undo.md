在 Maya 的 Python API 中，`pm.undoInfo()` 和 `pm.UndoChunk()` 是 PyMEL 提供的工具，用于管理 Maya 的撤销和重做功能。它们可以帮助开发者在脚本中控制操作的撤销行为，特别是在执行一系列命令时希望将它们组合为一个单一的撤销操作。以下是对这两者的详细介绍及其使用方法。

### 1. `pm.undoInfo()`
`pm.undoInfo()` 是 PyMEL 中对 Maya 原生命令 `maya.cmds.undoInfo` 的封装，用于控制和查询撤销/重做队列的参数。它可以设置撤销队列的状态、长度，打开或关闭撤销块（chunk），以及查询撤销或重做队列的内容。

#### 主要功能
- **控制撤销状态**：开启或关闭撤销功能。
- **设置队列长度**：限制撤销队列的最大条目数，或设置为无限。
- **管理撤销块**：打开或关闭一个撤销块（chunk），以将多个操作组合为一个单一的撤销步骤。
- **查询队列信息**：获取当前撤销或重做队列的状态、长度或内容。

#### 常用参数（Flags）
以下是 `pm.undoInfo()` 的主要参数：
- `state` (布尔值)：开启 (`True`) 或关闭 (`False`) 撤销功能。
- `infinity` (布尔值)：设置撤销队列长度为无限 (`True`) 或有限 (`False`)。
- `length` (无符号整数)：设置撤销队列的最大条目数（与 `infinity=False` 配合使用）。
- `openChunk` (布尔值)：打开一个新的撤销块，之后的所有操作将被视为一个整体。
- `closeChunk` (布尔值)：关闭当前打开的撤销块。
- `chunkName` (字符串)：为撤销块指定名称，便于识别。
- `undoName` (字符串)：查询将要撤销的操作名称。
- `redoName` (字符串)：查询将要重做的操作名称。
- `undoQueueEmpty` (布尔值)：查询撤销队列是否为空。
- `redoQueueEmpty` (布尔值)：查询重做队列是否为空。
- `printQueue` (布尔值)：打印撤销队列内容。
- `printRedoQueue` (布尔值)：打印重做队列内容。

#### 返回值
- 如果查询模式（`query=True`）下无其他标志，返回撤销队列中的项目数（整数）。
- 根据查询的标志，返回对应类型（如字符串、整数或布尔值）。

#### 使用示例
```python
import pymel.core as pm

# 开启撤销功能，设置无限队列长度
pm.undoInfo(state=True, infinity=True)

# 设置有限队列长度为 200
pm.undoInfo(state=True, infinity=False, length=200)

# 关闭撤销功能
pm.undoInfo(state=False)

# 查询当前队列长度
length = pm.undoInfo(query=True, length=True)
print(f"Undo queue length: {length}")

# 查询撤销队列中的项目数
queue_size = pm.undoInfo(query=True)
print(f"Items in undo queue: {queue_size}")

# 打开一个撤销块
pm.undoInfo(openChunk=True, chunkName="myOperation")

# 执行一些操作
pm.createNode("transform", name="testNode1")
pm.createNode("transform", name="testNode2")

# 关闭撤销块
pm.undoInfo(closeChunk=True)
```

**说明**：
- 上述代码中，`testNode1` 和 `testNode2` 的创建被包含在一个名为 `myOperation` 的撤销块中。执行 `pm.undo()` 将一次性撤销这两个节点的创建，而不是逐个撤销。
- 使用 `openChunk` 和 `closeChunk` 时要小心，确保成对使用，否则可能导致撤销队列状态异常。

#### 注意事项
- 如果在打开一个撤销块后发生错误，未关闭的块可能导致撤销队列出现问题。建议使用 `try...finally` 或上下文管理器（如 `pm.UndoChunk`）来确保块正确关闭。
- 关闭撤销功能（`state=False`）会清空撤销队列，需谨慎使用。

### 2. `pm.UndoChunk()`
`pm.UndoChunk()` 是 PyMEL 提供的一个上下文管理器，专门用于将一系列操作封装在一个单一的撤销块中。它是对 `pm.undoInfo(openChunk=True)` 和 `pm.undoInfo(closeChunk=True)` 的简化封装，结合 Python 的 `with` 语句使用，确保撤销块在代码块执行完毕后自动关闭，即使发生错误。

#### 主要功能
- **自动管理撤销块**：在 `with` 语句的代码块中，所有 Maya 命令都被记录在一个撤销块中，执行 `pm.undo()` 可一次性撤销整个块。
- **错误安全**：即使代码块中发生异常，`pm.UndoChunk()` 也能保证撤销块被正确关闭，避免队列状态问题。

#### 使用方法
`pm.UndoChunk()` 通常与 Python 的 `with` 语句一起使用，语法如下：
```python
with pm.UndoChunk():
    # 在此执行多个 Maya 命令
    pm.createNode("transform", name="node1")
    pm.createNode("transform", name="node2")
    # 其他操作...
```

#### 使用示例
```python
import pymel.core as pm

# 检查初始状态
print(pm.ls("MyNode*", type="transform"))  # 输出: []

# 使用 UndoChunk 创建多个节点
with pm.UndoChunk():
    pm.createNode("transform", name="MyNode1")
    pm.createNode("transform", name="MyNode2")
    pm.createNode("transform", name="MyNode3")

# 检查创建结果
print(pm.ls("MyNode*", type="transform"))  # 输出: [nt.Transform(u'MyNode1'), nt.Transform(u'MyNode2'), nt.Transform(u'MyNode3')]

# 执行撤销
pm.undo()  # 一次性撤销所有三个节点的创建

# 检查撤销后状态
print(pm.ls("MyNode*", type="transform"))  # 输出: []
```

**说明**：
- 在 `with pm.UndoChunk():` 内的所有操作（创建三个节点）被视为一个单一的撤销单元。调用 `pm.undo()` 会同时删除所有三个节点。
- `pm.UndoChunk()` 自动处理 `openChunk` 和 `closeChunk`，无需手动调用 `pm.undoInfo()`。

#### 高级示例：结合错误处理
```python
import pymel.core as pm

try:
    with pm.UndoChunk():
        pm.createNode("transform", name="MyNode1")
        pm.createNode("transform", name="MyNode2")
        raise RuntimeError("模拟错误")
except RuntimeError as e:
    print(f"错误发生: {e}")

# 即使发生错误，撤销块已正确关闭
print(pm.ls("MyNode*", type="transform"))  # 输出: []
```

**说明**：
- 即使代码块中抛出异常，`pm.UndoChunk()` 确保撤销块被关闭，队列不会出现问题。
- 这里即使错误发生，`MyNode1` 和 `MyNode2` 的创建也会被撤销。

### 两者的关系与选择
- **`pm.undoInfo()`** 提供了更细粒度的控制，适合需要手动管理撤销队列或查询队列状态的场景。例如，设置队列长度、查询撤销操作名称等。
- **`pm.UndoChunk()`** 是更高层次的工具，专为简化撤销块管理设计，适合大多数需要将多个操作组合为单一撤销的场景。它使用上下文管理器，代码更简洁且更安全。

### 最佳实践
1. **优先使用 `pm.UndoChunk()`**：
   - 对于大多数脚本，推荐使用 `pm.UndoChunk()`，因为它自动管理撤销块，减少错误风险。
   - 尤其在执行一系列命令（如创建节点、设置属性等）时，使用 `with pm.UndoChunk():` 能确保操作被正确分组。

2. **谨慎使用 `pm.undoInfo()`**：
   - 如果需要手动控制撤销块（如动态决定是否打开/关闭），可以使用 `pm.undoInfo(openChunk=True)` 和 `pm.undoInfo(closeChunk=True)`。
   - 总是确保 `openChunk` 和 `closeChunk` 成对出现，建议使用 `try...finally` 结构：
     ```python
     pm.undoInfo(openChunk=True, chunkName="myChunk")
     try:
         # 操作
         pm.createNode("transform", name="testNode")
     finally:
         pm.undoInfo(closeChunk=True)
     ```

3. **避免撤销队列问题**：
   - 不要在撤销块打开时执行非必要操作（如 GUI 更新），否则可能引入“空白”撤销条目，导致多次按 `Ctrl+Z` 才能撤销。
   - 如果发现撤销需要多次操作，检查代码中是否有未关闭的撤销块或额外命令被意外记录。

4. **结合 Maya API**：
   - 如果使用 Maya Python API（`maya.api.OpenMaya`）执行操作（如 `MDagModifier`），这些操作默认不进入撤销队列。需要自定义插件或使用第三方工具（如 `apiundo`）来支持撤销功能。[](https://github.com/mottosso/apiundo)

### 注意事项
- **撤销块嵌套**：Maya 支持嵌套撤销块，但嵌套过多可能导致性能问题或队列混乱，建议尽量保持简单。
- **非撤销操作**：某些 Maya 命令（如某些 UI 操作）可能不被撤销队列支持，需通过测试确认。
- **性能**：大量撤销操作可能影响性能，尤其在无限队列模式（`infinity=True`）下，注意监控内存使用。
- **调试**：使用 `pm.undoInfo(printQueue=True)` 或 `pm.undoInfo(printRedoQueue=True)` 查看撤销/重做队列内容，便于调试。

### 总结
- **`pm.undoInfo()`**：提供灵活的撤销队列管理，适合需要精细控制或查询队列状态的场景。
- **`pm.UndoChunk()`**：简化和自动化撤销块管理，推荐用于大多数脚本任务，代码更简洁且错误安全。
- **使用建议**：优先选择 `pm.UndoChunk()` 用于日常脚本开发；当需要特殊控制（如设置队列长度或查询状态）时，使用 `pm.undoInfo()`。

通过合理使用这两者，可以有效管理 Maya 中的撤销和重做操作，提升脚本的健壮性和用户体验。[](https://help.autodesk.com/cloudhelp/2022/ENU/Maya-Tech-Docs/PyMel/generated/classes/pymel.core.system/pymel.core.system.UndoChunk.html)[](https://help.autodesk.com/cloudhelp/2020/ENU/Maya-Tech-Docs/PyMel/generated/functions/pymel.core.system/pymel.core.system.undoInfo.html)