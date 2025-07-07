# Maya：第四周 作业

![](attachments/Maya：第四周%20作业_image_0.png)

[單壹崽崽](https://www.jianshu.com/u/92cf571d45d7)

关注

2019.12.23 21:02:14字数 0阅读 352

![](attachments/Maya：第四周%20作业_image_1.png)

image.png

![](attachments/Maya：第四周%20作业_image_2.png)

参考操作.gif

```python
import maya.cmds as cmds
def reference_tool(file_path, namespace='', reference_mode='import', reference_number=1):
    """
    :param file_path:
    :param namespace:
    :param reference_mode:
    :param reference_number:
    :return:
    """
    ref_file_list = []
    if reference_mode == 'import':
        ref_file_list = [cmds.file(file_path, r=True, ns=namespace) for i in range(reference_number)]
    if reference_mode == 'remove':
        ref_file_list = cmds.file(file_path, rr=True)
    if reference_mode == 'unload':
        ref_file_list = cmds.file(file_path, ur=True)
    if reference_mode == 'load':
        ref_file_list = cmds.file(file_path, lr=True)
    return ref_file_list
source_file = [(r'C:\Users\KangTa\Desktop\test\box.ma', 'A'),
               (r'C:\Users\KangTa\Desktop\test\pSphere.ma', 'B')]
all_ref_list = []
for fp, ns in source_file:
    test_ref_list = reference_tool(file_path=fp,
                                   namespace=ns,
                                   reference_mode='import',
                                   reference_number=3)
    for r in test_ref_list:
        all_ref_list.append(r)
for ref_f in all_ref_list[2:5]:
    reference_tool(ref_f, reference_mode='unload')
for ref_f in all_ref_list[2:5]:
    reference_tool(ref_f, reference_mode='load')
for ref_f in all_ref_list:
    reference_tool(ref_f, reference_mode='remove')
```

![](attachments/Maya：第四周%20作业_image_3.png)

image.png

![](attachments/Maya：第四周%20作业_image_4.png)

image.png

![](attachments/Maya：第四周%20作业_image_5.png)

创建小球.gif

```python
import maya.cmds as cmds
pSphere_tool_window_name = 'pSphere_window'
if cmds.window(pSphere_tool_window_name, q=True, ex=True):
    cmds.deleteUI(pSphere_tool_window_name)
p_win = cmds.window(pSphere_tool_window_name, t='Create Poly Sphere Tool', wh=(300, 190))
main_layout = cmds.columnLayout(w=350, h=190, adj=True)
frame_layout = cmds.frameLayout('frameLayout1_ui', l=' Create Poly Sphere ', en=True, h=180, vis=True, bgc=[0.0, 0.0, 0.0], cl=False, cll=False, p=main_layout)
name_layout = cmds.rowLayout(nc=2, p=frame_layout)
cmds.text(l='     Name :      ', p=name_layout)
name_field = cmds.textField(w=100, tx='pSphere', p=name_layout)
number_layout = cmds.rowLayout(nc=2, p=frame_layout)
cmds.text(l='     Number :     ', p=number_layout)
number_int_field = cmds.intField(w=100, min=1, p=number_layout)
radius_layout = cmds.rowLayout(nc=2, p=frame_layout)
cmds.text(l='     Radius :       ', p=radius_layout)
radius_float_field = cmds.floatField(w=100, v=1.0, min=0.001, p=radius_layout)
cmds.separator(p=frame_layout)
create_btn = cmds.button(h=50, bgc=[0.6, 0.7, 0.6], l='Create', c=create_btn_cmd, p=frame_layout)
cmds.showWindow(p_win)
def create_btn_cmd():
    name_str = cmds.textField(name_field, q=True, tx=True)
    num = cmds.intField(number_int_field, q=True, v=True)
    radius = cmds.floatField(radius_float_field, q=True, v=True)
    for i in range(num):
        cmds.polySphere(n='{}_{}_Mesh'.format(name_str, i), r=radius)
```

![](attachments/Maya：第四周%20作业_image_6.png)

image.png

![](attachments/Maya：第四周%20作业_image_7.png)

image.png

![](attachments/Maya：第四周%20作业_image_8.png)

playblast.gif

```php
my_cam = 'my_camera'
main_panel = cmds.getPanel(vis=True)[0]
cmds.modelPanel(main_panel, e=True, cam=my_cam)
cmds.modelEditor(main_panel, e=True, alo=False)
cmds.modelEditor(main_panel, e=True, pm=True)
cmds.playblast()
```