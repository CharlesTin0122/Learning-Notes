# Maya: 第三周 作业

![](attachments/Maya%20第三周%20作业_image_0.png)

[單壹崽崽](https://www.jianshu.com/u/92cf571d45d7)

关注

2019.12.16 14:19:46字数 416阅读 718

lesson7_轻松获取节点连接关系

![](attachments/Maya%20第三周%20作业_image_1.png)

image.png

![](attachments/Maya%20第三周%20作业_image_2.png)

动画数据转移.gif

思路：1.找出与源物体的相连接的animCurve节点（判断出哪些属性有K帧）

2.通过animCurve节点找出属性接口的完整连接关系

3.把完整连接关系的列表中的来源物体名字替换为目标物体名字

4.用参数控制是否断开来源物体连接

5.连接目标物体

```python
import maya.cmds as cmds
def transfer_keyframe_connection(source_obj, target_obj, source_disconnect=True):
    """Transfer Keyframe Connection From Source Object To Target Object
    :param source_obj: Str
    :param target_obj: Str
    :param source_disconnect: Bool. 
    :return:
    """
    source_anim_curves = cmds.listConnections(source_obj, t="animCurve")
    if not source_anim_curves:
        cmds.inViewMessage(
            amg="<hl> Warning: The Source Object Has Not Any Keyframe ! </hl>.",
            pos='midCenter', fade=True)
        return False
    source_obj_keyframe_connection = [cmds.listConnections(anim_crv, c=True, p=True) for anim_crv in source_anim_curves]       
    target_obj_keyframe_connection = [[c[0], c[1].replace(c[1].split('.')[0], target_obj)] for c in 
                                      source_obj_keyframe_connection]
    for index, items in enumerate(source_obj_keyframe_connection):
        if source_disconnect:
            cmds.disconnectAttr(items[0], items[1])
        cmds.connectAttr(target_obj_keyframe_connection[index][0], target_obj_keyframe_connection[index][1])
transfer_keyframe_connection('pSphere1', 'pCube1', source_disconnect=True)
```

lesson8_几种物体约束的命令

![](attachments/Maya%20第三周%20作业_image_3.png)

image.png

![](attachments/Maya%20第三周%20作业_image_4.png)

控制器.gif

思路：

1.利用约束的保持偏移的属性来吸附到物体坐标以及方向

2.独立写一个函数来处理控制器形态的改变，如果没有指定控制器形态则默认形态是圆环控制器

3.利用参数控制控制器是否对物体有父子约束，缩放约束以及偏移组的个数

```python
import maya.cmds as cmds
def transfer_curve_shape(source_obj, target_obj):
    """Transfer Shapes From Source Object To Target Object
    :param source_obj:str. curve object
    :param target_obj:str. curve object
    :return:str
    """
    target_obj_shapes = cmds.listRelatives(target_obj, s=True)
    if not target_obj_shapes:
        return False
    cmds.delete(target_obj_shapes)
    temp_source_obj = cmds.duplicate(source_obj, n='_{}_TEMP_CURVE'.format(source_obj))[0]
    if cmds.listRelatives(temp_source_obj, p=True):
        cmds.parent(temp_source_obj, w=True)
    temp_source_obj_shapes = cmds.listRelatives(temp_source_obj, s=True)
    if not temp_source_obj_shapes:
        return False
    cmds.xform(temp_source_obj, cp=1)
    temp_world_grp = cmds.group(em=True)
    cmds.delete(cmds.parentConstraint(temp_world_grp, temp_source_obj))
    cmds.makeIdentity(temp_source_obj, n=0, s=1, r=1, t=1, apply=True, pn=1)
    for s in temp_source_obj_shapes:
        cmds.parent(s, target_obj, s=True, add=True)
    cmds.delete(temp_source_obj, temp_world_grp)
    new_target_obj_shapes = cmds.listRelatives(target_obj, s=True)
    for index, s in enumerate(new_target_obj_shapes):
        cmds.rename(s, '{}Shape{}'.format(target_obj, index + 1))
    return target_obj
def controller(target_obj, controller_shape=None, controller_name=None, offset_group_number=0,
               object_mode=True, parent_constrain=True, scale_constrain=False):
    """Create controller for object
    :param target_obj: Str
    :param controller_name: Str
    :param controller_shape: Str . You Can Custom Controller Shape
    :param offset_group_number: Int
    :param object_mode: Bool.
    :param parent_constrain: Bool.
    :param scale_constrain: Bool.
    :return: list. Controller Name And Offset Groups
    """
    if not controller_name:
        controller_name = '{}_control'.format(target_obj)
    control_grp = cmds.group(em=True, n='{}_grp'.format(controller_name))
    default_con = cmds.circle(n=controller_name, nr=(0, 1, 0))
    if controller_shape:
        transfer_curve_shape(controller_shape, default_con[0])
    cmds.parent(default_con[0], control_grp)
    offset_grp = []
    if offset_group_number > 0:
        for i in range(offset_group_number):
            temp_grp = cmds.group(default_con[0],
                                  name='{}_offset_{}_grp'.format(default_con[0], offset_group_number - i))
            offset_grp.append(temp_grp)
    offset_grp.append(control_grp)
    
    if object_mode:
        cmds.delete(cmds.parentConstraint(target_obj, control_grp))
    if parent_constrain:
        cmds.parentConstraint(default_con[0], target_obj, mo=True, weight=True)
    if scale_constrain:
        cmds.scaleConstraint(default_con[0], target_obj, mo=True, weight=True)
    
    return [default_con[0], offset_grp]
controller('joint1', 
           controller_shape='nurbsCircle1', 
           controller_name='test_joint_ctrl',
           object_mode=True, 
           parent_constrain=True, 
           scale_constrain=True,
           offset_group_number=3)
```

lesson9_创建和获取关键帧信息

![](attachments/Maya%20第三周%20作业_image_5.png)

image.png

![](attachments/Maya%20第三周%20作业_image_6.png)

随机抖动.gif

思路：

1.利用animCurve类型来判断需要抖动的属性是否有关键帧，如果有则利用listAttr的time参数来获取时间段每一帧的属性数值

2.利用range函数的step参数来控制时间段的间隔，这样可以控制隔几帧K下关键帧

3.利用keyTangent函数改变K帧后的曲线模式

4.利用参数控制曲线模式改变的开启与关闭（比如想保留当前随机出来的结果，那么就可以开启edit_key_tangent参数来改变曲线的模式）

5.抖动则可以用sin 或者cos函数，随机浮点则可以用 random.uniform或者随机整数

```python
import random
import math
import maya.cmds as cmds
def random_shake(target_obj, time_range=None, keyframe_step=1, 
                 shake_offset_range=5, attr_name=None, attr_original_value=0,
                 key_tangent='auto', edit_key_tangent=False):
    """Random Shake For Object. Support Set Offset Keyframe Base On Original Value
    :param target_obj:Str
    :param time_range:list. time range
    :param keyframe_step:Int. Step for keyframe
    :param shake_offset_range: Amplitude for shake
    :param attr_name:Str. attr name
    :param attr_original_value:float . attr original value
    :param key_tangent:Str "auto", "spline", "clamped", "linear", "flat"
    :param edit_key_tangent:Bool
    :return: None
    """
    if attr_name is None:
        attr_name = 'ty'
    if time_range is None:
        time_range = [0, 100]
    if not edit_key_tangent:
        current_attr_value = attr_original_value
        attr_anim_curves = cmds.listConnections("{}.{}".format(target_obj, attr_name), t="animCurve")
        for i in range(time_range[0], time_range[-1] + 1, keyframe_step):
            shake_value = math.sin(i) * random.uniform(0, shake_offset_range)
            if attr_anim_curves:
                current_attr_value = cmds.getAttr("{}.{}".format(target_obj, attr_name), t=i)
            cmds.setKeyframe(target_obj, at=attr_name, time=i, v=shake_value + current_attr_value)
    new_anim_curves = cmds.listConnections("{}.{}".format(target_obj, attr_name), t="animCurve")
    if not new_anim_curves:
        return False
    cmds.keyTangent(new_anim_curves[0], itt=key_tangent, ott=key_tangent)
random_shake('pSphere1',
             time_range=[1, 200],
             keyframe_step=5,
             shake_offset_range=3,
             attr_name='ty',
             key_tangent="auto",
             attr_original_value=10,
             edit_key_tangent=False)
```