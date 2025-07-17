# **前言**

在平时我们进行游戏开发的时候，经常会围绕着角色与动画这两元素进行整体的开发工作，因此角色与动画的性能优化将重中之重，因为他们决定着游戏的游玩体验。今天将与大家分享一些角色与动画方面的性能优化经验，帮助大家在开发过程中提高游戏性能，并且尽可能照顾有着不同知识储备的开发者。

本文出自[[https://www.youtube.com/watch?v=N_suMyUuork]]，讲者是Matthew Lake。

![图片](attachments/54a1c63d6d72122b50df9f0b5b0e68e2_MD5.webp)

  

**目录**

一、常用的知识

    1.1. 常用命令

    1.2. Size Map

    1.3. MemReport

    1.4. Control Rig

    1.5. GPU Visualizer

    1.6. Insights

二、动画序列

    2.1. 资产检查

    2.2. 编辑器工具

    2.3. 导入设置

    2.4. 轨道与曲线处理结果

    2.5. 动画压缩

三、LOD

    3.1. 屏幕大小

    3.2. LOD滞后阈值

    3.3. 骨骼列表

    3.4. 减面设置

四、动画蓝图

    4.1. 多线程

    4.2. Fast Path

    4.3. 动画蓝图函数

    4.4. 动画蓝图LOD

    4.5. 优化小技巧杂项

五、骨骼网格体姿势更新

    5.1. 是否更新

    5.2. 更新频率

    5.3. 受预算控制的骨骼网格体组件

六、纹理

    6.1. 限制纹理分辨率大小

    6.2. Micro Detail

    6.3. 纹理压缩

    6.4. Oodle编码

    6.5. 通道合成

    6.6. 蒙版

七、骨骼网格体组件

    7.1. 包围盒

    7.2. 渲染静态

    7.3. Nanite小妙招

八、蓝图

    8.1. Tick

    8.2. 解决硬引用

    8.3. 软引用

    8.4. 子蓝图

结语

## **一、常用的知识** 

### **1.1. 常用命令**  

Stat FPS显示帧率与帧用时。

Stat UNIT显示各种帧用时，游戏线程与GPU耗时等。

Stat UNITGRAPH将以图表显示Stat UNIT中显示的数据。

![图片](attachments/3f7f4d115b3d177e3a97d853a3a1fbb7_MD5.webp)

Stat ANIM显示动画相关的耗时统计数据

![图片](attachments/bd2ee82b2f879ce07338716257b72c13_MD5.webp)

ShowDebug ANIMATION显示动画相关的Debug内容，角色包围盒，当前动画节点的权重等。

![图片](attachments/d766e5d1867085068457b58b3a4a0361_MD5.webp)

### 

### **1.2. Size Map** 

Size Map（尺寸图）用来看资产的引用、加载该资产所需要的磁盘大小与内存大小。

![图片](attachments/f9eab794b95ab72bb86ca8ee9be25f0c_MD5.webp)

### **1.3. MemReport** 

游戏运行中打这个命令可以输出一份当前内存加载了的资产。

![图片](attachments/660dcf7145cf3a565039e76cc9b790d0_MD5.webp)

### 

### **1.4. Control Rig** 

如果您正在用Control Rig，可以在Control Rig的类默认中找到Show Node Instruction Index、Show Node Run Counts、Enable Profiling选项，打开之后就会发现我们的Control Rig视图像圣诞树一样亮起了灯。红箭头的数值就是当前Control Rig所需要的耗时。

![图片](attachments/8dc89ffcc91a818b55ec4331fc1d0f18_MD5.webp)

在节点上也能看到耗时和节点的序号。

![图片](attachments/c0a1f12bc88500f39fcc12de92bb482c_MD5.webp)

### 

### **1.5. GPU Visualizer** 

在PIE中按“Ctrl + Shift + 逗号”组合键可以呼出一个GPU Visualizer工具，它可以列出GPU帧耗时的详细信息。

![图片](attachments/dd646b66384c062fbf85fa06201d079a_MD5.webp)

### 

### **1.6. Insights** 

强烈推荐用Insights，这是个很棒的内置性能追踪工具。

![图片](attachments/4514fc661a197efd4edebd3cb733c82d_MD5.webp)

如果我们要记录一些动画相关的性能追踪，需要在通道里勾选Animation、AssetLoadTime和Stat Named Events选项。

![图片](attachments/bf9f72796877504353a3e7bda1432e68_MD5.webp)

在PIE运行中可以随时打开追踪，玩一段时间然后结束追踪，就能记录下一段时间内的性能表现，在Insights中打开对应的记录文件就能看到详细信息。

![图片](attachments/1752cb71e5ade8bf4d1ce256da4e2106_MD5.webp)

## **二、动画序列** 

### **2.1. 资产检查** 

项目内的动画序列一般会有成百上千个，所以注意一些小细节就能搞定大优化。在动画序列的导入中，尽可能只导入必要的东西。在Animation Track的导入中，假如我们不需要脸部动画数据就不必要将其导入。

然后就是Animation Curves，我们会在DCC中加上一些编辑器内用不到的动画曲线，所以确保导入后删除掉这些不必要的动画曲线。

![图片](attachments/413aa7aadb01d4443ddb88e5adcd2153_MD5.webp)

在检查动画序列资产中经常会用到这个Track Data数组，我们可以在这里看到动画序列采样了哪些骨骼。

![图片](attachments/fb7d18398deb6185e7c06587f1067823_MD5.webp)

### 

### **2.2. 编辑器工具** 

我们可以编写资产操作工具去帮助我们快速编辑或者显示资产的信息。

![图片](attachments/02e09e6e078683c4a46941d0bdd8e793_MD5.webp)

以下是示例函数的基本逻辑，帮助我们输出当前动画序列的轨道条数或者命名。我们可以利用这个快速检查动画序列的轨道数，以便于我们调整和优化这些资产。

         ![图片](attachments/235d1608da7d9fb643aa75773dad99d9_MD5.webp)

### **2.3. 导入设置** 

可以在导入的时候就避免从源文件导入曲线。

![图片](attachments/19c0ee09235a335676d7cd43285e025c_MD5.webp)

一个个调整会很痛苦，所以我们可以让引擎记住我们的导入设置。在这里修改配置文件。

 ![图片](attachments/a768f3a01d7e579642842d52cee44b46_MD5.webp)

### **2.4. 轨道与曲线处理结果** 

当我们完成以上的清理轨道与曲线工作时，就能看到这个动画序列磁盘与内存占用都得到了很大的优化。上文也提到过动画序列在项目中可能有成百上千个，以此积跬步至千里，整个项目的动画序列将会有很可观的磁盘与内存占用的优化。

![图片](attachments/42cb6fcd781cea60a6b29f137391ca18_MD5.webp)

不仅如此，在Anim Graph中也会有相当不错的优化，因为节点之间的信息是一级一级传递下去的。减少了轨道与曲线数量，传递下去的数据就会变少，处理就会变得更快。

![图片](attachments/0bfd499267dc9540387f84e1d22d5e7d_MD5.webp)

### 

### **2.5. 动画压缩** 

在虚幻5.3及以上版本中，动画压缩库（Animation Compression Library）是默认开启的，如果低于这个版本，就需要在虚幻商城中下载使用。

传送门：**https://www.unrealengine.com/marketplace/en-US/product/animation-compression-library**

## **三、LOD** 

大家对于LOD应该不陌生，这里便简单说说。Level of Detail是一种处理网格体远近细节程度的技术，如果网格体离得远，就会显示更低细节的模型。而对于骨骼网格体而言，LOD的不同，骨骼数量，变形目标也会有所不同。

![图片](attachments/320e59441b24dde6d676b4554ed43438_MD5.webp)

在虚幻内可以直接生成静态网格体和骨骼网格体的LOD，由于本文着重介绍角色，所以我们重点放在骨骼网格体上，感兴趣的小伙伴可以自己了解一下静态网格体的LOD生成。

骨骼网格体的LOD生成可以在编辑器内调整，LOD数量代表我们将自动生成几个LOD。

![图片](attachments/8bbc93bd902a4b34e724c972ed33ca93_MD5.webp)

LOD设置可以调整更多关于LOD生成的细节参数。使用数据资产储存这些的好处就是，我们可以给很多个骨骼网格体上同一种参数，这样我们就不用反复设置了。

![图片](attachments/3a452a8c50b6cc9ebad5d2fad8e207ba_MD5.webp)

我们来到数据资产看看这些参数。

![图片](attachments/2dd4fa65e2aa7d211011dd0fda5832c5_MD5.webp)

### 

### **3.1. 屏幕大小** 

屏幕大小顾名思义就是在屏幕上小于这个值就会使用这个LOD，以此类推其他LOD。

![图片](attachments/b2b35d8218f2353c6f7575b646ac20ae_MD5.webp)

使用A.VisualizeLODs 1指令可以绘制出具体的网格体信息。

![图片](attachments/e23e7ec0e83c97d2ea729e9409433a07_MD5.webp)

### 

### **3.2. LOD滞后阈值** 

由于骨骼网格体有动画，角色在动的时候，即使相机是静止的，角色的屏幕大小也会不断变化。这时候就需要一个滞后阈值来防止这种LOD来回切换的现象。

![图片](attachments/4bcaba95f245c888951c7301e929a950_MD5.webp)

![图片](attachments/ade053093029a4febb29f1556709b20f_MD5.webp)

有了这个阈值之后，我们处理LOD的曲线就会变成这样。这样LOD来回切的问题就解决了。

![图片](attachments/a5acf28a692524315a6fde1c438547bf_MD5.webp)

### 

### **3.3. 骨骼列表** 

骨骼列表可以帮助我们剔除LOD中不需要的骨骼。有两种模式，去除列表中的骨骼和保留列表中的骨骼。

![图片](attachments/e1a28143ad5a6cfaaf1245aee6d77d1c_MD5.webp)

举个例子，我想在LOD1去除脸部骨骼，在LOD2只保留身体骨骼等等。

![图片](attachments/1b11d3c3812ed7b8d4fb413a78329079_MD5.webp)

### 

### **3.4. 减面设置** 

减面设置实际上是一个大类，里面有很多参数，这里只会介绍几个重要的参数。

是否重映射变形目标：由于变形目标很耗性能，所以只会在必要的时候启用这个选项。

最大骨骼影响：一个顶点可能被多个骨骼影响，降低这个值可以减少骨骼数。

除了以上两个以外，还有很多设置，大家可以随意调整参数自行查看结果，找找感觉。

![图片](attachments/4db566479bbc87120916f8be30ccbe2b_MD5.webp)

在虚幻5.5中，Nanite即将支持骨骼网格体，但LOD技术仍然重要，在一些不支持Nanite的平台或者需要极度优化的项目中还会用到。

## **四、动画蓝图** 

### **4.1. 多线程** 

为项目中的动画蓝图启用多线程支持。

![图片](attachments/aad3b91a1c21e1f683b5b99cf7e4cf7b_MD5.webp)

为动画蓝图启用多线程支持。    

![图片](attachments/fb248e88d715d71846ac972cb0f31503_MD5.webp)

需要注意，如果动画蓝图用了根动画，这个动画蓝图将不会启用多线程运行。

![图片](attachments/e4c65662c74e3f3e26e4ef9a97f76ced_MD5.webp)

启用了多线程的动画蓝图将支持线程安全更新动画节点，可以把我们的更新逻辑放在这里。

![图片](attachments/ffb40ae95665d634d17634518616cf48_MD5.webp)

### 

### **4.2. Fast Path** 

当我们看到这些闪电标志时意味着这些节点用了Fast Path。如果没有，就会用回动画蓝图VM，这个过程相较于Fast Path会慢一些。

![图片](attachments/8150e6a8372d833d3d189f2afe4f52f4_MD5.webp)

在这里启用相关设置。

![图片](attachments/e4568af8222c5d0e55401be796c60fc3_MD5.webp)

如果我们想避免回退使用VM，可以打开这个Warning设置，提醒我们哪里回退了。

![图片](attachments/cb8b9eb87ed6158205e0f92d9e5a8164_MD5.webp)

![图片](attachments/4fad3526c7b82aa586bc42287708dcb7_MD5.webp)

可以直接读本蓝图的变量，但不要读引用的变量，这样会导致回退。

![图片](attachments/35ae290c6cf793a65d2222ff374c21fa_MD5.webp)

![图片](attachments/d7a89906134b5f807c4ad31877640fdb_MD5.webp)

用Property Access节点可以进入Fast Path。

![图片](attachments/bc0939ad097593f6a01b4b1b583c929b_MD5.webp)

And和Or节点，计算后结果也会导致回退，尽量将参数直接接入。

![图片](attachments/21417afc6b7b7b29aba6ae7871a01483_MD5.webp)

那如果我真的需要计算呢？看下面的动画蓝图函数。

### 

### **4.3. 动画蓝图函数** 

在节点中使用这些函数，可以拿变量进行计算。这些函数只会在节点运行的时候执行。

![图片](attachments/fccc83a79516a3c9fae63a89ef8ee813_MD5.webp)

或者使用Call Function节点，这个节点可以直接放在动画流程图中，并且有更多的事件触发时机选择。    

![图片](attachments/93a194ac67daa61247a318f3f7c63ff0_MD5.webp)

需要注意的是，这些函数需要线程安全才能运行，在蓝图中可以打开这个选项。

           ![图片](attachments/425d1368c15a5583543f674284b0ad88_MD5.webp)

使用例如下，这样就能保证节点进入Fast Path了。

![图片](attachments/70e564f2385e4d070aaa9b5aff6f0b3d_MD5.webp)

### **4.4. 动画蓝图LOD** 

选择节点，调整节点的LOD阈值，就能保证节点只会在对应的LOD及更高细节的LOD上播放。使用这个节点可以进一步优化远距离角色的动画蓝图处理表现。

         ![图片](attachments/1f72a166d4b69f9470ca86fc01166ed9_MD5.webp)

我们还可以获取当前骨骼网格体LOD来驱动动画蓝图的逻辑。比如动画蓝图会在LOD等于1时播放某个动画等。

![图片](attachments/7d845e34a84d479bb7d2a4fafd924906_MD5.webp)

虚幻5.3中更新了后期处理动画蓝图的LOD阈值，与上述的LOD阈值类似，在某个LOD层级以后不再启用后期处理动画蓝图。

![图片](attachments/c7b93da0785cc7ecf86b19b0c9a565a1_MD5.webp)

### 

### **4.5. 优化小技巧杂项** 

不要重复使用空间转换节点，将他们绑在一起使用，避免反复转换空间。

![图片](attachments/9c2eb0c26f73f17d4ab3aba7f5231b3f_MD5.webp)

状态机可以自定义一些状态转换参数，优化状态机的消耗成本。

![图片](attachments/25de25ee2834b127c2ce861a86b28827_MD5.webp)

缓存了姿势就能在多个地方中继续使用这个姿势，状态机也可以缓存。

![图片](attachments/ff157bb6708f798a5e192209f97b6720_MD5.webp)

## **五、骨骼网格体姿势更新** 

### **5.1. 是否更新** 

即使我们看不见骨骼网格体，它仍然会更新姿势，所以我们需要设置下图这个参数，调整骨骼网格体的姿势更新行为。

![图片](attachments/785b7bb796587ef189bccc45fa6beadc_MD5.webp)

我们可以调整项目配置文件来调整骨骼网格体组件中的这个默写值，但这个不适用于骨骼网格体Actor。我们可以自己手动设置这个值来应对一些需要特殊处理的情况。

![图片](attachments/bddefc1d594390aa00fc0eb852cd54c6_MD5.webp)

或者在源码中设置这个值。

![图片](attachments/013f88ed3db618baffacd4b27e49e3c8_MD5.webp)

除此之外还有一个参数叫No Skeletal Update，顾名思义用来控制是否更新骨骼网格体。

![图片](attachments/3b55529176059a0ddf8343790013ac63_MD5.webp)

### 

### **5.2. 更新频率** 

我们可以在骨骼网格体组件中打开更新频率相关的参数功能。

![图片](attachments/0f566a8409465982c2feacda1a81e6bd_MD5.webp)

虚幻引擎会自动控制跳过的帧，但如果想要手动控制跳过的帧，可以在商城使用这个插件。

传送门：**https://www.unrealengine.com/marketplace/en-US/product/update-rate-optimisation-blueprint-nodes**

![图片](attachments/e7f9e17379c4bafa1dce5f74a7c1612c_MD5.webp)

这个插件有两个模式，一个是LOD模式，一个是屏幕大小模式，可以通过对应的参数设置跳过的帧数。当我们启用了插值，就算跳过了一些更新帧，看起来与原来的没多大区别。

![图片](attachments/3762e2129bbbd9af00be484fe17053d0_MD5.webp)

### 

### **5.3. 受预算控制的骨骼网格体组件** 

虚幻自带一个Animation Budget Allocator插件，可以将骨骼网格体组件替换成这个插件提供的SkeletalMeshComponentBudgeted类，然后在Begin Play中执行这些。

![图片](attachments/7dbbec0dd564f07dceb256137121c0bf_MD5.webp)

在场景中执行这个指令a.Budget.Debug.Enabled 1可以打开Debug绘制。

![图片](attachments/e2e3d8bcd8b493252927fd63840dbbe4_MD5.webp)

用这个节点就能调整我们希望达到的预算，然后插件就会自动帮我们管理骨骼网格体的优化，比如调整跳过的帧等参数。这个结构体里还有更多参数，感兴趣的小伙伴可以自行探索。

![图片](attachments/827da2b47d67fbaaff2fc2b8c63e836a_MD5.webp)

## **六、纹理** 

我们常见的纹理分辨率基本都是2的幂，这是肯定的，因为要自动生成MipMap。但我们有注意过这些不同大小的纹理之间有什么倍数关系吗？看看这张图，假如我们能优化纹理分辨率大小，将能极大优化我们的磁盘空间与内存占用。

![图片](attachments/1f63b481ef91f1233ca62f486f6339a9_MD5.webp)

### **6.1. 限制纹理分辨率大小** 

在编辑器内，我们可以用高清的纹理，并通过调整这个值，就能在烘焙的时候将纹理限制到对应的分辨率大小。

![图片](attachments/cf5449d47741c4da5b5834fd1b14a1f0_MD5.webp)

还是和上面一样，我们可以调整全局设置。可以看到这里会为不同的纹理组设置不同的参数，找到想要修改的地方设置即可。

![图片](attachments/06d0b1c3fa5c82e49fb3b781b90e331e_MD5.webp)

推荐用矩阵批量修改资产，将角色纹理都设置成对应的角色纹理组。

![图片](attachments/863bbab6c6f2fefac660745a0ed24244_MD5.webp)

### 

### **6.2. Micro Detail** 

细节纹理容易在压缩纹理之后丢失掉，看起来会很糊。

![图片](attachments/ffa42c89428cab71bb7d6c058a937a77_MD5.webp)

所以我们可以将这些细节纹理用Shader的方式呈现，比如在材质中Tiling这些细节纹理，而不是将细节纹理烘焙在主纹理上。

![图片](attachments/b463853be255d49aab84458263bf4546_MD5.webp)

### 

### **6.3. 纹理压缩** 

虚幻的默认压缩是下图这两个。在导入纹理的时候，虚幻会尽可能自动检测纹理到底该用哪个压缩方式，但有时候可能会出错，因为我们有些纹理可能不需要Alpha通道。

![图片](attachments/94d8822e3aa5399c00e2293abbf24998_MD5.webp)

用Compress Without Alpha去掉Alpha通道即可。

![图片](attachments/b42f845a5b9707a806022766095267e2_MD5.webp)

Alpha通道剔除对比如下。    

![图片](attachments/50e6f677bd907ea71b4c0f327461fdd3_MD5.webp)

压缩算法的编码不同导致储存大小不同，对比如下图。如果我们的磁盘与内存真的不够，就需要重点考虑哪些纹理确实不需要Alpha通道，哪些纹理不需要高精度的颜色表现了。

![图片](attachments/d30a03c64ed0ab4c7034036995f9ca5e_MD5.webp)

有时候我们只需要单通道纹理，这时候G8压缩方法就比较好，这个方法会只留下Red通道。所有这些压缩方法可以在纹理的细节面板中调整。    

![图片](attachments/09554241438d12162361253cda2ebc9a_MD5.webp)

### 

### **6.4. Oodle编码** 

我们在打开纹理编辑器的时候可能就已经见过这个藏在角落的Oodle面板了，但这个东西到底有什么用？

![图片](attachments/22258d954cf27646e7e2499653bfc80c_MD5.webp)

这个面板可以让我们调整相关的纹理编码参数，当我们调整出了一个看起来很满意的参数之后就可以在BaseEngine配置文件中修改全局默认值了。    

![图片](attachments/ee8be91d698d17c4612c3e7ee06f3848_MD5.webp)

![图片](attachments/5a63763d4d90337636f5d0e1e75d5e72_MD5.webp)

### 

### **6.5. 通道合成** 

一个很常见的例子就是将AO遮罩、粗糙度遮罩和金属度遮罩合并成一张RGB纹理。我们甚至还可以加多一张Emissive或者别的什么遮罩放在Alpha通道里，随我们喜欢。这样我们就可以在材质中减少纹理采样，优化纹理复杂度。    

![图片](attachments/23308007b1b45d00be0e8e710d32fb4e_MD5.webp)

在权衡了纹理质量的前提下，想要追求极致优化，可以合成法线纹理。首先我们需要将法线纹理的压缩设置改回默认，然后在材质中这么写。这样我们就可以往法线纹理的B通道中加东西了。

![图片](attachments/b89bf242bf4625be773a6438914a02a5_MD5.webp)

注意！这种方案非常影响纹理的质量，下图是结果，请权衡好质量与优化。    

![图片](attachments/0eb087a97fb5cd8a74137217462eaffa_MD5.webp)

### 

### **6.6. 蒙版** 

大部分人会以为只能往RGBA纹理中塞4种蒙版，但其实我们可以往里面塞9种蒙版！

![图片](attachments/4ff5ca4e336ae19bda9256a4827e46e2_MD5.webp)

## **七、骨骼网格体组件** 

### **7.1. 包围盒** 

骨骼网格体组件还有更多参数设置。我们在更新骨骼网格体时会更新它的包围盒，包围盒的更新我们也可以进行一些调整。执行ShowFlag.Bounds 1可以显示组件的包围盒，这个可以帮助我们Debug。    

![图片](attachments/9432e21529f6ca8208a484f463b2db62_MD5.webp)

上文提到过，骨骼网格体可以跳过更新帧，然后通过插值对骨骼变形进行平滑。而包围盒的更新也可以跳过更新帧，并且不在平滑后更新。将包围盒更新模式调整成Skip Bounds Update When Interpolating即可。

因为遮蔽剔除和相机剔除都是用包围盒计算的，假如包围盒进入剔除范围，这个组件就不会被渲染。骨骼网格体组件可以固定包围盒，但存在一定的风险，它可能会在应该渲染的时候不渲染。当然，如果确定我们的角色不会超过这个包围盒，我们就可以放心使用固定包围盒。

![图片](attachments/4f2d9ee85fd7b207d3bd2383543da57c_MD5.webp)

如果我们采用了模块化角色方案，可以调整成使用父项骨骼网格体的包围盒模式。    

![图片](attachments/a3b60e2ecc9cb19b3feb3905ff90011c_MD5.webp)

以上这些设置能在这里找到。

![图片](attachments/cc274a269ece86649b125d950d5631bc_MD5.webp)

### 

### **7.2. 渲染静态** 

假如我们有一个骨骼网格体，但是它在游戏内不需要动画，这时候这个Render Static选项就很有用。并且这个选项可以在游戏内自由调节。    

![图片](attachments/90efc60f66568fdfded9ad314ae5957b_MD5.webp)

### 

### **7.3. Nanite小妙招** 

现在Nanite骨骼网格体还没出，但我们可以用点小伎俩。比如我们可以导入一个只有单个三角面的骨架（因为虚幻不允许导入没有面与蒙皮的骨骼网格体），然后将这个三角面关掉。

![图片](attachments/885e33d11ffa98bfc167373bb35892b9_MD5.webp)

导入一些静态网格体，静态网格体可以用Nanite，然后再将他们绑定在骨架上。    

![图片](attachments/fb91520c8b172c3871a674ab9647b8be_MD5.webp)

这样我们就得到了一个“Nanite骨骼网格体”，这非常适用于各种刚性的骨骼网格体上。

![图片](attachments/85507e258cc55431dcc0a659160aba43_MD5.webp)

## **八、蓝图**

### **8.1. Tick** 

优化的重点关注对象——Tick事件。在不需要的情况下，请默认关闭Tick。

![图片](attachments/9dcc0d36c5e31e4c633a78bf4b055c20_MD5.webp)

在蓝图中Actor上关掉还不行，Component也需要关掉。

在CPP中，我们可以从PrimaryActorTick或PrimaryComponentTick中关闭Tick。

![图片](attachments/53975f5ed3866ec3031d0f120557bb58_MD5.webp)

如果需要Tick，考虑一下是否时时刻刻需要Tick。如果不需要就可以调整Tick Rate。    

![图片](attachments/2028f86cd89baf9c6456fb1bf0049e23_MD5.webp)

在CPP中，也是在PrimaryActorTick或PrimaryComponentTick中调整Tick Rate。

![图片](attachments/d7ef5c38a27a0009176b8d3a53781069_MD5.webp)

执行dumpTicks指令可以输出现在在Tick的事件有哪些。

![图片](attachments/174d22b008dfaf801d1c247c2cce7d64_MD5.webp)

### 

### **8.2. 解决硬引用** 

引用如果处理不当也会出现大问题，这会导致资产拖着一堆引用，导致加载不畅或者内存占用高。当我们打开Size Map就能看到资产的硬引用，加载第三人称角色蓝图意味着要加载上Size Map上显示的这些资产。    

![图片](attachments/7927862071426d241326feac311040c1_MD5.webp)

举一个反面案例，这是硬引用处理不当导致的。加载角色的时候加载多了一些载具相关的东西。    

![图片](attachments/eac3a6d092b0c383d317a2983dc56e87_MD5.webp)

这是因为角色蓝图里有一个载具类引用的变量，或者Cast To了载具类。

![图片](attachments/aeb7ac567415a26d2523315c7612e73a_MD5.webp)

如何处理Cast就很重要了，首先如果我们确实需要用到某个类，放心Cast，比如角色与动画蓝图之间的Cast。

![图片](attachments/8a21774ba9f1ece20070146d16c244c3_MD5.webp)

并且我们可以用检查类替换Cast。    

![图片](attachments/1b21731894b8a821764ffbcabc076570_MD5.webp)

但如果我们真的需要用到类里面的逻辑怎么办？可以试试用接口。

![图片](attachments/f47f215c1e3dd321b3c9e3773bdd99ca_MD5.webp)

当我们创建了一个蓝图接口，并且加入了我们需要的函数，就可以在Object中实现我们的接口。    

![图片](attachments/0e910d0afe21aeb3aa6de9410ed24081_MD5.webp)

然后在蓝图中实现它即可。

![图片](attachments/8453d632b74dbc604369a96d57ecae44_MD5.webp)

这样我们就用接口代替了Cast调用了函数。    

![图片](attachments/d983c0391439ba32f04364227a7e525b_MD5.webp)

### 

### **8.3. 软引用** 

虚幻5.4可以将变量调整成软引用。

![图片](attachments/650f30e43b505f2270a7e69765f84d73_MD5.webp)

旧版本中我们需要这么调整。

![图片](attachments/a0f4ea7516a6f6d8fb5afc9985b350d2_MD5.webp)

软引用能做的东西不多，并且我们在使用它之前得将它加载成硬引用。Blocking节点会阻塞游戏线程，而Async节点会异步完成加载任务。    

![图片](attachments/6ab0db979a2293425f9e6aae96a1a765_MD5.webp)

要注意的是，以上这些节点加载出来的引用会卡在蓝图的生命周期里，不会被垃圾收集处理，在加载完，完成了对应的任务之后，推荐用一个Set Object Reference (by ref)节点清掉这个引用，让垃圾收集处理它。

![图片](attachments/497f756077746d10849a92fa8be10f1b_MD5.webp)

### 

### **8.4. 子蓝图** 

我们一般会将角色蓝图的子蓝图作为角色的变体，修改里面的网格体和里面的一些参数。这个例子是用Quinn的主蓝图生成了一个Mannequin的子蓝图。

![图片](attachments/cba2b4639ae3624011a7e118c3bfe24a_MD5.webp)

当我们打开子蓝图的Size Map就会发现，它加载上了主蓝图中的Quinn骨骼网格体。

![图片](attachments/52bdeaa181183d9687e50d54b3db9dbc_MD5.webp)

这种情况下，需要将主蓝图中的网格体或者其他一些硬引用去掉。

![图片](attachments/cad91b3686aa213b3c7c8156a2be340a_MD5.webp)

然后再创建两个子蓝图，分别对应Quinn和Mannequin。这样两个子蓝图就会只加载自己对应的引用资产。

![图片](attachments/b242eae47a9fe302af5824e01e3aaf95_MD5.webp)

# **结语**

这次分享真的干货满满，门槛很低，但能解决不少优化问题。LOD、纹理、骨骼网格体、蓝图等等一应俱全，全方面解析了角色与动画方面的性能问题，并分享了对应的解决方案。希望这次的分享能够给您带来帮助，祝创作愉快，工作顺利。