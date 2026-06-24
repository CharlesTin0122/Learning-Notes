- 使用矩阵来绑定手臂 腿和脊椎
# 绑定手臂
- 创建手臂的IKFK骨骼，放入arm_l_ctrl_grp组，该组位置位于上臂根部，该组的变换转移至Offset Parent Matrix
- ![](attachments/05.2-Limb%20Rigging%20-%2002.png)
- 是用手臂根控制器arm_root_l_ctrl的World Matrix链接arm_l_ctrl_grp组的Offset Parent Matrix
- ![](attachments/05.2-Limb%20Rigging%20-%2002-1.png)
- 这样 arm_root_l_ctrl 就控制了 arm_l_ctrl_grp 组，使得手臂IKFK骨骼跟随上臂根控制器运动
- ![](attachments/05.2-Limb%20Rigging%20-%2002-2.png)![](attachments/05.2-Limb%20Rigging%20-%2002-3.png)
# 约束主骨骼
- 使用IKFK骨骼父子约束主骨骼，这里使用父子约束而不是使用偏移父矩阵，是因为偏移父矩阵约束在烘焙动画的是偶不会将矩阵值（matrix）赋予变换值（transform），会导致在游戏引擎中失去动画。
- ![](attachments/05.2-Limb%20Rigging%20-%2002-4.png)
- 还是经典操作
- ![](attachments/05.2-Limb%20Rigging%20-%2002-5.png)
# 绑定腿
- ![](attachments/05.2-Limb%20Rigging%20-%2002-6.png)
- - 最后将IKFK骨骼组放入RigSystem组
- ![](attachments/05.2-Limb%20Rigging%20-%2002-10.png)
# 绑定脊椎
- 整理脊椎控制器
- ![](attachments/08.2-IK%20FK%20Spine.png)
- Pelvis控制器矩阵约束IKFK骨骼组
- ![](attachments/05.2-Limb%20Rigging%20-%2002-8.png)
- IKFK骨骼约束主骨骼，Pelvis控制器IKFK_Switch属性控制约束节点
- ![](attachments/05.2-Limb%20Rigging%20-%2002-9.png)
- 实现脊椎IKKF控制器的显示
- ![](attachments/14-基于矩阵的Limb%20Rigging-1.png)
