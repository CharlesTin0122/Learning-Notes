# Gameplay 进阶
> 本系列使用的虚幻引擎版本为5.3.2
>
>  Windows11 i7-12700 RTX3060 laptop 
> 
> 40G LPDDR5内存 1.5T SSD+2T 机械硬盘
## UE5 进阶方向
![Alt text](image-11.png)
## C++ or Blueprints
### Gameplay Toolchain

#### 表层工具链
- UBT UHT 反射 GC 元数据......
- UFUNCTION() UPROPERTY()......
- TArray TMap......
- GameplayStatics CharacterMovementComponent......
#### 深层架构
MVVM
- Rendering
    - Model，material，shader，texture
    - Light，shadow
    - Render pipeline
  - Sky，terrain，etc
- Animation
  - Basic concepts
  - Animation structure and pipeline
- Physics
  - Basic concepts of Physical System
  - Gameplay applications
  - Performance optimization
- Gameplay
  - Event System
  - Scripts System
  - Graph Driven
- Misc.
  - Effects(Niagara)
  - Navigation
  - Camera
  - ...
#### 引擎架构
引擎架构分层 / Game engine layers

1.工具层 / Tool Layer：

FBX、USD\
各种编辑器

2.功能层 / Function Layer：

How to Make the world alive\
Heavy-duty Hotchpotch 

游戏绘制三渲二 visible，

动画，物理表达计算 movable，

脚本AI状态机定义行为 playable

人机交互（例：血条）

3.资源层 / Resource Layer：

Manager Asset Life Cycle\
eg: GC 延迟加载

声音、模型等，加载管理各种资源

4.核心层 / Core Layer：

**SIMD**\
类似工具箱，进行游戏逻辑管理

5.平台层 / Platform Layer：

操作系统、输入设备、运行平台、软件平台

- 第三方工具 SDK
- .asset
- GUID reference
  

看完这些，大家应该可以明白了我们去开发游戏，很多时候都是在Gameplay层进行开发，我们把已有的美术资源组合起来，然后一一为其编写行为逻辑，并构建整套游戏逻辑，所以，无论用C++还是蓝图，我们本身都是已经在一套已经建好轮子的引擎上进行开发，本质都是调用函数与事件处理，所以游戏开发中使用C++还是蓝图其实差别并不大，C++不需要通过蓝图虚拟机来编译，运行速度更快，而且学习用C++编写一些插件可以更好的帮我们掌握C++的高级特性，我们甚至能自己去造一些gameplay框架上的轮子，而用蓝图显然是更加利于逻辑编写的，能够更方便地实施调试，且对刚入门游戏行业的程序员与设计师更加友好，所以，一般大家完全可以从蓝图开始学习制作游戏，等到能把很多函数和蓝图库研究明白了，不满足于写行为逻辑了，那就可以去看C++源码的一些实现方式了，比如如何导航，如何创建计时器，这些其实都早已经封装成了C++和蓝图函数，我们可以在代码里看到它具体的实现，这对深入研究游戏引擎和开发是非常有帮助的。
### 服务器开发

当然，现在的游戏基本都需要网络模块，就算是基本的单机游戏，那也需要一个成熟的Auth系统，如果大家想去了解UDP和PRC这些东西，大家可以先用自己比较熟练掌握的语言去搭建一个小框架，然后去学习一下sql语句，这个部分UE5封装好了OnlineSession与整套PRC等工具链，大家对网络有些了解之后就可以去看UE5这部分的实现了，然后去写自己的远程调用，服务器鉴权等等，甚至还能优化一些低延迟同步，消息队列，异步加载等等，这部分是建议把C++很多特性学习一下再进行开发。
### Shader
这里写的shader不是指Computer Graphics，并不是用DX12，Vulkan，OpenGL等等api去写渲染管线，光照方程等等。UE5用蓝图搭建了一套Shader系统，大家可以尝试着去做一些风格化渲染，线条描边，三渲二，这些主要是对材质和纹理进行操作，十分建议先从蓝图开始写起。等熟练掌握之后再去看C++源码那些图形Api
## Gameplay 系统架构
**以制作大型3A游戏的角度去思考**
[Gameplay架构-大钊](https://zhuanlan.zhihu.com/p/22833151)

### Actor
>如果让你来制作一款3D游戏引擎，你会怎么设计其结构？

>尽管游戏的类型有很多种，市面上也有众多的3D游戏引擎，但绝大部分游戏引擎都得解决一个基本问题：抽象模拟一个3D游戏世界。根据基本的图形学知识，我们知道，为了展示这个世界，我们需要一个个带着“变换”的“游戏对象”，接着让它们父子嵌套以表现更复杂的结构。本质上，其他的物理模拟，游戏逻辑等功能组件，最终目的也只是为了操作这些“游戏对象”。
这件事，在Unity那里就直接成了“GameObject”和“Component”；在Cocos2dx那里是一个个的“CCNode”，操纵部分直接内嵌在了CCNode里面；那么在UE4的眼中，它是怎么看待游戏的3D世界的？

Actor继承于Object，具有的一些功能：Replication,Spawn,Tick......


>思考：为何Actor不像GameObject一样自带Transform？

>C++的哲学“不为你不需要的东西付代价”

`USceneComponent* RootComponent`

![Alt text](image.png)

### Level & World

![Alt text](image-1.png)

![Alt text](image-2.png)

![Alt text](image-3.png)

### WorldContext，GameInstance，Engine

**WorldContext**

![Alt text](image-4.png)
```cpp
namespace EWorldType
{
	enum Type
	{
		None,		// An untyped world, in most cases this will be the vestigial worlds of streamed in sub-levels
		Game,		// The game world
		Editor,		// A world being edited in the editor
		PIE,		// A Play In Editor world
		Preview,	// A preview world for an editor tool
		Inactive	// An editor world that was loaded but not currently being edited in the level editor
	};
}
```
```cpp
struct FWorldContext
{
    [...]
	TEnumAsByte<EWorldType::Type>	WorldType;

	FSeamlessTravelHandler SeamlessTravelHandler;

	FName ContextHandle;

	/** URL to travel to for pending client connect */
	FString TravelURL;

	/** TravelType for pending client connects */
	uint8 TravelType;

	/** URL the last time we traveled */
	UPROPERTY()
	struct FURL LastURL;

	/** last server we connected to (for "reconnect" command) */
	UPROPERTY()
	struct FURL LastRemoteURL;

}
```
**GameInstance**
![Alt text](image-5.png)

**Engine**

![Alt text](image-6.png)
>此处UEngine分化出了两个子类：UGameEngine和UEditorEngine。众所周知，UE的编辑器也是UE用自己的引擎渲染出来的，采用的也是Slate那套UI框架。好处有很多，比如跨平台比较统一，UI框架可以复用一套控件库，Dogfood等等，此处不再细讲。所以本质上来说，UE的编辑器其实也是个游戏！我们是在编辑器这个游戏里面创造我们自己的另一个游戏。话虽如此，但比较编辑器和游戏还是有一定差别的，所以UE会在不同模式下根据编译环境而采用不同的具体Engine类，而在基类UEngine里通过一个WorldList保存了所有的World。

### Pawn

![Alt text](image-7.png)

![Alt text](image-8.png)

### Controller
![Alt text](image-10.png)
1. 作为一个最基本的`Controller`，首先最重要的就是能**与`Pawn`关联起来**，能够做到控制pawn去实现行为逻辑。尤其是在比如RTS或者多人协同游戏上，我们要能准确区分不同`Controller`去控制不同的`Pawn`，这些逻辑会随着需求的增多而变得越来越复杂。
2. **复制相同逻辑**，能够将同一段行为复制给不同的对象，允许多个实例存在。
3. **可挂载释放**，可以灵活地从PawnA转移到PawnB。
4. **能够脱离Pawn存在**
5. **操纵Pawn生死的能力**
6. **根据配置自动生成**
7. **事件响应**
8. **自身有状态**
9. **拥有一定的扩展继承组合能力**。
10. **保存数据状态**
    >听说金鱼的记忆只有7秒，可是我却想记住你一辈子。所以我希望我能拥有一些记忆，人的过去成就了现在，也将指引着未来。以前有一个人跟我说过，**当你不能再拥有的时候，唯一能做的就是令自己不要忘记。**
11. **可在世界里移动**
12. **可探查世界的对象**
13. **可同步**

### APlayerState
**![Alt text](image-12.png)**
### PlayerController & AIController
Component-Actor-Pawn-Controller
![Alt text](image-9.png)
>- Camera的管理，目的都是为了控制玩家的视角，所以有了PlayerCameraManager这一个关联很紧密的摄像机管理类，用来方便的切换摄像机。PlayerController的ControlRotation、ViewTarget等也都是为了更新Camera的位置。因为跟Camera的关系紧密，而Camera最后输出的是屏幕坐标里的图像，所以为了方便一些拾取的HitResult函数也都是实现在这里面。渲染章节会再详细介绍UE的摄像机管理。
>- Input系统，包括构建InputStack用来路由输入事件，也包括了自己对输入事件的处理。所以包含了UPlayerInput来委托处理。
UPlayer关联，既然顾名思义是PlayerController，那自然要和Player对应起来，这也是PlayerController最核心的部分。一个UPlayer可以是本地的LocalPlayer，也可以是一个网络控制UNetConnection。PlayerController只有在SetPlayer之后，才可以开始正常工作。
>- HUD显示，用于在当前控制器的摄像机面前一直显示一些UI，这是从UE3迁移过来的组件，现在用UMG的比较多，等介绍UI模块的时候再详细介绍。
>- Level的切换，PlayerController作为网络里通道，在一起进行Level Travelling的时候，也都是先通过PlayerController来进行RPC调用，然后由PlayerController来转发到自己World中来实际进行。
>- Voice，也是为了方便网络中语音聊天的一些控制函数。

![Alt text](image-13.png)
>Navigation，用于智能根据导航寻路，其中我们常用的MoveTo接口就是做这件事情的。而在移动的过程中，因为少了玩家控制的来转向，所以多了一个SetFocus来控制当前的Pawn视角朝向哪个位置。
AI组件，运行启动行为树，使用黑板数据，探索周围环境，以后如果有别的AI算法方法实现成组件，也应该在本组件内组合启动。
Task系统，让AI去完成一些任务，也是实现GameplayAbilities系统的一个接口。目前简单来说GameplayAbilities是为Actor添加额外能力属性集合的一个模块，比如HP，MP等。其中的GamePlayEffect也是用来实现Buffer的工具。另外GamePlayTags也是用来给Actor添加标签标记来表明状态的一种机制。目前来说该两个模块似乎都是由Epic的Game Team在维护，所以完成度不是非常的高，用的时候也往往需要根据自己情况去重构调整。
### GameMode
![Alt text](image-14.png)

![Alt text](image-15.png)
## Blueprints Misc.
-  Actor Blueprint
-  Anim Blueprint
-  Component
-  UMG
-  Notify
-  AITask
-  Niagara
-  ......
## CombatComponent 实战
- InputAction
- Anim Montage
- Notify
- Interface
- Component