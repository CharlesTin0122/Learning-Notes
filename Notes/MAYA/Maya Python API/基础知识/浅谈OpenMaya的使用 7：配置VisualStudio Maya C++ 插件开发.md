本篇简单记录一下在VisualStudio中使用C++写Maya插件时，应该怎么配置VS。以及一个简单的Maya命令的开发框架是怎样的。

寻常的少量数据搜索、注册回调等功能通过使用Python版的OpenMaya即可实现目的。但是如果是需要写Deformer、Node这些需要快速实时计算的节点，就需要使用C++来编写了。

## 配置Visual Studio

1.创建空项目

![](attachments/cad6d16646eb7259c7e9699043f649a6_MD5.webp)

![](attachments/c1ef73d2a48537b6b92bd9d21a69da02_MD5.webp)

2.创建项目文件

![](attachments/afb378fe252dabe50968b288b024b5b3_MD5.png)

  

3.打开项目设置

![](attachments/e1776542cc613eead7899f1a1a8420e0_MD5.webp)

4.将exe换成.dll

![](attachments/16342be4da4472e0de9cb74e81e77692_MD5.webp)

5.修改扩展名为.mll

![](attachments/9e0377f0f763aa9fc9574ac708eadd6e_MD5.png)

6.添加包含路径

![](attachments/7c655b363d3865253cfb9fd050bc8b9b_MD5.webp)

7.添加静态库路径

![](attachments/0b3c2e60b456b2117ed272f60deeef1f_MD5.png)

之后点击应用，确定。

  

  

## 简单Maya命令框架

首先来到头文件，包含需要的头文件。

然后显示链接静态库。

最后定义一个命令类（名字可任意）。

![](attachments/d201a81fdf888e410756c6ef25c6380b_MD5.png)

  

来到cpp文件

![](attachments/9845c9e6b832d1d40c5cc4cd8260ef92_MD5.webp)

之后编译,然后打开目录文件夹，即可看到.mll文件。

![](attachments/bfde78abbaea92f2bc1c1e513b296ef9_MD5.png)

  

## 加载Maya插件

打开Maya的插件管理器

![](attachments/5b50f039710200e87faf79c50db63b9c_MD5.png)

资源管理器中指定.mll文件

![](attachments/d758e6b7e73dd95073d6cff122f44f6a_MD5.png)

![](attachments/65f1f9390b8d4025a6bacf5347a9c4ad_MD5.png)

加载成功后即可测试命令

![](attachments/663742eaf6e502863e3ece146da3bb33_MD5.png)

![](attachments/4eddb61173a4c6e315720340597504aa_MD5.webp)

mel和python都可以成功执行。