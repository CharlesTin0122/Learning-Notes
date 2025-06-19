# Maya 第九周 作业

![](attachments/Maya%20第九周%20作业_image_0.png)

[單壹崽崽](https://www.jianshu.com/u/92cf571d45d7)

关注

2020.02.15 00:29:10字数 38阅读 419

1.lesson25_Maya API 中的多边形处理 - MFnMesh/MItMesh

![](attachments/Maya%20第九周%20作业_image_1.png)

image.png

2.lesson26_Maya API 中的指针 - MScriptUtil

![](attachments/Maya%20第九周%20作业_image_2.png)

image.png

![](attachments/Maya%20第九周%20作业_image_3.png)

image.png

```python
def get_vtx_uv_point(obj, vtx_index):
    """
    """
    shape_mobj = pm.PyNode(obj).getShape().__apimobject__()
    mfn = om.MFnMesh(shape_mobj)
    s_util = om.MScriptUtil()
    uv_ptr = s_util.asFloat2Ptr()
    m_point = om.MPoint()
    mfn.getPoint(vtx_index, m_point)
    mfn.getUVAtPoint(m_point, uv_ptr)
    u_value = s_util.getFloat2ArrayItem(uv_ptr, 0, 0)
    v_value = s_util.getFloat2ArrayItem(uv_ptr, 0, 1)
    return (u_value, v_value)
get_vtx_uv_point('pSphere2', 2)
```

3.lesson27_Maya API 中的事件捕获 - MMessage

![](attachments/Maya%20第九周%20作业_image_4.png)

image.png

写法1：

```csharp
import maya.OpenMaya as om
import maya.cmds as cmds
from functools import partial
def rename_ref_func(*args, **kwages):
    new_name_space = kwages.get('new_name_space')
    file_path = args[1].resolvedFullName() 
    cmds.file(file_path, e=1, namespace=new_name_space)
ref_callback_id  = om.MSceneMessage.addReferenceCallback(om.MSceneMessage.kAfterCreateReference, 
                                                         partial(rename_ref_func,new_name_space='Test'))
# remove
om.MMessage.removeCallback(ref_callback_id)
```

写法2：

```python
import maya.OpenMaya as om
import maya.cmds as cmds
from functools import partial
def rename_ref_func(new_name_space, *args):
    file_path = args[1].resolvedFullName() 
    cmds.file(file_path, e=1, namespace=new_name_space)
ref_callback_id  = om.MSceneMessage.addReferenceCallback(om.MSceneMessage.kAfterCreateReference, 
                                                         partial(rename_ref_func, 'Test'))
# remove
om.MMessage.removeCallback(ref_callback_id)
```