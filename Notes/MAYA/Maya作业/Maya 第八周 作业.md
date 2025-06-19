# Maya 第八周 作业

![](attachments/Maya%20第八周%20作业_image_0.png)

[單壹崽崽](https://www.jianshu.com/u/92cf571d45d7)

关注

2020.02.03 19:19:01字数 140阅读 594

lesson21_Maya API 的全局操作方法 - MGlobal

![](attachments/Maya%20第八周%20作业_image_1.png)

image.png

![](attachments/Maya%20第八周%20作业_image_2.png)

image.png

![](attachments/Maya%20第八周%20作业_image_3.png)

image.png

可以用截图软件看到maya视图的大小，比如我测出来是大约：723 X 556

那么用maya的openMayaUI 模块下的M3dView中的 portWidth 和 portHeight 也可以精确的测量出视图的大小：

```python
import maya.OpenMayaUI as omUI
view = omUI.M3dView.active3dView()
view.portWidth() # 707
view.portHeight() # 549
```

然后用MGlobal下的selectFromScreen 来选择视窗范围内的物体：

比如选择正中央的一块区域：

![](attachments/Maya%20第八周%20作业_image_4.png)

image.png

![](attachments/Maya%20第八周%20作业_image_5.png)

image.png

```css
import maya.OpenMaya as om
om.MGlobal.selectFromScreen(310, 220, 380, 320, om.MGlobal.kReplaceList)
```

2.lesson22_Maya API 的文件操作 - MFileIO

![](attachments/Maya%20第八周%20作业_image_6.png)

image.png

![](attachments/Maya%20第八周%20作业_image_7.png)

image.png

![](attachments/Maya%20第八周%20作业_image_8.png)

image.png

```python
import maya.OpenMaya as om
import maya.cmds as cmds
sg_node = cmds.ls(type='shadingEngine')
cmds.select(sg_node, ne=True)
om.MFileIO.exportSelected("C:\Users\KangTa\Desktop\sg_tes.ma", 'mayaAscii')
```

扩展下导出场景中使用过的材质球

```python
import maya.OpenMaya as om
import maya.cmds as cmds
# 列出场景中使用的材质球
def get_used_materials_in_scene():
    """list the material used in scene
    """
    
    for shading_engine in cmds.ls(type='shadingEngine'):
        if cmds.sets(shading_engine, q=True):
            for material in cmds.ls(cmds.listConnections(shading_engine), mat=True):
                yield material
all_material = list(get_used_materials_in_scene())
cmds.select(all_material, r=True)
om.MFileIO.exportSelected("C:/Users/KangTa/Desktop/sg_test.ma", 'mayaAscii')
```

3.lesson23_Maya API 中的节点迭代器和函数类

![](attachments/Maya%20第八周%20作业_image_9.png)

image.png

```csharp
m_sel = om.MSelectionList()
mat_iter = om.MItDependencyNodes(om.MFn.kShadingEngine)
while not mat_iter.isDone():
    m_sel.add(mat_iter.item())
    # m_sel.add(om.MFnDependencyNode(mat_iter.item()).name())
    mat_iter.next()
om.MGlobal.setActiveSelectionList(m_sel)
om.MFileIO.exportSelected("C:/Users/KangTa/Desktop/sg_test.ma", 'mayaAscii')
```