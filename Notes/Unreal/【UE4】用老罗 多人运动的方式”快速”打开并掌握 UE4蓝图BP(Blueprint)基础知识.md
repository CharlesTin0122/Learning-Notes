## 【前言】

本篇只涉及基础的蓝图知识，没有大佬们搞的那么高深（而且我也并不怎么喜欢写文字堆叠的那种代码，图形化代码更适合我）

之前也乱七八糟的学过各种语言，感觉编程语言就跟人类语言一样，人类语言的不同是受不同地域的限制而不同，而编程语言是根据平台的不同，如Web端的，PC端的，手机端的，服务端的，各有各的优势，但是呢，总得有一门母语，就跟汉语一样，再去学习其他语种都有个参照。

编程语言也一样，恰巧我的编程语言母语是Unreal BP蓝图（图形化的东西使编程更简化，像把一堆代码集成写成一个节点，以后再调用的时候直接键入调入这个节点就可以，而不至于找不到当时写的源代码，又得重新写一遍，既省时又省力）

## 【导图】

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_2.png)

## **Event Dispatcher 是重头戏！**

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_3.png)

## 一、变量（Variable）

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_4.png)

## 【1.1】常见变量：

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_5.png)

## 【1.2】特殊变量

### 【1.2.1】枚举Enumeration（Enum）

【1.2.1.1】枚举定义

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_6.png)

【1.2.1.2】枚举选择

通过设置Default Value默认值，可切换不同的频道，判断各位美女们是否有空，以让老罗跟不同的美女单个邂逅运动。

1. 一种是 Equal（Enum）来Branch判断

1. 一种是直接根据设置的默认值来Switch On判断切换不同的美女频道

1. 还有一种是Select选择器（我们在下面的结构体部分可以看到）

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_7.png)

**另外，如果你用Enum的名字 配合模型的插槽名字 来直接定义位置的话，记得一定要用String转化！否则是个错误的名字！！！**

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_8.png)

### 【1.2.2】结构体 Structure

可以集合很多的变量类型，如人物的姓名、年龄、身高、体重等等，都可以集成在一块，作为一个结构体进行整合变量。当然也可以嵌套其他的枚举/结构体类型

【1.2.2.1】结构体定义+嵌套

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_9.png)

【1.2.2.2】结构体get变量设置

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_10.png)

**另外：枚举+结构体+选择器来让我们在细节栏内调换颜色也是一种非常吃香的方法呢。（由于不能Get到Structure结构体的名字，所以下方就是将结构体的值和枚举的名字绑定起来了，比较方便呢）**

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_11.png)

### 【1.2.3】Object类

灯光、角色、网格体，或者是自己定义的BP蓝图都属于这个变量类型

新建一个BP_Actor，添加变量，键入BP _Actor 测试可看到

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_12.png)

## 二、Macro 宏

### 【2.1】作用

它存放常用的逻辑操作，像循环语句双击打开可以看到大多用宏构成（新建MacroLibrary可以将ParentClass设置为Object（在创建之初就选Object），这样所有的蓝图都可以使用这些常用逻辑操作了）（另：Function Library的父类只能是Blueprint Function Library，不可更改）

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_13.png)

### 【2.2】注意

1. 如果你要播放动画，经常用到

1. Macro可以有很多的输入引脚和输出引脚，而函数Function的话只能由各有一个

1. 宏是逻辑运算，是编译不了的（可以看到Compile按钮呈灰显状态）

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_14.png)

## 三、Event/Function 事件/函数

1. 自定义事件Custom Event/Function

1. Event Begin Play

1. Construction Script

1. Event Tick

1. Event End Play

1. Event Destroyed(我经常看成De +story，注意一下)

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_15.png)

相关综合实际操作请参见Spline BP

[**X Tesla：【UE4】Spline BP 程序化模型/动画轨迹（爆肝般的详细）**](https://zhuanlan.zhihu.com/p/134279765)

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_16.png)

## 四、Event Dispatcher 事件调度器

## 本故事纯属虚构，如有雷同，纯属巧合。

## 本故事纯属虚构，如有雷同，纯属巧合。

## 本故事纯属虚构，如有雷同，纯属巧合。

### 【4.1】准备素材

【4.1.1】老罗BP

1. 新建Character BP

1. 添加Mesh和动画蓝图

1. 添加文字以区别开

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_17.png)

【4.1.2】女孩 父类 BP（在实例当中创建不同颜色的女孩及文字标签）

1. 跟4.1.1一样（或复制一份老罗的BP）

1. 创建材质，给Color Vector值以在蓝图中控制

1. 填写以下蓝图

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_18.png)

【4.1.3】

1. 创建女孩父类BP的实例，为RGB 或123

1. 在关卡中设置相关亮眼睛（可编辑的）变量及调节角色位置，如下图。

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_19.png)

### 【4.2】给老罗的BP添加Dispatcher（老罗要跟美女们建立联系呢）

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_20.png)

### 【4.3】设置多人运动事件

1. 我们先把老罗的蓝图实例化

1. 然后定义与大美女、二美女、三美女的整体多人运动事件

1. 这里是在美女身上燃烧欲望的火焰，以判断区别。

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_21.png)

### 【4.4】快捷键绑定呼叫

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_22.png)

### 【4.5】操作测验

1. B——老罗赢得了三位美女的青睐，绑定了联系，要了电话号。

1. C——老罗打电话，叫来了三位美女，多人运动开始，老罗开始发力。

1. U——三位美女看清楚了老罗是个渣男，把手机停机了，从此再也不跟老罗联系了。

1. C——老罗再次给三位美女打电话，没有一个人接

1. B——老罗尝试再跟三位美女联系，用它的高超技法重新赢得了美女们的青睐，再次建立了联系

1. C——老罗又开始发力了，多人运动开始

1. U——三位美女看清楚了老罗是个渣男，人渣都不如，发誓再也不联系了。

然后，就没有然后了。

【UE4】多人运动理解Dispatcher

## 【4.6】设置多人运动Bug事件

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_23.png)

## 【4.7】操作测验

1. N——老罗跟各位美女建立联系

1. C——老罗打电话，开始运动

1. T——老大发现老罗是个渣男，从此断绝往来（老二和老三还蒙在鼓里呢）

【UE4】多人运动理解Dispatcher

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_24.png)

## 五、Interface 接口

### 【5.1】设置Interface

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_25.png)

1. 我们新建一个Interface，命名位Interface Multiperson_Movement

1. 函数命名位MultiPersonMovement

1. 添加一个Inputs变量为Number

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_26.png)

### 【5.2】给女孩 父类添加 Interface

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_27.png)

### 【5.3】在女孩父类当中添加接口事件

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_28.png)

### 【5.4】进入关卡蓝图

用Does Implement Interface来判断女孩是否使用MultiPerson Interface，如果使用了，则呼叫通信输出字符串。（按下O测试）

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_29.png)

### 【5.5】测试

【UE4】Interface测试视频

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_30.png)

## 六、循环语句

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_31.png)

### 【6.1】For Loop

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_32.png)

### 【6.2】For Loop With Break

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_33.png)

### [6.3]For Each Loop

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_34.png)

### [6.4]For Each Loop With Break(跟For Loop With Break差不多呢）

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_35.png)

### 【6.5】While Loop（类似For Loop With Break）

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_36.png)

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_37.png)

## 七、执行语句

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_38.png)

### 【7.1】Do Once

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_39.png)

### 【7.2】Sequence

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_40.png)

### 【7.3】Multigate

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_41.png)

### 【7.4】FlipFlop

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_42.png)

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_43.png)

## 八、判断语句

![](attachments/【UE4】用老罗%20多人运动的方式”快速”打开并掌握%20UE4蓝图BP(Blueprint)基础知识_image_44.png)

## ---------------------------------------------------------------------------

## UE4 的蓝图基础知识就介绍到这里了，如有其他待添加，如有错误请指正~

## 创作不易，看完后不妨点个赞多收藏，对我也是一份鼓励，促使我继续创作下去呢。（即使赚不到一分钱）