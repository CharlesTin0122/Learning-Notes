---
date created: 2023-12-05 11:34
---

最近在研究用PyQt写Maya插件的界面，遇到不少的疑难杂症，在这里汇总一下，便于日后查询。

## 与Maya界面融合

首先最主要的目标是想让PyQt写好的界面与Maya完美融合，不会在操作Maya界面的时候把我们自己的窗口压到后面，而网上传统的方法便是使用`OpenMayaUI`库以及`shiboken2`库中的`wrapInstance`方法，将我们的窗口parent到已经存在的Maya窗口中。

官网的Maya开发人员帮助中也给了以下代码示例：

```python
from maya import OpenMayaUI as omui 

from PySide2.QtCore import * 
from PySide2.QtGui import * 
from PySide2.QtWidgets import *
from PySide2 import __version__
from shiboken2 import wrapInstance 

mayaMainWindowPtr = omui.MQtUtil.mainWindow() 
mayaMainWindow= wrapInstance(long(mayaMainWindowPtr), QWidget) 

# WORKS: Widget is fine 
hello = QLabel("Hello, World", parent=mayaMainWindow) 
hello.setObjectName('MyLabel') 
hello.setWindowFlags(Qt.Window) # Make this widget a standalone window even though it is parented 
hello.show() 
hello = None # the "hello" widget is parented, so it will not be destroyed. 

# BROKEN: Widget is destroyed 
hello = QLabel("Hello, World", parent=None) 
hello.setObjectName('MyLabel') 
hello.show() 
hello = None # the "hello" widget is not parented, so it will be destroyed.
```

> 代码中对比了`parent = mayaMainWindow`和`parent = None`两种情况，后者在使用show()方法后窗口会由于Python的GC机制在创建后瞬间消失，但前者由于parent到了Maya的主窗口中，就会由Maya来维持其生命周期。另外，此时在操作Maya界面的时候，我们的窗口也会一直保持置顶不会被挡住。

## Dock窗口

为了让我们的窗口能够dock在Maya的UI中，网上常见的方法是结合上面的`wrapInstance`方法，再通过内置库的`cmds.workspaceControl`来实现。（_注：Maya2017之前的版本为_ `cmds.dockControl`）

详情可参考**Dhruv Govil**大神的Python For Maya: Artist Friendly Programming教程中的Lighting Manager案例。

虽然该方法可行，但需要写多行代码才能实现dock的逻辑，比较麻烦，于是我又去调研了其他方案。

后来发现Maya提供了`maya.app.general.mayaMixin`模块，其中包含的类可以方便将基于PyQt创建的控件融合进Maya UI中，其中用于dock窗口的就是`MayaQWidgetDockableMixin`类。

官方示例：

```python
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide.QtGui import QPushButton, QSizePolicy

class MyDockableButton(MayaQWidgetDockableMixin, QPushButton):
    def __init__(self, parent=None):
        super(MyDockableButton, self).__init__(parent=parent)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred )
        self.setText('Push Me')

# Create an instance of the button and display it.
button = MyDockableButton()
# Show the button as a non-dockable floating window.
button.show(dockable=False)
# A valid Maya control name has been automatically assigned to the button.
buttonName = button.objectName()
print('# ' + buttonName)
# MyDockableButton_368fe1d8-5bc3-4942-a1bf-597d1b5d3b83

# showRepr() can be used to display the current dockable settings.
print('# ' + button.showRepr())
# show(dockable=False, height=23, width=70, y=610, x=197, floating=True)

# Change it to a dockable floating window.
button.show(dockable=True)
print('# ' + button.showRepr())
# show(dockable=True, area='none', height=23, width=70, y=610, x=197, floating=True)
```

- 在继承了`MayaQWidgetBaseMixin`类后，如果没有明确指定parent，则可以直接将我们的控件parent到main Maya window，无需再用`wrapInstance`方法，非常方便。
- 另外要注意`MayaQWidgetBaseMixin`应作为第一继承，否则在使用`show(dockable=True)`语句时会报错。
- 继承该类后，PyQt的`setWindowIcon`方法会失效，窗口无法自定义图标。

## 保持窗口唯一

当我们用上述方法写完窗口后，会发现重复执行`show`方法时，会弹出多个窗口，这个原因就是我们每实例化一次，Maya都会自动给我们的窗口起一个独一无二的Object Name，如上面案例中的`MyDockableButton_368fe1d8-5bc3-4942-a1bf-597d1b5d3b83`。

解决该问题的方法也很简单，可以手动用`setObjectName`方法给我们的窗口命名，避免可以同时实例化多个窗口。当然我们在后续重复执行代码的时候，Maya会因为重名问题报错：_Object's name is not unique_，所以应该在实例化之前先用`cmds.deleteUI`删除已存在的窗口。

**至此，我们得到了一个很简单的方式来写Maya Dockable Window**：

```python
class MyDockableWindow(MayaQWidgetDockableMixin, QtWidgets.QWidget):

    def __init__(self):
        super(MyDockableWindow, self).__init__()

        # Delete existing UI
        try:
            cmds.deleteUI('MDWWorkspaceControl')
        except RuntimeError:
            pass

        self.setWindowTitle('My Dockable Window')
        self.resize(500, 400)
        self.setObjectName('MDW')
        self.show(dockable=True)

MyWin = MyDockableWindow()
```

## 界面尺寸问题

由于我写的界面宽高并不是Fixed，而是允许用户随意缩放窗口，但我又希望每次用户打开界面的时候能复原我的初始布局，于是我在`__init__`时用了`resize`方法来确保界面大小固定。

而当继承了`MayaQWidgetDockableMixin`后，我发现我的界面经过用户手动大小调整后每次关闭再打开，Maya始终记得界面关闭前的大小，`resize`方法失效了。

经过研究，我发现Maya会将每个界面布局（Workspace）存储在一个对应的JSON文件中，其中记录着各个控件（如Outliner、ToolBox、ArnoldRenderView）的布局信息，所以在每次打开某一个控件的时候，Maya都会记得它上次关闭前的一些属性，包括窗口大小。

这个JSON文件位于`C:\Users\<用户名>\Documents\maya\<版本>\prefs\workspaces`文件夹中，内容参考如下：

```json
"closedControls": [
    {
        "objectName": "UVToolkitDockControl",
        "posX": 1901,
        "posY": 697,
        "controlHeight": 930,
        "controlWidth": 315,
        "widthProperty": "preferred",
        "heightProperty": "free"
    },
    {
        "objectName": "hyperShadePanel1Window",
        "posX": 2610,
        "posY": 333,
        "controlHeight": 870,
        "controlWidth": 1365,
        "widthProperty": "free",
        "heightProperty": "free"
    },
    {
        "objectName": "ArnoldRenderView",
        "posX": 765,
        "posY": 758,
        "controlHeight": 750,
        "controlWidth": 1450,
        "widthProperty": "free",
        "heightProperty": "free"
    },
]
```

- closedControls是没有dock在Maya界面中，已经被关闭的Workspace Control，如果我们的窗口在关闭Maya时没有dock，则可以在这里面找到。
- 其中controlHeight以及controlWidth就记录了这个窗口的宽高属性，会在下次打开时调用。
- 在关闭软件时，Maya会自动调用`saveShelf`命令来记录界面布局信息，该JSON文件也会被重写。

## 保存Dock窗口

如果我们在关闭Maya时，我们的窗口已经dock在了Maya界面布局上，会发现下次启动Maya后窗口消失。

如果想要创建一个能够跨会话永久保持的窗口，则可以参考**Kaine van Gemert**大神的方法，代价就是比较复杂。

原文链接：

[Qt for Maya: Dockable Windows​kainev.com/qt-for-maya-dockable-windows/](https://link.zhihu.com/?target=https%3A//kainev.com/qt-for-maya-dockable-windows/)

**注：以上这种方法经我测试，确实能够达到改写JSON文件来保存dock窗口的效果，但在关闭前将窗口dock后重启Maya，会发现软件一直崩溃打不开，而不dock则没有问题，暂时不清楚原因和解决方案。**

## 撤销多步操作

在测试我的界面功能时，会发现当我点击了一个按钮，执行了一个操作后，需要undo很多次才能够撤回这步操作，前几次的undo都没有任何反应，十分奇怪。

究其原因，是因为我的按钮对应着一个槽函数，而这个函数中包含着很多个command命令，而Maya的撤销机制是一次只能撤销一句command命令，所以当执行完一个函数后进行撤销，很可能前几次undo操作都不会有任何反应。

如果希望实现一步撤销，则需要把多个command包裹进一个块（chunk），使用Maya的`undoInfo`命令。

```python
cmds.undoInfo(openChunk=True)

# YOUR CODE

cmds.undoInfo(closeChunk=True)
```

如此一来，就可以把多个命令一次性撤销了。

## 显示错误提示信息

在编写一些功能时，时常会用到`Raise RuntimeError`来提示错误信息。但结合PyQt使用时，Maya的Command Line却不再显示标红的错误信息，取而代之的是Script Editor中返回的多行错误信息的Traceback。

案例如下：

```python
# Traceback (most recent call last):
#   File "<file path>", line 1, in <method>
#     raise RuntimeError('My custom error message.')
# RuntimeError: My custom error message.
```

而这样的话如果不打开Script Editor，用户在操作出错时就无法收到反馈，难以判断问题出在哪里。这个Traceback其实就是Python在运行遇到异常时返回的信息，可以通过`sys`库的`tracebacklimit`方法来消除。

```python
import sys
sys.tracebacklimit = 0
```

> 给`tracebacklimit`赋值一个整数，代表最多能向上回溯几条错误来源，0代表不回溯。

不过即使消除了Traceback，在遭遇异常时Script Editor也仍会打印`# RuntimeError: My custom error message.`这条信息，且无法在Command Line中显示，于是我找到了替代方案，就是利用`OpenMaya`库的`MGlobal.displayError`方法。

另外还有`displayInfo`和`displayWarning`方法来显示普通和警告信息。

```python
import maya.OpenMaya as om

om.MGlobal.displayError('Error Message')
om.MGlobal.displayWarning('Warning Message')
om.MGlobal.displayInfo('Info Message')
```

通过该方法，就能在不抛出异常的情况下直接在Command Line中向用户展现提示信息。需要注意的是，上述语句只能打印提示信息，并不会中断脚本的运行，继续执行仍会遭遇异常并覆盖掉我们设定的提示信息，所以最好直接在`displayError`后面接上`return`执行返回。
