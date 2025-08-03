# Maya API编程 
[Maya API Programming | Chad Vernon](https://www.chadvernon.com/maya-api-programming/)
[](http://www.cgcircuit.com/course/introduction-to-the-maya-api?affid=ef44e69526a3d370b2fdcd141b5e0e2710ed9c1ed68109c0d58e39a516ec0cb16af1166111d27e654aca6abdfecc0a850cc048bbf30827c68fc655f3f465b707)查看我在CGCircuit上的Maya API视频系列简介：

##  介绍 

本研讨会面向希望学习如何使用 Maya API 扩展和自定义 Maya 的个人。个人应具有现有的 C++ 和/或 Python 经验以及中高级的 Maya 知识水平。充分了解面向对象编程 （OOP） 非常有帮助，因为 Maya API 大量使用 OOP。您不会从本次研讨会中了解有关 Maya API 的所有信息。本次研讨会的目的不是让您成为专业的Maya程序员，而是为您提供坚实的基础，以进一步学习Maya API。

此工作流程中包含的技术和代码可能并不完美，或者被精英Maya API程序员接受为利用API的最佳方式。这里介绍的代码和知识基于我在大型工作室制作动画和效果密集型故事片时使用 Maya API 在 C++ 和 Python 中创建数十个节点、变形器和工具集的经验。如果您认为某些内容不正确，请告诉我。 Maya API 学习资源有限，因此希望这些说明能帮助您添加到工具集中。

### 什么是 Maya API？

Maya API是一个C++/Python API，允许程序员和脚本编写者访问Maya的内部库。借助Maya API，程序员可以使用新技术自定义Maya，并创建工具来帮助将软件集成到工作室的制作流程中。使用 Maya API 编写的任务的执行速度比使用 MEL 编写的相同任务快几倍。

### Maya API 可以实现什么？

Maya API 传统上用于制作插件，这些插件是 Maya 在运行时加载的动态库。插件包含要添加到 Maya 的许多不同类型对象的实现。当我在这里提到“对象”时，我指的是面向对象编程意义上的对象。Maya API提供了多个基类，程序员将继承这些基类并填充所需的实现。一些可能的对象类型是：

-  渲染视口。 
-  纹理烘焙引擎。 
-  命令 
-  约束 
-  变形器 
-  粒子和流体发射器 
-  着色 
-  IK 求解器 
-  依赖节点 
-  OpenGL 定位器 
-  文件导出器 
-  工具 

从 Maya 8.5 开始，Maya API 可以通过 Python 访问。使用 Python，我们不仅可以制作上述插件，还可以在脚本中访问 API 命令，这为现有工具集增加了显着的性能提升。

###  C++ 与 Python 

插件可以用 C++ 和 Python 制作。那么你应该使用哪一个呢？两者都很有用，但在某些情况下，应该使用一个而不是另一个。

为了速度，任何复杂的或适用于变形器等较大数据集的东西都应该用 C++ 制作。对于性能不重要的简单节点，Python 可以正常工作。任何处理 OpenGL 的东西，例如视口和定位器，都应该使用 C++ 制作，因为我已经看到 Python 实现的速度显着下降。

此外，Python 中的一些 API 调用在语法方面非常痛苦，因为 API 需要大量的 C++ 指针和引用，这些指针和引用被 Python 中一个非常神秘的模块 （MScriptUtil） 包装，但没有很好地记录。

我在开发插件时同时使用了 C++ 和 Python。当我编写一个新节点时，我有时会从 Python 开始计算算法细节。由于 Python 不像 C++ 那样编译，因此迭代时间更快。Maya 因数组索引和内存错误而崩溃的可能性也较小。

大多数时候，我坚持使用 C++，只是因为这就是最终产品。但是，我在脚本中经常使用 Python 和 API，因此仍然值得学习。所有 API 调用都是相同的;这只是语法上的差异。

### 设置您的开发环境

学习 API 的第一步是设置构建环境。Maya API 打包为一组需要访问的库。从文档中，这些库是：

- OpenMaya - 包含用于定义节点和命令以及将它们组合到插件中的基本类。
- OpenMayaUI - 包含创建新用户界面元素（如纵器、上下文和定位器）所需的类。
- OpenMayaAnim - 包含动画类，包括变形器和反向运动学。
- OpenMayaFX - 包含Autodesk Dynamics的类。
- OpenMayaRender - 包含用于执行渲染函数的类。

####  蟒 

如果您使用的是 Python，访问这些库就像将它们导入到代码中一样简单：

```python
import maya.OpenMaya
import maya.OpenMayaUI
import maya.OpenMayaAnim
import maya.OpenMayaFX
import maya.OpenMayaRender
```

####  C++ 

[](https://www.youtube.com/watch?v=2mUOt_F2ywo&list=PL_RMNSHxKvdUFTdl12WumiqnNWLn4LDQj)[](https://github.com/chadmv/cgcmake)我建议使用 CMake 来帮助在 Windows、Linux 和 OSX 上创建构建环境。您可以观看我创建的视频系列，介绍如何将 CMake 与 Maya 一起使用。相应的 CMake 模块可以在我的 github 项目上找到。

##  Maya 依赖关系图 

[](https://knowledge.autodesk.com/support/maya/learn-explore/caas/simplecontent/content/using-parallel-maya.html)从 Maya 2016 开始，Maya 引入了新的多线程评估模型。要了解有关此模型的更多信息，请阅读此处链接的论文。

本页的其余部分将介绍具有脏传播的旧版 Maya 2016 之前的评估模型。

[](http://help.autodesk.com/view/MAYAUL/2018/ENU//?guid=__files_Dependency_graph_plugins_Dependency_Graph_DG_nodes_htm)在编写大多数 Maya 插件时，必须了解 Maya 依赖关系图体系结构。 Maya DG 的解释可以在大多数 Maya 书籍和文档中找到。 它基本上是一个将信息从一个节点传递到下一个节点的节点网络。 开发人员需要了解 DG 的最重要方面是 Maya 如何以及何时通过图形重新计算和传播数据。

节点有一组输入和输出。 输出取决于输入的值。 这些输出被称为其相应输入的依赖项，并且输入会影响相应的输出。  作为一种优化，Maya 的 DG 设计为仅在需要时计算数据。 它通过节点输入和输出上的脏标志来实现这一点。 当输入值发生更改时，任何依赖输出都会被标记为脏。 输出实际上不会重新计算。 与此输出的任何连接都被标记为脏，并且脏传播一直持续到到达图的末尾。 尚未发生数据重新计算;只有肮脏的旗帜被推过了总干事。 当Maya请求DG重新求值时（例如在屏幕刷新中），Maya将检查节点输出是否脏。 如果是，Maya 会告诉节点对自身进行求值。  当该节点求值时，它会发现其输入是脏的，因此要求任何连接的输入节点重新求值。 此过程一直持续到重新评估图中的数据并将输入和输出标记为干净。

当尝试找出节点未被计算的原因时，这些知识非常有用。 如果未计算节点，则不会请求其输出。

由于 Maya DG 架构的描述已经在其他地方进行了深入讨论，因此我不会在这里重现它。 我建议在文档以及其他各种 Maya 书籍和白皮书中阅读有关 Maya 依赖关系图架构的更多信息。

![](Notes/MAYA/Maya%20Python%20API/attachments/874ee83611dac9d63e43b9db40a0e250_MD5.png "DGEvaluation")

## Maya API 简介

###  对象类型 

Maya API 由四种类型的 C++ 对象组成：包装器、对象、函数集和代理。

####  包装 

包装器只是数据或数学结构的便利类。Maya API 包括数组、向量、矩阵、四元数等的包装器。包装器还包括实用工具，例如选择列表、DAG 路径、视口等。这些类以“M”前缀开头。示例包括 MIntArray、MFloatArray、MMatrix、MVector、MQuaternion、MPlane、MPointArray、MSelectionList 等。

包装器还包括迭代器，迭代器是用于遍历数据序列的类。有一些迭代器可以遍历 Maya 的依赖关系图，迭代网格顶点、边和面，迭代表面 cvs 等。迭代器类以“MIt”为前缀，包括 MItMesh、MItDependencyGraph、MItKeyFrame、MItMeshEdge、MItSurfaceCV 等。

####  对象 

[](http://docs.autodesk.com/MAYAUL/2014/ENU/Maya-API-Documentation/files/API_MObject.htm)对象称为 MObject ，是表示所有Maya对象（曲线、曲面、DAG节点、DG节点、灯光、着色器、纹理、IK解算器、动力学场等）的通用基类。这个通用基础允许通过API传递许多不同类型的MObject，并允许API开发人员利用Maya中所有节点的继承结构。MObject 的每个实例表示节点或节点上的属性。但是，MObject 并不是真正的节点或属性，而是节点或属性的句柄。这样，Maya 可以保持节点和属性的所有权，并确保它运行所有必要的例程，以保持 Maya 平稳运行。由于 MObject 是指向内部 Maya 对象的指针，因此不应在调用插件之间挂起 MObject，因为 Maya 可能会在内存中移动这些内部对象，从而使 MObject 无效。为了访问 MObject 所代表的数据的特定功能，我们使用函数集。

#### 功能集

由于 MObject 是所有节点的基类，因此在 MObject 类中包含与节点交互所需的所有函数是不切实际的。在特定类型的节点上运行的函数被分解为称为函数集的 C++ 类。例如，有用于摄像机、蒙皮簇、IK 手柄、网格、表面、变换等的函数集。函数集对 MObject 进行作。对象和函数集的常规工作流是使用 MFn：：Type 枚举确定对象与哪个函数集兼容，然后将该函数集附加到对象：

```cpp
if (obj.hasFn(MFn::kMesh)) {
  MFnMesh fnMesh(obj);
}
```

```python
if obj.hasFn(OpenMaya.MFn.kMesh):
    fnMesh = OpenMaya.MFnMesh(obj)
```

通常，你已经知道 MObject 表示的数据类型，不需要显式检查数据类型。函数集类以“MFn”为前缀。示例包括 MFnMesh、MFnNurbsCurve、MFnDagNode、MFnLatticeDeformer、MFnRenderPass 等。

对象/函数集工作流程创建了数据与功能的分离，这与经典 OOP 不同，在经典 OOP 中，类通常封装数据和功能以对数据进行作。在Maya中，数据用MObject表示，功能通过函数集实现。

#### 代理

代理是插件开发人员用来实现新型 Maya 对象（如自定义节点、变形器、ik 解算器、命令、变换等）的抽象类。在开发新对象时，我们创建一个继承自这些代理类之一的新类，然后实现所有必需的功能。代理类以“MPx”为前缀，包括 MPxNode、MPxDeformerNode、MPxConstraint、MPxCommand、MPxIkSolver 等。

### 错误检查

[](http://docs.autodesk.com/MAYAUL/2014/ENU/Maya-API-Documentation/files/API_MStatus_class.htm)C++ 中的错误检查是使用 MStatus 类完成的。API 中的大多数函数都接受或返回 MStatus 变量。我们可以查询这个变量来确定特定函数是否成功。如果函数失败，MStatus 变量将包含有关函数失败原因的信息。检查这些错误非常重要，因为当 Maya API 中的函数失败时，它们会以静默方式失败。不会有任何警告，其余代码可能无法正常工作，或者Maya可能会崩溃。因此，应始终检查函数是否成功使用 MStatus。

```cpp
// oMesh is an MObject for a mesh object and so can’t be used with
// the NURBS surface function set
MFnNurbsSurface fnSurface(oMesh, &status);
if (status.error()) {
  std::cerr << "nAPI error detected in " << __FILE__ << " at line " << __LINE__ << endl;
  status.perror("Something went wrong!");
}
```

Maya API附带了几个有用的宏，用于检查MStatus变量。这些都是：

```cpp
CHECK_MSTATUS(status);
CHECK_MSTATUS_AND_RETURN_IT(status);
```

`CHECK_MSTATUS` 宏执行与上述相同的功能。`CHECK_MSTATUS_AND_RETURN_IT` 宏与 `CHECK_MSTATUS` 相同，只是如果失败，它会返回状态。

MStatus 不适用于 Python。将Maya API与Python一起使用时，失败的函数将引发异常，您可以使用Python的内置错误处理来处理它。

```python
try:
    fnSurface = OpenMaya.MFnNurbsSurface(oMesh)
except:
    print("Something went wrong!")
```

## 您的第一个插件

作为Maya API的介绍，我们将创建一个简单的命令插件。 这将显示所有插件中通用的模板代码，并显示前面讨论的各种Maya API概念。 该命令将简单地将文本打印到脚本编辑器中。

在所有插件中，您需要实现 3 个常用功能：

- [](http://download.autodesk.com/us/maya/2011help/files/Command_plugins_initializePlugin.htm)initializePlugin – 加载插件时调用。 用于向Maya注册新命令、工具、节点等。
- [](http://download.autodesk.com/us/maya/2011help/files/Command_plugins_uninitializePlugin.htm)uninitializePlugin – 卸载插件时调用。 用于取消注册在 initializedPlugin 中注册的任何内容。
- [](http://download.autodesk.com/us/maya/2011help/files/Command_plugins_Creator_methods.htm)creator – Maya 调用此函数以创建对象的新实例，例如在调用 createNode 或调用命令时。

这些函数在我们的 HelloWorld 命令中如下所示：

```cpp
void* HelloWorld::creator() {
  return new HelloWorld;
}

MStatus initializePlugin(MObject obj) {
  MFnPlugin plugin(obj, "Chad Vernon", "1.0", "Any");
  MStatus status = plugin.registerCommand("helloWorld", HelloWorld::creator);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  return status;
}

MStatus uninitializePlugin(MObject obj) {
  MFnPlugin plugin(obj);
  MStatus status = plugin.deregisterCommand("helloWorld");
  CHECK_MSTATUS_AND_RETURN_IT(status);
  return status;
}
```

这是样板代码，通常被复制并粘贴到我所有的插件中，并稍微更改以包含插件中包含的所有节点/命令/变形器。 该代码只是注册和注销我们的插件包含的任何新节点、命令等。 这也是我们告诉Maya我们要创建的节点类型的地方，例如它是普通依赖节点、变形器、自定义定位器、ik解算器、约束等。

您可以在文档中阅读这些函数的详细信息，但我们可以在这里指定插件版本号、所需的Maya版本、插件作者等。

由于我们正在实现一个新命令，因此我们需要创建一个继承代理类 MPxCommand 的类：

```cpp
#ifndef HELLOWORLD_H
#define HELLOWORLD_H

#include <maya/MArgList.h>
#include <maya/MObject.h>
#include <maya/MGlobal.h>
#include <maya/MPxCommand.h>

class HelloWorld : public MPxCommand {
public:
  HelloWorld() {};
  virtual MStatus doIt(const MArgList&);
  static void* creator();
};
#endif
```

上面的代码显示了 HelloWorld 命令的标头声明。 我们首先包含必要的头文件。 Maya 中的每个类都有自己的头文件，因此，如果在插件中使用特定类，则需要包含其头文件才能使用它。

[](http://download.autodesk.com/us/maya/2011help/API/class_m_px_command.html)MPxCommand 的文档列出了我们可以选择实现的许多不同函数。由于这是我们的第一个插件，我们只会实现命令的一个必要功能：doIt 函数。 当我们最终在Maya中调用新命令时，Maya将创建新的HelloWorld对象，然后调用该对象的doIt函数。 doIt 函数如下所示：

```cpp
MStatus HelloWorld::doIt(const MArgList&) {
  MGlobal::displayInfo("Hello World!");
  return MS::kSuccess;
}
```

[](http://download.autodesk.com/us/maya/2011help/API/class_m_global.html)MPxCommand：:d o它接受一个 MArgList 对象，该对象用于传入命令参数。 我们将在后面的部分中学习如何使用它。 此函数中唯一感兴趣的行是 MGlobal：:d isplayInfo 调用。 MGlobal 是一个类，它提供了许多有用的功能，例如打印文本和选择对象。 在这里，我们只是打印一些文本。

一旦插件编译并加载完毕，我们就可以用以下命令调用该命令：

```python
import maya.cmds as cmds
cmds.helloWorld()
```

整个插件如下所示：

```cpp
// HelloWorldCmd.h

#ifndef HELLOWORLD_H
#define HELLOWORLD_H

#include <maya/MArgList.h>
#include <maya/MObject.h>
#include <maya/MGlobal.h>
#include <maya/MPxCommand.h>

class HelloWorld : public MPxCommand {
public:
  HelloWorld() {};
  virtual MStatus doIt(const MArgList&);
  static void* creator();
};
#endif
```

```cpp
// HelloWorldCmd.cpp

#include "include/HelloWorldCmd.h"
#include <maya/MFnPlugin.h>
void* HelloWorld::creator() {
  return new HelloWorld;
}

MStatus HelloWorld::doIt(const MArgList& argList) {
  MGlobal::displayInfo("Hello World!");
  return MS::kSuccess;
}

MStatus initializePlugin(MObject obj) {
  MFnPlugin plugin(obj, "Chad Vernon", "1.0", "Any");
  MStatus status = plugin.registerCommand("helloWorld", HelloWorld::creator);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  return status;
}

MStatus uninitializePlugin(MObject obj) {
  MFnPlugin plugin(obj);
  MStatus status = plugin.deregisterCommand("helloWorld");
  CHECK_MSTATUS_AND_RETURN_IT(status);
  return status;
}
```

需要记住的一件事是，maya/MFnPlugin.h 应该只包含在插件中一次。 此头文件是向Maya注册插件所必需的。 如果将其包含在插件的多个源文件中，则会收到错误。 如果你的插件有多个节点和命令，你可能会将 initializePlugin 和 uninitializePlugin 函数放在一个单独的文件中，因此只需在该文件中包含 MFnPlugin。

该命令的相同 Python 实现是：

```python
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

class HelloWorld(OpenMayaMPx.MPxCommand):
        
    def doIt(self, argList):
        print("Hello World!")
        
def creator():
    return OpenMayaMPx.asMPxPtr(HelloWorld())

def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, "Chad Vernon", "1.0", "Any")
    try:
        plugin.registerCommand("helloWorld", creator)
    except:
        raise RuntimeError("Failed to register command")

def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterCommand("helloWorld")
    except:
    raise RuntimeError("Failed to unregister command")
```

在 Python 中，我们可以使用 MGlobal 类来打印文本，也可以只使用内置的 Python 打印命令。

现在我们已经引入了 Maya API，我们可以开始学习如何实现更有趣和有用的插件。

## 依赖图插件简介

[](http://download.autodesk.com/us/maya/2011help/files/Dependency_graph_plugins.htm)依赖关系图插件是最常见的插件类型。开发人员通常会创建自定义节点来执行某种数学计算或几何运算。在继续之前，应阅读Maya文档的“依赖关系图插件”部分。它包含许多有关Maya依赖关系图架构和节点创建工作流的有用信息。阅读该信息后，在创建第一个依赖关系图节点时，将更容易进行作。我们的第一个节点将是一个简单的节点，它接受一个输入浮点值，将其加倍，并将加倍值设置为输出。它是一个相当没用的节点，但它会向我们介绍节点插件的结构，并为更有趣的节点奠定基础。

为了创建依赖图节点，我们创建一个继承自代理类 MPxNode 的类：

```cpp
// DoublerNode.h

#ifndef DOUBLERNODE_H
#define DOUBLERNODE_H
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MStatus.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MPxNode.h>
class DoublerNode : public MPxNode {
 public:
  DoublerNode() {}
  virtual MStatus compute(const MPlug& plug, MDataBlock& data);
  static void* creator();
  static MStatus initialize();
  
  static MTypeId id;
  static MObject aInput;
  static MObject aOutput;
};
#endif
```

这应该看起来与我们之前创建的命令非常相似。我们实现的不是 doIt 函数，而是计算函数。我们还有一些静态成员变量。MObject表示节点将具有的属性。“a”前缀只是我对表示节点属性的 MObject 遵循的命名约定。

MTypeId 成员变量是创建的所有节点中必需的 id 值。Maya 中的所有节点都需要唯一的十六进制 ID 号。从 Maya 文档中：

> 对于节点的本地测试，您可以使用 0x00000000 和 0x0007ffff 之间的任何标识符，但对于计划用于更永久目的的任何节点，您应该从 Autodesk 技术支持获取通用唯一 ID。您将被分配一个可以自行管理的唯一范围。

[](http://mayaid.autodesk.io/)如果要在工作室创建节点，则应向Autodesk请求ID范围。如果仅使用随机 id 值，则它可能会与现有节点 id 值发生冲突，并且你会在 Maya 中看到不良行为。您可以在此处请求节点 ID 块

### 属性

节点可以具有许多不同类型的输入和输出属性，从整数、浮点数和布尔值等数值属性，到网格、曲线、数值数组等更复杂的类型。在实现新节点时，我们需要定义该节点的所有属性以及哪些属性将触发脏标志传播。我们在向Maya注册节点时指定的初始化函数中执行此作。这是 DoublerNode 的初始化函数：

```cpp
MStatus DoublerNode::initialize() {
  MFnNumericAttribute nAttr;
 
  aOutput = nAttr.create("output", "out", MFnNumericData::kFloat);
  nAttr.setWritable(false);
  nAttr.setStorable(false);
  addAttribute(aOutput);
 
  aInput = nAttr.create("input", "in", MFnNumericData::kFloat);
  nAttr.setKeyable(true);
  addAttribute(aInput);
  attributeAffects(aInput, aOutput);
 
  return MS::kSuccess;
}
```

[](http://download.autodesk.com/us/maya/2011help/API/class_m_fn_numeric_attribute.html)由于我们的节点仅包含数字属性，因此我们使用 MFnNumericAttribute 创建它们。有不同的类可以创建不同类型的属性;这些包括：

- [MFn复合属性](http://download.autodesk.com/us/maya/2011help/API/class_m_fn_compound_attribute.html)
- [MFnEnum属性](http://download.autodesk.com/us/maya/2011help/API/class_m_fn_enum_attribute.html)
- [MFn通用属性](http://download.autodesk.com/us/maya/2011help/API/class_m_fn_generic_attribute.html)
- [MFnLightData属性](http://download.autodesk.com/us/maya/2011help/API/class_m_fn_light_data_attribute.html)
- [MFn矩阵属性](http://download.autodesk.com/us/maya/2011help/API/class_m_fn_matrix_attribute.html)
- [MFnMessage属性](http://download.autodesk.com/us/maya/2011help/API/class_m_fn_message_attribute.html)
- [MFnNumeric属性](http://download.autodesk.com/us/maya/2011help/API/class_m_fn_numeric_attribute.html)
- [MFnTyped属性](http://download.autodesk.com/us/maya/2011help/API/class_m_fn_typed_attribute.html)
- [MFn单元属性](http://download.autodesk.com/us/maya/2011help/API/class_m_fn_unit_attribute.html)

我们将在后面的章节中介绍它们。

在创建属性时，我们需要为属性指定各种选项，例如属性是输入还是输出、是否可键入、数组、缓存、保存文件时存储等。在上面的示例中，通过将 aOutput 属性设置为不可写，我们指定它永远不能使用 setAttr 命令进行设置，并且不能用作目标连接;基本上，该属性是一个输出属性，只有节点本身应该设置其值。通过将 storeable 设置为 false，我们告诉 Maya 在保存场景时不要将此值存储在 .mb 或 .马 文件中。这是有道理的，因为它是一个输出属性，因此无论如何都会计算出该值，因此无需将其存储到磁盘。

[](http://download.autodesk.com/us/maya/2011help/API/class_m_fn_attribute.html)[](http://download.autodesk.com/us/maya/2011help/API/class_m_px_node.html#c7eddfe936bc124fdc1902f16098aaba)然后创建 aInput 属性并将其设置为可设置关键帧。当属性可设置关键帧时，当选择节点时，该属性将显示在通道框中。若要了解可以为属性设置的所有选项，请参阅 MFnAttribute 文档。创建 aInput 属性并将其添加到节点后，我们通过调用 attributeAffects 指定 aInput 属性影响 aOutput 属性。这将创建输入/输出关系，该关系告诉Maya，当输入发生更改时，它应将输出标记为脏，并且Maya在下次请求时需要重新计算它。您需要为节点中的每个属性依赖项调用此函数。

### 插头

[](http://download.autodesk.com/us/maya/2011help/API/class_m_plug.html)Maya API 具有属性和插件的概念。脚本编写者可能熟悉属性是节点上可用值和选项的集合。在 API 中，属性是指定义节点并在相同类型的节点之间共享的数据接口。例如，所有 polySphere 节点都具有半径属性。属性的实际数据或值存储在插件中。实际的 C++ 类是 MPlug 。因此，属性在相同类型的所有节点之间共享，并且插件对于节点的单个实例是唯一的。在整个研讨会中谈论属性和插头时，我可能会互换提及它们，但从技术上讲，两者之间是有区别的。

### 数据块和数据句柄

[](http://download.autodesk.com/us/maya/2011help/API/class_m_data_block.html)[](http://download.autodesk.com/us/maya/2011help/API/class_m_data_handle.html)创建新节点时，我们需要注意两个对象。它们是 MDataBlock 和 MDataHandle 。数据块是计算输出属性所需的所有数据的节点存储对象。在计算节点输出时，所有属性值、输入和输出都通过数据块进行管理。此数据块对象仅在计算节点输出期间有效，因此不应存储指向数据块的指针。

为了访问数据块内的数据，我们使用数据句柄。数据句柄是指向数据块内数据的指针对象。使用数据块和句柄的一般工作流程是：

1. 请求从数据块到特定属性的数据句柄。Maya 提供数据块。
2. 从数据句柄读取数据。
3. 执行我们的计算。
4. 请求输出数据句柄，以便我们可以将输出存储到数据块中。
5. 使用输出数据句柄将计算数据存储到数据块中。

[](http://download.autodesk.com/us/maya/2011help/API/class_m_array_data_handle.html)在某些情况下，我们从属性中读取数组数据。在这些情况下，我们使用 MArrayDataHandle 对象。我们将在后面的部分中了解有关本类的更多信息。

在计算输出属性时，我们应该只使用通过其数据块提供给节点的数据。这包括任何输入属性和连接。我们永远不应该将目光投向节点外部来获取计算所需的数据。例如，假设我们编写一个节点，并且我们想要规范化的绘制权重贴图，例如在皮肤簇节点上。在计算节点中的输出插件时，我们不应该在 DG 中找到蒙皮簇节点并查询其权重值。如果需要这些权重值，则应使用单独的命令将这些权重复制到节点数据块中，创建自己的绘制权重归一化算法，或将所有绘制的权重插件连接到节点。如果在节点计算时查看节点外部，则可能会触发不需要的节点评估。节点应该表现得像一个黑匣子，并且只知道它的输入和输出。

### 计算函数

通过在initialize函数中定义的节点属性接口，我们现在可以实现输出值的实际计算。这是在节点计算方法中完成的。每当Maya从节点请求输出值并且输出值为脏时，Maya将调用该节点计算函数来重新计算输出值。在我们的节点中，我们只需获取输入值，将其加倍，然后将其设置为输出：

```cpp
MStatus DoublerNode::compute(const MPlug& plug, MDataBlock& data) {
  if (plug != aOutput) {
    return MS::kUnknownParameter;
  }
  // Get the input
  float inputValue = data.inputValue(aInput).asFloat();
 
  // Double it
  inputValue *= 2.0f;
 
  // Set the output
  MDataHandle hOutput = data.outputValue(aOutput);
  hOutput.setFloat(inputValue);
  data.setClean(plug);
  return MS::kSuccess;
}
```

此计算函数执行前面概述的相同工作流步骤。我们在同一行上获取输入数据句柄和输入值。然后，我们执行计算，获取输出数据句柄，然后将结果存储回数据块中。计算并存储输出后，我们需要将输出插头标记为干净，以便Maya知道不要再次计算其值。

初始条件语句检查 Maya 当前请求的输出插件。这是为了确保我们不会执行不必要的计算，并允许我们在节点具有多个输出属性时过滤我们的计算。当所有内容都计算完毕并存储回数据块时，我们返回一个成功代码，以告诉 Maya 没有任何问题。

下面列出了 DoublerNode 的整个插件：

```cpp
// DoublerNode.h

#ifndef DOUBLERNODE_H
#define DOUBLERNODE_H
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MStatus.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MPxNode.h>
class DoublerNode : public MPxNode {
 public:
  DoublerNode() {}
  virtual MStatus compute(const MPlug& plug, MDataBlock& data);
  static void* creator();
  static MStatus initialize();
  
  static MTypeId id;
  static MObject aInput;
  static MObject aOutput;
};
#endif
```

```cpp
// DoublerNode.cpp

#include "include/DoublerNode.h"
#include <maya/MFnPlugin.h>
 
MTypeId DoublerNode::id(0x00000001);
MObject DoublerNode::aInput;
MObject DoublerNode::aOutput;
 
void* DoublerNode::creator() { return new DoublerNode; }
MStatus DoublerNode::compute(const MPlug& plug, MDataBlock& data) {
  if (plug != aOutput) {
    return MS::kUnknownParameter;
  }
  // Get the input
  float inputValue = data.inputValue(aInput).asFloat();
 
  // Double it
  inputValue *= 2.0f;
 
  // Set the output
  MDataHandle hOutput = data.outputValue(aOutput);
  hOutput.setFloat(inputValue);
  data.setClean(plug);
  return MS::kSuccess;
}
 
MStatus DoublerNode::initialize() {
  MFnNumericAttribute nAttr;
 
  aOutput = nAttr.create("output", "out", MFnNumericData::kFloat);
  nAttr.setWritable(false);
  nAttr.setStorable(false);
  addAttribute(aOutput);
 
  aInput = nAttr.create("input", "in", MFnNumericData::kFloat);
  nAttr.setKeyable(true);
  addAttribute(aInput);
  attributeAffects(aInput, aOutput);
 
  return MS::kSuccess;
}
 
MStatus initializePlugin(MObject obj) {
  MStatus status;
  MFnPlugin plugin(obj, "Chad Vernon", "1.0", "Any");
 
  status = plugin.registerNode("doublerNode", DoublerNode::id, DoublerNode::creator, DoublerNode::initialize);
  CHECK_MSTATUS_AND_RETURN_IT(status);
 
  return status;
}
 
MStatus uninitializePlugin(MObject obj) {
  MStatus status;
  MFnPlugin plugin(obj);
 
  status = plugin.deregisterNode(DoublerNode::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);
 
  return status;
}
```

这是相应的 Python 实现：

```python
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
 
class DoublerNode(OpenMayaMPx.MPxNode):
    kPluginNodeId = OpenMaya.MTypeId(0x00000001)
 
    aInput = OpenMaya.MObject()
    aOutput = OpenMaya.MObject()
 
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
 
    def compute(self, plug, data):
        if plug != DoublerNode.aOutput:
            return OpenMaya.MStatus.kUnknownParameter
 
        inputValue = data.inputValue(DoublerNode.aInput).asFloat()
        inputValue *= 2.0
        hOutput = data.outputValue(DoublerNode.aOutput)
        hOutput.setFloat(inputValue)
        data.setClean(plug)
 
        return OpenMaya.MStatus.kSuccess
 
def creator():
    return OpenMayaMPx.asMPxPtr(DoublerNode())
 
def initialize():
    nAttr = OpenMaya.MFnNumericAttribute()
 
    DoublerNode.aOutput = nAttr.create('output', 'out', OpenMaya.MFnNumericData.kFloat)
    nAttr.setWritable(False)
    nAttr.setStorable(False)
    DoublerNode.addAttribute(DoublerNode.aOutput)
 
    DoublerNode.aInput = nAttr.create('input', 'in', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    DoublerNode.addAttribute(DoublerNode.aInput)
    DoublerNode.attributeAffects(DoublerNode.aInput, DoublerNode.aOutput)
 
def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Chad Vernon', '1.0', 'Any')
    try:
        plugin.registerNode('doublerNode', DoublerNode.kPluginNodeId, creator, initialize)
    except:
        raise RuntimeError('Failed to register node')
 
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(DoublerNode.kPluginNodeId)
    except:
        raise RuntimeError('Failed to register node')
```

当插件编译并加载时，我们可以用以下代码对其进行测试：

```python
import maya.cmds as cmds
node = cmds.createNode('doublerNode')
locator = cmds.spaceLocator()[0]
cmds.connectAttr('{}.output'.format(node), '{}.ty'.format(locator))
```

此代码创建一个 douberNode 并将其连接到定位器的 translateY 值。对 doublerNode 的输入进行动画处理会显示节点的效果。

## 变形器

[](http://download.autodesk.com/us/maya/2011help/API/class_m_px_deformer_node.html)变形器是依赖图节点的子集，它们对输入几何体执行变形算法，并将变形的几何体输出到变形器的输出属性。 当您考虑在网格体或表面上移动点或 CV 的算法时，您通常希望创建变形器。 我过去实现的变形器示例包括包裹、抖动、位移、混合形状和蒙皮滑动变形器。 要创建变形器节点，我们创建一个继承自代理类 MPxDeformerNode 的类。

[](http://download.autodesk.com/us/maya/2011help/CommandsPython/deformer.html)由于变形器是依赖节点的子集，因此可以像所有其他节点一样使用 createNode 命令创建它们，但是，变形器具有许多特殊功能，这些功能取决于与变形器节点建立的其他连接。 当您使用变形器命令时，将为您建立这些连接。 此功能包括成员资格编辑和变形历史的重新排序。

变形器具有与普通依赖节点相同的结构，只是我们实现了变形函数而不是计算函数。 为了展示制作变形器所涉及的一些过程，我们将创建一个简单的混合形状节点，用于将一个网格体混合到另一个网格体。

作为变形器的输入，我们需要一个目标网格体和一个混合权重值：

```cpp
MStatus BlendNode::initialize() {
  MFnTypedAttribute tAttr;
  MFnNumericAttribute nAttr;
     
  aBlendMesh = tAttr.create("blendMesh", "blendMesh", MFnData::kMesh);
  addAttribute(aBlendMesh);
  attributeAffects(aBlendMesh, outputGeom);
  
  aBlendWeight = nAttr.create("blendWeight", "bw", MFnNumericData::kFloat);
  nAttr.setKeyable(true);
  addAttribute(aBlendWeight);
  attributeAffects(aBlendWeight, outputGeom);
 
  // Make the deformer weights paintable
  MGlobal::executeCommand( "makePaintable -attrType multiFloat -sm deformer blendNode weights;" );
 
  return MS::kSuccess;
}
```

[](http://download.autodesk.com/us/maya/2011help/API/class_m_fn_typed_attribute.html)上面是我们的变形器初始化函数，我们在其中指定了变形器的所有属性。 要创建网格体属性，我们使用 MFnTypedAttribute 。 类型化属性用于创建非简单类型的大多数属性，如网格、曲面、曲线、数组等。 添加网格体属性后，我们将其设置为影响输出几何体属性 outputGeom。 所有变形器都有一个 outputGeom 属性，它是 MPxDeformerNode 类的一部分。 网格体属性完成后，我们创建混合权重属性，该属性与我们在依赖节点示例中添加的浮点属性相同。

[](http://download.autodesk.com/us/maya/2011help/Commands/makePaintable.html)initialize 函数中感兴趣的最后一个代码是 makePaintable 调用。 makePaintable 是一个 MEL（和 Python）命令，用于使特定属性可绘制。 所有变形器都带有每个顶点的权重属性，因此我们只需激活该属性的可绘制性即可。  初始化变形器后，我们可以继续使用变形函数。

```cpp
MStatus BlendNode::deform(MDataBlock& data, MItGeometry& itGeo,
                          const MMatrix &localToWorldMatrix,
                          unsigned int mIndex) {
  MStatus status;
 
  // Get the envelope and blend weight
  float env = data.inputValue(envelope).asFloat();
  float blendWeight = data.inputValue(aBlendWeight).asFloat();
  blendWeight *= env;
 
  // Get the blend mesh
  MObject oBlendMesh = data.inputValue(aBlendMesh).asMesh();
  if (oBlendMesh.isNull()) {
    // No blend mesh attached so exit node.
    return MS::kSuccess;
  }
 
  // Get the blend points
  MFnMesh fnBlendMesh(oBlendMesh, &status);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  MPointArray blendPoints;
  fnBlendMesh.getPoints(blendPoints);
 
  MPoint pt;
  float w = 0.0f;
  for (; !itGeo.isDone(); itGeo.next()) {
    // Get the input point
    pt = itGeo.position();
    // Get the painted weight value
    w = weightValue(data, mIndex, itGeo.index());
    // Perform the deformation
    pt = pt + (blendPoints[itGeo.index()] - pt) * blendWeight * w;
    // Set the new output point
    itGeo.setPosition(pt);
  }
 
  return MS::kSuccess;
}
```

变形函数是所有变形实现代码发生的地方。 该工作流程类似于普通依赖节点，其中我们：

1. 从数据块获取我们的输入
2. 执行变形
3. 将变形的几何体存储回数据块中。

[](http://download.autodesk.com/us/maya/2011help/API/class_m_fn_mesh.html)我们的变形函数首先从数据块中获取包络和混合权重输入值。 包络是一个内置的变形器属性，你可以将其用作变形的幅度乘数。 获取数值属性值后，我们得到混合目标网格体。 我们需要检查数据是否有效，因为如果没有目标网格体连接到变形器，则MObject将为空，我们无法执行变形。 一旦我们有了代表目标网格体的有效MObject，我们就需要提取其点位置。 我们通过将MFnMesh函数集附加到MObject来做到这一点。 MFnMesh 是用于查询、编辑和创建多边形网格的函数集。 现在我们有了所有输入，我们可以开始变形算法。

[](http://download.autodesk.com/us/maya/2011help/API/class_m_it_geometry.html)变形函数带有一个 MItGeometry 参数，用于迭代输入网格体的组件。 如果要利用变形器集成员身份，则必须使用此迭代器，因为它仅迭代变形器成员身份中包含的顶点或 cv。 您可以使用 MItGeometry：：index（） 查询当前顶点 ID。

[](http://download.autodesk.com/us/maya/2011help/API/class_m_px_deformer_node.html#2d4d2d66ff6da150f30d9438e2f36e24)当我们迭代每个顶点时，我们获取该顶点的绘制权重值。 MPxDeformerNode 有一个内置的便利函数 weightValue ，我们可以用它来查询每个绘制的权重值。 传递到此函数的 multiIndex 属性是输入几何的索引。 某些变形器可以同时影响多个网格体，每个网格体都有自己的绘制权重值贴图。 此索引指定要使用的索引。 大多数时候，这是 0。 正是出于这个原因，所有可绘制的属性都需要一个父复合数组属性，我们将在后面的章节中了解这一点。

有了权重值后，我们就可以进行实际变形，这是在一条线上。 混合形状变形是对当前顶点的简单加权矢量增量的添加。 计算出新的点位置后，我们将其放回几何迭代器中。 请注意，我们不必执行任何 setClean 调用。 除非我们向变形器添加任何自定义输出，否则当我们使用变形函数时，MPxDeformerNode会自动为我们处理。

您会注意到，在所有这些代码中，实际的变形算法只有一行。 这是在 Maya API 中制作插件时的常见情况。 大多数代码通常是所有节点设置、事件处理和清理。 想出算法几乎是容易的部分。

这是blendNode变形器的完整代码列表。 请注意，当我们向Maya注册节点时，我们还指定它是变形器节点。

```cpp
// BlendNode.h

#ifndef BLENDNODE_H
#define BLENDNODE_H
 
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MGlobal.h>
#include <maya/MItGeometry.h>
#include <maya/MMatrix.h>
#include <maya/MPointArray.h>
#include <maya/MStatus.h>
 
#include <maya/MFnMesh.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
 
#include <maya/MPxDeformerNode.h>
 
class BlendNode : public MPxDeformerNode {
 public:
  BlendNode() {};
  virtual MStatus deform(MDataBlock& data, MItGeometry& itGeo,
                         const MMatrix &localToWorldMatrix, unsigned int mIndex);
  static void* creator();
  static MStatus initialize();
 
  static MTypeId id;
  static MObject aBlendMesh;
  static MObject aBlendWeight;
};
#endif
```

```cpp
// BlendNode.cpp

#include "include/BlendNode.h"
#include <maya/MFnPlugin.h>
 
MTypeId BlendNode::id(0x00000002);
MObject BlendNode::aBlendMesh;
MObject BlendNode::aBlendWeight;
 
void* BlendNode::creator() { return new BlendNode; }
 
MStatus BlendNode::deform(MDataBlock& data, MItGeometry& itGeo,
                          const MMatrix &localToWorldMatrix, unsigned int mIndex) {
  MStatus status;
 
  // Get the envelope and blend weight
  float env = data.inputValue(envelope).asFloat();
  float blendWeight = data.inputValue(aBlendWeight).asFloat();
  blendWeight *= env;
 
  // Get the blend mesh
  MObject oBlendMesh = data.inputValue(aBlendMesh).asMesh();
  if (oBlendMesh.isNull()) {
    // No blend mesh attached so exit node.
    return MS::kSuccess;
  }
 
  // Get the blend points
  MFnMesh fnBlendMesh(oBlendMesh, &status);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  MPointArray blendPoints;
  fnBlendMesh.getPoints(blendPoints);
 
  MPoint pt;
  float w = 0.0f;
  for (; !itGeo.isDone(); itGeo.next()) {
    // Get the input point
    pt = itGeo.position();
    // Get the painted weight value
    w = weightValue(data, mIndex, itGeo.index());
    // Perform the deformation
    pt = pt + (blendPoints[itGeo.index()] - pt) * blendWeight * w;
    // Set the new output point
    itGeo.setPosition(pt);
  }
 
  return MS::kSuccess;
}
 
MStatus BlendNode::initialize() {
  MFnTypedAttribute tAttr;
  MFnNumericAttribute nAttr;
   
  aBlendMesh = tAttr.create("blendMesh", "blendMesh", MFnData::kMesh);
  addAttribute(aBlendMesh);
  attributeAffects(aBlendMesh, outputGeom);
  
  aBlendWeight = nAttr.create("blendWeight", "bw", MFnNumericData::kFloat);
  nAttr.setKeyable(true);
  addAttribute(aBlendWeight);
  attributeAffects(aBlendWeight, outputGeom);
 
  // Make the deformer weights paintable
  MGlobal::executeCommand("makePaintable -attrType multiFloat -sm deformer blendNode weights;");
 
  return MS::kSuccess;
}
 
MStatus initializePlugin(MObject obj) {
  MStatus status;
  MFnPlugin plugin(obj, "Chad Vernon", "1.0", "Any");
 
  // Specify we are making a deformer node
  status = plugin.registerNode("blendNode", BlendNode::id, BlendNode::creator,
                               BlendNode::initialize, MPxNode::kDeformerNode);
  CHECK_MSTATUS_AND_RETURN_IT(status);
 
  return status;
}
 
MStatus uninitializePlugin(MObject obj) {
  MStatus     status;
  MFnPlugin plugin(obj);
 
  status = plugin.deregisterNode(BlendNode::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);
 
  return status;
}
```

这是相应的 Python 实现：

```python
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import maya.cmds as cmds
 
class BlendNode(OpenMayaMPx.MPxDeformerNode):
    kPluginNodeId = OpenMaya.MTypeId(0x00000002)
     
    aBlendMesh = OpenMaya.MObject()
    aBlendWeight = OpenMaya.MObject()
     
    def __init__(self):
        OpenMayaMPx.MPxDeformerNode.__init__(self)
 
    def deform(self, data, itGeo, localToWorldMatrix, mIndex):
        envelope = OpenMayaMPx.cvar.MPxDeformerNode_envelope
        env = data.inputValue(envelope).asFloat()
        blendWeight = data.inputValue(BlendNode.aBlendWeight).asFloat()
        blendWeight *= env
 
        oBlendMesh = data.inputValue(BlendNode.aBlendMesh).asMesh()
        if oBlendMesh.isNull():
            return OpenMaya.MStatus.kSuccess
 
        fnBlendMesh = OpenMaya.MFnMesh(oBlendMesh)
        blendPoints = OpenMaya.MPointArray()
        fnBlendMesh.getPoints(blendPoints)
 
        while not itGeo.isDone():
            pt = itGeo.position()
            w = self.weightValue(data, mIndex, itGeo.index())
            pt = pt + (blendPoints[itGeo.index()] - pt) * blendWeight * w
            itGeo.setPosition(pt)
            itGeo.next()
 
        return OpenMaya.MStatus.kSuccess
 
def creator():
    return OpenMayaMPx.asMPxPtr(BlendNode())
 
def initialize():
    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()
     
    BlendNode.aBlendMesh = tAttr.create('blendMesh', 'bm', OpenMaya.MFnData.kMesh)
    BlendNode.addAttribute( BlendNode.aBlendMesh )
     
    outputGeom = OpenMayaMPx.cvar.MPxDeformerNode_outputGeom
    BlendNode.attributeAffects(BlendNode.aBlendMesh, outputGeom)
 
    BlendNode.aBlendWeight = nAttr.create('blendWeight', 'bw', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    BlendNode.addAttribute(BlendNode.aBlendWeight)
    BlendNode.attributeAffects(BlendNode.aBlendWeight, outputGeom)
 
    # Make deformer weights paintable
    cmds.makePaintable('blendNode', 'weights', attrType='multiFloat', shapeMode='deformer')
 
def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Chad Vernon', '1.0', 'Any')
    try:
        plugin.registerNode('blendNode', BlendNode.kPluginNodeId, creator, initialize, OpenMayaMPx.MPxNode.kDeformerNode)
    except:
        raise RuntimeError('Failed to register node')
 
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(BlendNode.kPluginNodeId)
    except:
        raise RuntimeError('Failed to deregister node')
```

除了语法之外，这里唯一的区别是对代理类 MPxDeformerNode 的内置静态变量 outputGeom 和 envelope 的访问。 我们不能只使用 self.outputGeom 或 self.envelope;相反，我们可以使用类似的代码：

```python
outputGeom = OpenMayaMPx.cvar.MPxDeformerNode_outputGeom
envelope = OpenMayaMPx.cvar.MPxDeformerNode_envelope
```

[](https://help.autodesk.com/view/MAYAUL/2020/ENU/?guid=Maya_SDK_MERGED_Maya_Python_API_html)可以在文档的Maya Python API部分中阅读有关脚本化插件工作流的更多信息。

### 获取输入几何体MObject

通常，当我们编写变形器时，我们希望访问输入的几何体MObject，以便获取顶点法线、uv等信息。在 MPxDeformerNode：:d eform 函数中，我们只能使用 MItGeometry 迭代器，它只为我们提供位置信息。我们可以从数据块中获取 MObject，但我们必须小心不要触发任何不必要的依赖关系图计算。

```cpp
MStatus SomeDeformer::deform( MDataBlock& data, MItGeometry& itGeo, const MMatrix &localToWorldMatrix, unsigned int geomIndex )
{
    MStatus status;
    MArrayDataHandle hInput = data.outputArrayValue(input, &status);
    CHECK_MSTATUS_AND_RETURN_IT( status )
    status = hInput.jumpToElement(geomIndex);
    CHECK_MSTATUS_AND_RETURN_IT(status)
    MObject oInputGeom = hInput.outputValue().child(inputGeom).asMesh();
    MFnMesh fnInputMesh(oInputGeom);
}
```

```python
def deform(self, data, itGeo, localToWorldMatrix, geomIndex ):
    inputAttribute = OpenMayaMPx.cvar.MPxDeformerNode_input
    inputGeom = OpenMayaMPx.cvar.MPxDeformerNode_inputGeom
    hInput = data.outputArrayValue(inputAttribute)
    hInput.jumpToElement(geomIndex)
    oInputGeom = hInput.outputValue().child(inputGeom).asMesh()
    fnInputMesh = OpenMaya.MFnMesh(oInputGeom)
```

在 MPxDeformerNode 中，计算方法已经为我们实现了。计算方法为我们获取输入的几何图形，创建几何交互器，并调用 deform 方法，这就是我们实现的。请注意，当我获取数据句柄时，我使用 outputArrayValue 和 outputValue。这可以防止Maya触发脏传播。如果我要使用 inputArrayValue 和 inputValue，Maya 将重新计算输入几何体，从而导致不必要的图形求值，因为这已经在计算方法中完成。

## 属性编辑器模板（Attribute Editor Templates）

通常，当我们创建节点时，我们希望自定义节点的属性编辑器显示，使其更加用户友好。我们通过属性编辑器模板来做到这一点。属性编辑器模板是描述节点的属性编辑器界面的 MEL 文件。默认情况下，Maya 将在属性编辑器中自动排列节点的属性。属性编辑器模板允许我们自定义此显示。要创建属性编辑器模板，请创建一个名为 AE{nodeName}Template.mel 的 MEL 文件，其中包含 AE{nodeName}Template 函数，并将该文件放入MAYA_SCRIPT_PATH中。AE{nodeName}Template 函数包含 editorTemplate 命令，这些命令指示属性编辑器如何更改节点中属性的默认布局。下面是具有 4 个属性的虚构节点的示例属性编辑器模板，其中一个是渐变属性。

```fallback
global proc AEsampleNodeTemplate( string $nodeName )
{
    editorTemplate -beginScrollLayout;
 
    editorTemplate -beginLayout "Sample Node Attributes" -collapse 0;
        editorTemplate -addControl "magnitude";
        editorTemplate -addControl "offset";
        editorTemplate -addControl "distance";
 
        AEaddRampControl ($nodeName + ".rampAttribute");
 
    editorTemplate -endLayout;
 
    AEdependNodeTemplate $nodeName;
 
    editorTemplate -addExtraControls;
    editorTemplate -endScrollLayout;
}
```

## MScriptUtil

[](http://download.autodesk.com/us/maya/2011help/API/class_m_script_util.html)MScriptUtil 是我们在将 Maya API 与 Python 一起使用时必须使用的繁琐类。由于Maya API被设计为C++库，因此它具有许多指针和引用，这些指针和引用被传递到各种函数中并从各种函数返回。由于Python没有指向简单类型的指针或引用，因此当我们在Maya API中遇到这些类型时，我们必须使用MScriptUtil。请注意，如果使用 Python API 2.0，则不必使用 MScriptUtil。该文档包含有关 MScriptUtil 的一般用法的有用信息，因此我不会在此处重现它。 我将展示各种代码示例，这些示例演示了如何在各种情况下使用 MScriptUtil，因为在撰写本文时，MScriptUtil 的代码示例非常有限。 幸运的是，我不需要经常使用 MScriptUtil，但当我遇到它时，我会在此页面上放置一个片段以建立有用的参考。

### 通过引用传递

#### 整数

```python
# MStatus MItMeshPolygon::setIndex(int index, int& prevIndex)
itPoly = OpenMaya.MItMeshPolygon(pathShape)
util = OpenMaya.MScriptUtil()
util.createFromInt(0)
pInt = util.asIntPtr()
itPoly.setIndex(faceId, pInt)
```

```python
# MStatus MImage::getDepthMapSize(unsigned int& width, unsigned int& height) const

utilWidth = OpenMaya.MScriptUtil()
utilWidth.createFromInt(0)
ptrWidth = utilWidth.asUintPtr()
utilHeight = OpenMaya.MScriptUtil()
utilHeight.createFromInt(0)
ptrHeight = utilHeight.asUintPtr()
mimage.getDepthMapSize(ptrWidth, ptrHeight)
width = OpenMaya.MScriptUtil.getUint(ptrWidth)
height = OpenMaya.MScriptUtil.getUint(ptrHeight)
```

#### 浮点2

```python
# MStatus MItMeshPolygon::getUVAtPoint(MPoint &pt, float2& uvPoint, MSpace::Space space=MSpace::kObject, const MString*uvSet=NULL)

util = OpenMaya.MScriptUtil()
util.createFromList([0.0, 0.0], 2)
uvPoint = util.asFloat2Ptr()
itPoly.getUVAtPoint(closestPoint, uvPoint, OpenMaya.MSpace.kWorld)
u = OpenMaya.MScriptUtil.getFloat2ArrayItem(uvPoint, 0, 0)
v = OpenMaya.MScriptUtil.getFloat2ArrayItem(uvPoint, 0, 1)
```

### 访问数组

```python
# MMatrix::operator[] (unsigned int row)

#Doesn't work!
matrix[3][1] = 2.2
 
# Do this instead
OpenMaya.MScriptUtil.setDoubleArray(matrix[3], 1, 2.2)
```

```python
# float* MImage::depthMap(MStatus* ReturnStatus=NULL) const

ptrDepthMap = mimage.depthMap()
OpenMaya.MScriptUtil.getFloatArrayItem(ptrDepthMap, index)
```

## MRamp属性

MRampAttribute 允许您创建可调整的曲线或颜色属性，用户可以在其中插入和调整沿渐变点的插值。

![](Notes/MAYA/Maya%20Python%20API/attachments/a7fd163269b52519db401f445031f6dd_MD5.jpg "rampDeformer")

为了创建斜坡属性，我们调用 MRampAttribute 中包含的方便类：

```cpp
MStatus RampAttributeDeformer::initialize() {
  // Create the curve ramp attribute
  aCurveRamp = MRampAttribute::createCurveRamp("curveRamp", "cur");
  addAttribute(aCurveRamp);
  attributeAffects(aCurveRamp, outputGeom);
 
  // Create the color ramp attribute
  aColorRamp = MRampAttribute::createColorRamp("colorRamp", "cor");
  addAttribute(aColorRamp);
  attributeAffects(aColorRamp, outputGeom);
  
  return MS::kSuccess;
}
```

要访问节点或变形器中的渐变属性值，请执行以下作：

```cpp
MStatus RampAttributeDeformer::deform(MDataBlock& data, 
                          MItGeometry& itGeo, 
                          const MMatrix &localToWorldMatrix, 
                          unsigned int geomIndex) {
  MStatus status;
 
  // Get the ramp attributes
  MObject oThis = thisMObject();
  MRampAttribute curveAttribute(oThis, aCurveRamp, &status);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  MRampAttribute colorAttribute(oThis, aColorRamp, &status);
  CHECK_MSTATUS_AND_RETURN_IT(status);
 
  float rampPosition = 0.25f, curveRampValue;
  MColor color;
 
  // Get the corresponding value on the curve ramp attribute
  curveAttribute.getValueAtPosition(rampPosition, curveRampValue, &status);
  CHECK_MSTATUS_AND_RETURN_IT(status);
 
  // Get the corresponding value on the color ramp attribute
  colorAttribute.getColorAtPosition(rampPosition, color, &status);
  CHECK_MSTATUS_AND_RETURN_IT(status);
 
  // Do your calculation with the values
 
  return MS::kSuccess;
}
```

您还需要确保在节点的属性编辑器模板中正确设置了属性：

```fallback
global proc AErampDeformerTemplate( string $nodeName )
{
    editorTemplate -beginScrollLayout;
 
        editorTemplate -beginLayout "Ramp Deformer Attributes" -collapse 0;
            AEaddRampControl( $nodeName + ".curveRamp" );
            AEaddRampControl( $nodeName + ".colorRamp" );
        editorTemplate -endLayout;
 
    editorTemplate -addExtraControls;
    editorTemplate -endScrollLayout;
}
```

## 其他资源

以下是学习 Maya API 的其他资源。

- Maya 文档（开发人员资源> API 指南）
- MayaInstallPath/devkit/plug-ins 中的 Maya DevKit 示例
- [](http://www.davidgould.com/Books/CMP1/)完整的 Maya 编程（第一卷），作者：David Gould
- [](http://nccastaff.bournemouth.ac.uk/jmacey/RobTheBloke/www/)罗伯特·贝特曼的笔记。
- [](http://ewertb.soundlinker.com/maya.php)布莱恩·尤尔特的笔记。
- [](http://www.comet-cartoons.com/3ddocs/mayaAPI/index.html)迈克尔·彗星的笔记。
- [](http://groups.google.com/group/python_inside_maya)python_inside_maya Google 电子邮件列表。
- [](http://forums.cgsociety.org/forumdisplay.php?f=89)CGTalk Maya 编程论坛。