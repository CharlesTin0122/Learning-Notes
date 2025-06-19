---
date created: 2023-12-05 11:33
---

下面是Maya内UI常用的几个布局管理，通过这几个布局嵌套可以实现大部分UI上的开发需求

## columnLayout

此命令创建一个布局，该布局将其子元素安排在单个列中。

- 官方案例

  ```python
  cmds.window()
  cmds.columnLayout( columnAttach=('both', 5), rowSpacing=10, columnWidth=250)
  cmds.button()
  cmds.button()
  cmds.button()
  cmds.showWindow()
  ```

- 参考

  ![bb0948a67b77d6faa99a42fd1b719ba8_MD5](bb0948a67b77d6faa99a42fd1b719ba8_MD5.jpg)

## flowLayout

这个命令创建一个布局，它将其子元素排列在单行上(水平或垂直)。取决于-wrap布尔值(默认为false)，如果布局的父元素不能在一行中容纳所有的子元素，这些子元素要么换行，要么被截断。

- 案例

  ```python
  import maya.cmds as cmds

  cmds.window(title='小静的博客',w=300,h=100)
  cmds.flowLayout( columnSpacing=10, wrap=1)
  for i in range(10):
      cmds.button()
  cmds.showWindow()
  ```

- 参考

  ![e721943b53eb392c77b2888ec8e7f63f_MD5](e721943b53eb392c77b2888ec8e7f63f_MD5.gif)

## formLayout

此命令创建一个表单布局控件。 表单布局允许对其直接子控件进行绝对和相对定位。\
控件有四个边:上、左、下和右。 儿童只能被定位在两个方向上，左右和上下。 附加标志从指定要附加的边的参数(第二个参数)获得附件的方向。 子节点的任何或所有边都可以连接。 有六种方法可以附加它们:

- 官方案例

  ```python
  import maya.cmds as cmds

  window = cmds.window(title='小静的博客',w=300,h=100)
  form = cmds.formLayout(numberOfDivisions=100)
  b1 = cmds.button()
  b2 = cmds.button()
  column = cmds.columnLayout()
  cmds.button()
  cmds.button()
  cmds.button()

  cmds.formLayout( form, edit=True, attachForm=[(b1, 'top', 5), (b1, 'left', 5), (b2, 'left', 5), (b2, 'bottom', 5), (b2, 'right', 5), (column, 'top', 5), (column, 'right', 5) ], attachControl=[(b1, 'bottom', 5, b2), (column, 'bottom', 5, b2)], attachPosition=[(b1, 'right', 5, 75), (column, 'left', 0, 75)], attachNone=(b2, 'top') )

  cmds.showWindow( window )
  ```

- 参考

  ![298341cf1f8a1c408a5a78b20edaa2d6_MD5](298341cf1f8a1c408a5a78b20edaa2d6_MD5.jpg)

## frameLayout

这个命令创建帧布局控件。 框架布局可以围绕其子控件绘制边框，也可以显示标题。 框架布局也可以是可折叠的。 折叠一个框架布局将使子框架布局不可见，并缩小框架布局的大小。 然后可以扩展框架布局，使子框架可见。 请注意，框架布局可能只有一个子控件。 如果您希望在框架布局中有多个子布局，那么您必须使用其他控件布局作为框架布局的直接子布局。

- 案例

  ```python
  import maya.cmds as cmds

  cmds.window(title='小静的博客')
  cmds.frameLayout(l=u"按钮",cll=True,cl=1 )
  cmds.button()
  cmds.button()
  cmds.button()
  cmds.setParent( '..' )
  cmds.setParent( '..' )
  cmds.showWindow()
  ```

- 参考

  ![e2ad0a233cfd767c5c71e49d322b9da7_MD5](e2ad0a233cfd767c5c71e49d322b9da7_MD5.gif)

## gridLayout

此布局以网格的方式排列子元素，其中网格中的每个单元格大小相同。 您可以指定网格单元格的行数和列数以及宽度和高度。

- 官方案例

  ```python
  import maya.cmds as cmds

  cmds.window(title='小静的博客')
  cmds.gridLayout( numberOfColumns=2, cellWidthHeight=(100, 50) )
  cmds.button()
  cmds.button()
  cmds.button()
  cmds.button()
  cmds.button()
  cmds.button()
  cmds.button()
  cmds.showWindow()
  ```

- 参考

  ![c9911305b5792eae6502e37221dc6d78_MD5](c9911305b5792eae6502e37221dc6d78_MD5.jpg)

## rowLayout

此命令创建的布局能够将子元素定位到单个水平行中。

- 官方案例

  ```Python
  import maya.cmds as cmds

  cmds.window(title='小静的博客', widthHeight=(350, 150) )
  cmds.rowLayout( numberOfColumns=3, columnWidth3=(80, 75, 150), adjustableColumn=2, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)] )
  cmds.text()
  cmds.intField()
  cmds.intSlider()
  cmds.showWindow()
  ```

- 参考

  ![8a9c158d4fe638e4d34be9fe7865422a_MD5](8a9c158d4fe638e4d34be9fe7865422a_MD5.jpg)

## scrollLayout

此命令创建滚动布局。 当您有许多控件不能同时全部可见时，滚动布局非常有用。 该布局将显示一个水平和/或垂直滚动条时，以显示隐藏的控件。 由于滚动布局没有提供子控件的真正位置，所以应该使用另一个控件布局作为直接子控件。

- 官方案例

  ```Python
  import maya.cmds as cmds

  cmds.window(title='小静的博客', widthHeight=(350, 150) )
  scrollLayout = cmds.scrollLayout(
      horizontalScrollBarThickness=16,
      verticalScrollBarThickness=16)
  cmds.rowColumnLayout( numberOfColumns=3 )

  for index in range(10):
      cmds.text()
      cmds.intField()
      cmds.intSlider()

  cmds.showWindow()

  value = cmds.scrollLayout(scrollLayout, query=True, scrollAreaValue=True)
  top = value[0]
  left = value[1]
  ```

- 参考

  ![2e619e4b92dfad540f092353e996d625_MD5](2e619e4b92dfad540f092353e996d625_MD5.jpg)

  ## tabLayout

  此命令创建一个选项卡组。 选项卡组是控件布局的一种特殊形式，它只包含控件布局。 每当一个控件布局被添加到一个选项卡组时，它将有一个选项卡提供给它，允许从其他选项卡控件组中选择该组。 同一时间只能看到一个选项卡布局的一个子元素。

- 官方案例

  ```python
  import maya.cmds as cmds

  cmds.window(title='小静的博客', widthHeight=(200, 150) )
  form = cmds.formLayout()
  tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
  cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )

  child1 = cmds.rowColumnLayout(numberOfColumns=2)
  cmds.button()
  cmds.button()
  cmds.button()
  cmds.setParent( '..' )

  child2 = cmds.rowColumnLayout(numberOfColumns=2)
  cmds.button()
  cmds.button()
  cmds.button()
  cmds.setParent( '..' )

  cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'One'), (child2, 'Two')) )

  cmds.showWindow()
  ```

- 参考

  ![32eb234fbffce7e6826f0e99b6796435_MD5](32eb234fbffce7e6826f0e99b6796435_MD5.jpg)
