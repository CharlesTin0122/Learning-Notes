# Maya：第六周 作业

![](attachments/Maya：第六周%20作业_image_0.png)

[單壹崽崽](https://www.jianshu.com/u/92cf571d45d7)

关注

2020.01.07 22:43:44字数 948阅读 1,089

lesson15_走进 PyMEL 编程

![](attachments/Maya：第六周%20作业_image_1.png)

image.png

![](attachments/Maya：第六周%20作业_image_2.png)

image.png

```python
def create_material(material_type='lambert', material_name='', assigned_obj=''):
    shader_node = pm.shadingNode('lambert', name="{}_{}".format(material_name, material_type), asShader=True)
    shader_sg = pm.sets(name='{}_SG'.format(shader_node.name()), empty=True, renderable=True, noSurfaceShader=True)
    shader_node.outColor >> shader_sg.surfaceShader
    if assigned_obj:
        shader_node.rename("{}_{}_{}".format(assigned_obj, material_name, material_type))
        shader_sg.rename(name='{}_SG'.format(shader_node.name()))
        assigned_obj = pm.PyNode(assigned_obj)
        pm.sets(shader_sg, forceElement=assigned_obj)
    return [shader_node, shader_sg]
sel_obj = pm.selected(tr=True)[0]
blend_color_node = pm.createNode('blendColors')
color_list = [(1, 0, 0), (0, 1, 0)]
for index, color in enumerate(color_list):
    lambert_shader = create_material(material_type='lambert',
                                     material_name='color',
                                     assigned_obj='')
    lambert_shader[0].color.set(color)
    lambert_shader[0].outColor >> '{}.color{}'.format(blend_color_node, index + 1)
obj_shader = create_material(material_type='lambert',
                             material_name='color',
                             assigned_obj=sel_obj)
blend_color_node.output.connect(obj_shader[0].color, f=True)
```

lesson16_为 Maya 安装第三方 Python 包

![](attachments/Maya：第六周%20作业_image_3.png)

image.png

给Maya 安装pip

1. 下载get-pip.py文件到本地盘符

![](attachments/Maya：第六周%20作业_image_4.png)

image.png

2.管理员模式打开系统cmd

3.找到maya安装目录下的mayapy.exe文件，拖到cmd中，把get-pip.py 拖到cmd中

```css
C:\Program Files\Autodesk\Maya2019\bin\mayapy.exe" E:\get-pip.py
```

![](attachments/Maya：第六周%20作业_image_5.png)

image.png

4.回车安装成功：C:\Program Files\Autodesk\Maya2019\Python\Lib\site-packages

![](attachments/Maya：第六周%20作业_image_6.png)

image.png

![](attachments/Maya：第六周%20作业_image_7.png)

image.png

安装yaml：

1.管理员模式打开系统cmd

2.输入以下代码

```css
C:\Program Files\Autodesk\Maya2019\bin\mayapy.exe" -m pip install pyyaml
```

![](attachments/Maya：第六周%20作业_image_8.png)

image.png

![](attachments/Maya：第六周%20作业_image_9.png)

image.png

![](attachments/Maya：第六周%20作业_image_10.png)

image.png

编译安装：

安装numpy：

如果用pip安装maya的numpy的话，可以成功安装，但没法正常导入所以需要用编译的方法来安装numpy

删除错误安装的numpy

![](attachments/Maya：第六周%20作业_image_11.png)

image.png

所以先要找到numpy的源码：以maya2019.2为例

可以goole下：下载numpy的源码

[https://github.com/numpy/numpy/releases](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fnumpy%2Fnumpy%2Freleases)

![](attachments/Maya：第六周%20作业_image_12.png)

image.png

我这里用的是maya2019 所以要下载2019的Visual Studio 2015 Update 3 并且安装

![](attachments/Maya：第六周%20作业_image_13.png)

image.png

下载maya2019的devkit

![](attachments/Maya：第六周%20作业_image_14.png)

image.png

![](attachments/Maya：第六周%20作业_image_15.png)

image.png

解压devkit的文件到maya安装目录下

![](attachments/Maya：第六周%20作业_image_16.png)

image.png

首次安装VS2015后，需要打开

![](attachments/Maya：第六周%20作业_image_17.png)

image.png

选择C++ 更新window SDK 和VC插件

![](attachments/Maya：第六周%20作业_image_18.png)

image.png

以下是我更新完的

![](attachments/Maya：第六周%20作业_image_19.png)

image.png

用管理员模式打开vs2015 cmd

![](attachments/Maya：第六周%20作业_image_20.png)

image.png

首先进入numpy所在的盘符：

```
E:
```

![](attachments/Maya：第六周%20作业_image_21.png)

image.png

然后输入具体位置

```css
cd E:\numpy-1.18.1\numpy-1.18.1
```

![](attachments/Maya：第六周%20作业_image_22.png)

image.png

把maya安装目录下的mayapy.exe拖到vs命令行中加上setup.py build_ext -I 再把 安装目录下的python2.7文件夹拖进去加上 -L 再把lib文件夹拖进去 以下是完整代码

```bash
"C:\Program Files\Autodesk\Maya2019\bin\mayapy.exe" setup.py build_ext -I "C:\Program Files\Autodesk\Maya2019\include\python2.7" -L "C:\Program Files\Autodesk\Maya2019\lib"
```

可以看到1.81的numpy不支持2.7的python

![](attachments/Maya：第六周%20作业_image_23.png)

image.png

所以重新下载 可以看到发布包中1.16.5的版本是最后支持2.7python 的

![](attachments/Maya：第六周%20作业_image_24.png)

image.png

在正常安装前先给maya安装cpython：

方法和安装numpy一样

下载cpython源码到本地：

[https://pypi.org/project/Cython/#files](https://links.jianshu.com/go?to=https%3A%2F%2Fpypi.org%2Fproject%2FCython%2F%23files)

![](attachments/Maya：第六周%20作业_image_25.png)

image.png

安装cpython：

![](attachments/Maya：第六周%20作业_image_26.png)

image.png

然后build install

```css
"C:\Program Files\Autodesk\Maya2019\bin\mayapy.exe" setup.py build install  
```

![](attachments/Maya：第六周%20作业_image_27.png)

image.png

看到这个就说明安装成功了

![](attachments/Maya：第六周%20作业_image_28.png)

image.png

接下来就可以安装对应版本的numpy源码了：

![](attachments/Maya：第六周%20作业_image_29.png)

image.png

![](attachments/Maya：第六周%20作业_image_30.png)

image.png

![](attachments/Maya：第六周%20作业_image_31.png)

image.png

编译安装总结：

1.对应的VS版本（安装C++完整插件）

2.maya端：安装get-pip.py

3.安装maya对应版本的devkit

4.给Maya编译安装cpython

源码下载：

[https://pypi.org/](https://links.jianshu.com/go?to=https%3A%2F%2Fpypi.org%2F)

Maya2017 编译器

[https://around-the-corner.typepad.com/adn/2016/08/compiler-versions-for-maya-2017.html](https://links.jianshu.com/go?to=https%3A%2F%2Faround-the-corner.typepad.com%2Fadn%2F2016%2F08%2Fcompiler-versions-for-maya-2017.html)

Maya2018 编译器

[https://around-the-corner.typepad.com/adn/2018/02/compiler-versions-for-maya-2018.html](https://links.jianshu.com/go?to=https%3A%2F%2Faround-the-corner.typepad.com%2Fadn%2F2018%2F02%2Fcompiler-versions-for-maya-2018.html)

Maya2019 编译器

[https://around-the-corner.typepad.com/adn/2019/01/maya-2019-api-updates-guide.html](https://links.jianshu.com/go?to=https%3A%2F%2Faround-the-corner.typepad.com%2Fadn%2F2019%2F01%2Fmaya-2019-api-updates-guide.html)

Maya2020 编译器

[https://around-the-corner.typepad.com/adn/2019/12/maya-2020-api-update-guide.html](https://links.jianshu.com/go?to=https%3A%2F%2Faround-the-corner.typepad.com%2Fadn%2F2019%2F12%2Fmaya-2020-api-update-guide.html)

Maya2022 编译器

[https://around-the-corner.typepad.com/adn/2021/03/maya-2022-api-updates.html](https://links.jianshu.com/go?to=https%3A%2F%2Faround-the-corner.typepad.com%2Fadn%2F2021%2F03%2Fmaya-2022-api-updates.html)

软件下载：maya2019

[https://blog.csdn.net/luckypeng/article/details/54342659](https://links.jianshu.com/go?to=https%3A%2F%2Fblog.csdn.net%2Fluckypeng%2Farticle%2Fdetails%2F54342659)

Maya Devkit 下载：

[https://www.autodesk.com/developer-network/platform-technologies/maya](https://links.jianshu.com/go?to=https%3A%2F%2Fwww.autodesk.com%2Fdeveloper-network%2Fplatform-technologies%2Fmaya)

lesson17_自定义 Maya 环境变量

![](attachments/Maya：第六周%20作业_image_32.png)

image.png

![](attachments/Maya：第六周%20作业_image_33.png)

image.png

环境变量导出yaml文件模板：

```python
import os
import yaml
# Maya Default Environment
default_env = os.environ.copy()
custom_env = default_env
plug_in_paths = []
module_paths = []
script_paths = []
xbm_paths = []
shelf_paths = []
python_paths = []
custom_env_data = [('MAYA_PLUG_IN_PATH', plug_in_paths),
                   ('MAYA_MODULE_PATH', module_paths),
                   ('MAYA_SHELF_PATH', shelf_paths),
                   ('MAYA_SCRIPT_PATH', script_paths),
                   ('XBMLANGPATH', xbm_paths),
                   ('PYTHONPATH', python_paths)]
for item, value in custom_env_data:
    custom_env[item] = "{};{}".format(';'.join(value), os.getenv(item))
# Save Yaml File
maya_env_config = r'F:\Python\Python3_Learning\Maya_2019.yml'
with open(maya_env_config, 'w') as f:
    yaml.dump(custom_env, f)
```

导入yaml 模板： 由于启动这个py文件的不是mayapy，所以我这用的是Python3.81的编译器

```python
import yaml
import subprocess
from pathlib import Path
# Python 3.81
maya_env_config = r'F:\Python\Python3_Learning\Maya_2019.yml'
with open(maya_env_config, 'r') as f:
    my_nev = yaml.safe_load(f)
maya_exe_path = Path(my_nev['MAYA_LOCATION']) / r'bin\maya.exe'
subprocess.Popen(maya_exe_path, env=my_nev)
```

vbs方法：效果和bat一样，但是不会弹cmd窗口

```
Dim objws 
Set objws=WScript.CreateObject("wscript.shell") 
objws.Run "pythonw.exe F:\Python\Python3_Learning\Maya_2020_Env.py ",,True
```

bat文件: 没有自动关闭cmd窗口！！！

```bash
@echo off 
start pythonw F:\Python\Python3_Learning\Maya_2019_Env.py 
cmd/k
```

Yaml文件检查

[http://www.yamllint.com/](https://links.jianshu.com/go?to=http%3A%2F%2Fwww.yamllint.com%2F)

Maya环境变量参考

[https://knowledge.autodesk.com/zh-hans/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2018/CHS/Maya-EnvVar/files/GUID-925EB3B5-1839-45ED-AA2E-3184E3A45AC7-htm.html](https://links.jianshu.com/go?to=https%3A%2F%2Fknowledge.autodesk.com%2Fzh-hans%2Fsupport%2Fmaya%2Flearn-explore%2Fcaas%2FCloudHelp%2Fcloudhelp%2F2018%2FCHS%2FMaya-EnvVar%2Ffiles%2FGUID-925EB3B5-1839-45ED-AA2E-3184E3A45AC7-htm.html)

1人点赞

[TD Maya API Learning](https://www.jianshu.com/nb/41202645)