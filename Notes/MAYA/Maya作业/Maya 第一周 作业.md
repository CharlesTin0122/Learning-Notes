lesson0_初识帮助文档

![](attachments/Maya%20第一周%20作业_image_0.png)

image.png

```python
import maya.cmds as cmds
# circle
cmds.circle()
# circle -r 2
cmds.circle(r=2)
# circle -r 2 -nr 0 1 0
cmds.circle(r=2, nr=(0, 1, 0))
# curve -d 1 -p -2 0 -2 -p 3 0 -2 -p -2 0 3 -p -2 0 -2
cmds.curve(d=1, p=[(-2, 0, -2), (3, 0, -2), (-2, 0, 3), (-2, 0, -2)] )
```

lesson1_获取场景内操作对象

![](attachments/Maya%20第一周%20作业_image_1.png)

image.png

```python
import maya.cmds as cmds
nurbs_surface_objs = cmds.ls(type='nurbsSurface', long=True)
if nurbs_surface_objs:
    new_nurbs_surface_objs = [cmds.rename(obj, 'nurbs_{}'.format(obj)) for obj in nurbs_surface_objs]
```

lesson2_获取、改变场景内层级关系

![](attachments/Maya%20第一周%20作业_image_2.png)

image.png

```python
import maya.cmds as cmds
def get_obj_type(objs=None):
    """ Get Object Type Group
    :param objs: None or list
    :return: list
    """
    if not objs:
        objs = cmds.ls(sl=True, tr=True, long=True)
    all_obj_type = []
    if cmds.objExists(objs[0]):
        cmds.inViewMessage(
            amg="<hl> Warning: The {} Not Exists, Please Check The objs Argument ! Must Is List </hl>.".format(objs[0]),
            pos='midCenter', fade=True)
        return False
    for obj in objs:
        obj_shape = cmds.listRelatives(obj, s=True, f=True)
        if obj_shape:
            shape_type = cmds.objectType(obj_shape[0])
            all_obj_type.append(shape_type)
        else:
            all_obj_type.append(cmds.objectType(obj))
    all_obj_type = list(set(all_obj_type))
    return all_obj_type
def parent_type_group(objs=None, group_prefix='', group_suffix='_Grp', parent_to_group=True):
    """ Create Type Group For Objects
    :param objs: None Or List
    :param group_prefix: Str
    :param group_suffix: Str
    :param parent_to_group: Bool As a child object
    :return:
    """
    if not objs:
        objs = cmds.ls(sl=True, tr=True, long=True)
    if cmds.objExists(objs[0]):
        cmds.inViewMessage(
            amg="<hl> Warning: The {} Not Exists, Please Check The objs Argument ! Must Is List </hl>.".format(objs[0]),
            pos='midCenter', fade=True)
        return False
    all_obj_type = get_obj_type(objs)
    type_group = [cmds.group(em=True, name='{}{}{}'.format(group_prefix, obj_type, group_suffix))
                  for obj_type in all_obj_type]
    grp_dict = dict(zip(all_obj_type, type_group))
    for obj in objs:
        obj_shape = cmds.listRelatives(obj, s=True, f=True)
        if obj_shape:
            shape_type = cmds.objectType(obj_shape[0])
            if parent_to_group:
                cmds.parent(obj, grp_dict[shape_type])
        else:
            shape_type = cmds.objectType(obj)
            if parent_to_group:
                cmds.parent(obj, grp_dict[shape_type])
    return type_group
parent_type_group(['joint1', 'joint2'], group_prefix='Test_')
```

lesson3_获取、更改物体位置

![](attachments/Maya%20第一周%20作业_image_3.png)

image.png

```python
import itertools
import maya.cmds as cmds
def copy_pose(target_obj=None, source_obj=None, translation=True, rotation=True, scale=True, adsorb=False):
    """ Copy Pose
    :param target_obj: list
    :param source_obj: list
    :param translation: bool
    :param rotation: bool
    :param scale: bool
    :param adsorb: bool
    :return:
    """
    warning_str = 'The {} Or {} Not Exists, Please Check The objs Argument ! Must Is List'.format(target_obj[0],
                                                                                                  source_obj[0])
    if not cmds.objExists(target_obj[0]) or not cmds.objExists(source_obj[0]):
        cmds.inViewMessage(amg="<hl> Warning: {}  </hl>.".format(warning_str), pos='midCenter', fade=True)
        return False
    for i, item in enumerate(source_obj):
        source_obj_t = cmds.xform(item, q=True, t=True, ws=adsorb)
        source_obj_ro = cmds.xform(item, q=True, ro=True, ws=adsorb)
        source_obj_scale = cmds.getAttr('{}.s'.format(item))[0]
        if translation:
            cmds.xform(target_obj[i], t=source_obj_t, ws=adsorb)
        if rotation:
            cmds.xform(target_obj[i], ro=source_obj_ro, ws=adsorb)
        if scale:
            try:
                cmds.setAttr('{}.s'.format(target_obj[i]), source_obj_scale[0],
                             source_obj_scale[1], source_obj_scale[2])
            except Exception as inst:
                inset_str = " Can't Set {}'s Scale Attribute !!!".format(target_obj[i])
                print(inset_str)
sel_obj = cmds.ls(sl=True, long=True)
name_space_list = [n for n in cmds.namespaceInfo(lon=1) if n not in ('UI', 'shared')]
ref_obj_list = []
for obj in sel_obj:
    str_combination = [comb_item for comb_item in itertools.product(name_space_list, [obj])]
    for item in str_combination:
        ref_obj_list.append('|{}:{}'.format(item[0], item[1][1:]))
sel_ref_obj_list = [ref_obj for ref_obj in ref_obj_list if cmds.objExists(ref_obj)]
copy_pose(sel_obj, sel_ref_obj_list)
```

作者：單壹崽崽

链接：[https://www.jianshu.com/p/4292c8645096](https://www.jianshu.com/p/4292c8645096)

来源：简书

著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。