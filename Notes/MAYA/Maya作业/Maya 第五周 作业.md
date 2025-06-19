# Maya: 第五周 作业

![](attachments/Maya%20第五周%20作业_image_0.png)

[單壹崽崽](https://www.jianshu.com/u/92cf571d45d7)

关注

2020.01.01 23:08:40字数 39阅读 398

lesson13_Maya 中的事件触发

![](attachments/Maya%20第五周%20作业_image_1.png)

image.png

![](attachments/Maya%20第五周%20作业_image_2.png)

属性影响练习.gif

```python
import maya.cmds as cmds
def transfer_attr_val(source_obj, target_obj, attr_name):
    
    source_obj_attr_val = cmds.getAttr('{}.{}'.format(source_obj, attr_name))
    
    cmds.setAttr('{}.{}'.format(target_obj, attr_name), source_obj_attr_val)
  
# create ball and box mesh
ball_mesh = cmds.polySphere(n='ball', ch=False)[0]
cmds.setAttr('{}.tx'.format(ball_mesh), -3)
box_mesh = cmds.polyCube(n='box', ch=False)[0]
cmds.setAttr('{}.tx'.format(box_mesh), 3)
cmds.makeIdentity(ball_mesh, box_mesh, a=True, t=True)
attrs_list = ['{}{}'.format(attr, axial) for attr in 'trs' for axial in 'xyz']
jobs_id_list = []
for attr in attrs_list:
    
    job_id = cmds.scriptJob(attributeChange=('{}.{}'.format(ball_mesh, attr), 
                                             'transfer_attr_val("{}","{}","{}")'.format(ball_mesh,box_mesh,attr)))
    jobs_id_list.append(job_id)
# delete job id
cmds.scriptJob(kill= jobs_id_list)
```

扩展效果：

![](attachments/Maya%20第五周%20作业_image_3.png)

双向约束？.gif

不存在的！目前不支持K帧！就是走个逻辑玩玩,想玩的拿去玩~

```python
import pymel.core as pm
# setup
source_objs = pm.selected()
mutual_constrain_grp_list = []
for obj in source_objs:
    obj_parent = obj.getParent()
    if not obj_parent or not obj_parent.name().endswith('_mutual_constrain_Grp'):
        mutual_constrain_grp = pm.group(em=True, n='{}_mutual_constrain_Grp'.format(obj.name()))
        pm.delete(pm.parentConstraint(obj, mutual_constrain_grp))
        pm.parent(obj, mutual_constrain_grp)
        if obj_parent:
            pm.parent(mutual_constrain_grp, obj_parent)
    mutual_constrain_grp_list.append(mutual_constrain_grp)
        
def p_constrain(source_objs):
    
    source_objs = [pm.PyNode(obj) for obj in source_objs]
    current_sel_obj = pm.selected()
    
    if not current_sel_obj or current_sel_obj[0] not in source_objs or len(current_sel_obj)>1:
        return False
    
    for item in source_objs:
        if not item.getParent().name().endswith('_mutual_constrain_Grp'):
            return False
    
    pm.delete([item.getParent().inputs(t='parentConstraint') for item in source_objs])
    copy_list = source_objs[::]
    copy_list.remove(current_sel_obj[0])
    for item in copy_list:
        pm.parentConstraint(current_sel_obj[0], item.getParent(), mo=True,weight=1)
job_id = pm.scriptJob(event= ("SelectionChanged", 'p_constrain({})'.format([obj.name() for obj in source_objs])))
# delete job
pm.scriptJob(kill= job_id)
```