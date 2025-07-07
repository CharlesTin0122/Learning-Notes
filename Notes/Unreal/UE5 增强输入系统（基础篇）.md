- **概述**

- Enhanced Input System实际上就是对默认的输入系统做了一个扩展，它以模块化的方式解耦了从输入按键配置到事件处理的逻辑过程，提供了更灵活更便利的输入配置和处理过程。同时又能向前兼容UE4的输入系统。

- **重要的类**

- **Input Actions **

- 输入操作：是交互角色可能做出的任何动作，独立于原始输入，可以配置多种类型的输入值。

- **Input Mapping Contexts**

- 输入映射上下文，将用户输入映射到输入动作，并可以动态地为每个用户添加、移除或安排优先次序。你可以通过"增强输入本地玩家子系统"（Enhanced Input Local Player Subsystem），将一个或多个上下文添加给本地玩家，并调整它们的优先级，避免多个操作因读取同一个输入事件而冲突。

- **Modifiers**

- 修饰器，用于修改来自用户设备的原始输入值。在输入映射上下文中，每个输入动作的原始输入都可以关联任意数量的修饰器。常见修饰器包括取反（negate），死区、多帧输入平滑处理、将输入向量从本地空间转换到世界空间，以及插件中的一些其他修饰器。开发人员还可以创建自己的修饰器。

- **Trigers**

- 触发器，使用经过修饰器修改的输入值，或者使用其他输入动作的输出值，来确定是否激活输入动作。输入映射上下文中的输入动作，其每个输入都可以有一个或多个触发器。例如，拍摄照片时，可能需要用户按住鼠标左键约0.25秒，同时，还有一个用于控制摄像机拍照方向的输入动作处于激活状态。

- **具体操作**

- **创建Input Action**

- 创建前后行走，左右行走，转向，俯仰，跳跃5个行为，其中跳跃的数据类型为布尔类型，其余均为float类型

- 

![](attachments/增强输入系统（Enhanced%20Input%20System）_image_0.png)

- 

![](attachments/增强输入系统（Enhanced%20Input%20System）_image_1.png)

- 

![](attachments/增强输入系统（Enhanced%20Input%20System）_image_2.png)

- 创建

- **创建两个映射，move和action，move用来映射移动相关的行为，action用来映射跳跃行为**

- 

![](attachments/增强输入系统（Enhanced%20Input%20System）_image_3.png)

- **action映射设置**

- 

![](attachments/增强输入系统（Enhanced%20Input%20System）_image_4.png)

- **move映射设置**

- 

![](attachments/增强输入系统（Enhanced%20Input%20System）_image_5.png)

- **其中S，A，nouseY键所对应的向后移动，向左移动和俯仰观察的返回值应当取反（-1）。所以使用modifier（修饰器）来修改取反（Negate）.**

- 

![](attachments/增强输入系统（Enhanced%20Input%20System）_image_6.png)

- **事件蓝图**

- **重要节点**

- **Get Player Controller，获取玩家控制器**

- **Get Enhanced Input Local Player Subsystem From Controller，获取增强输入本地玩家子系统**

- **Add Mapping context，添加映射上下文**

- **Enhanced Input Action，获得增强输入行为事件**

- **获得Controller--获得增强输入本地玩家子系统--添加两个映射文件（move，action）**

![](attachments/增强输入系统（Enhanced%20Input%20System）_image_7.png)

- **调用前后移动行为，链接添加移动输入，他的方向是获取控制器的向前向量（只需要Yaw方向）。**

- 

![](attachments/增强输入系统（Enhanced%20Input%20System）_image_8.png)

- 

![](attachments/增强输入系统（Enhanced%20Input%20System）_image_9.png)

- 

![](attachments/增强输入系统（Enhanced%20Input%20System）_image_10.png)

- **调用左右移动行为，链接添加移动输入，他的方向是获取控制器的向右向量（需要roll和Yaw方向）。**

![](attachments/增强输入系统（Enhanced%20Input%20System）_image_11.png)

- **设置左右转身和俯仰查看，通过调用对应的action，赋值给添加控制器输出**

![](attachments/增强输入系统（Enhanced%20Input%20System）_image_12.png)

- **设置跳跃，调用jump的action，赋值给jump和stop jumping**

![](attachments/增强输入系统（Enhanced%20Input%20System）_image_13.png)

- 