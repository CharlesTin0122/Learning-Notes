- pip安装模块,‘-m’以模块的形式运行pip模块

```
py -m pip <pip arguments>
py -m pip install SomePackage            # latest version
py -m pip install SomePackage==1.0.4     # specific version
py -m pip install 'SomePackage>=1.0.4'   # minimum version
```

- 国内源安装模块

pip国内的一些镜像

阿里云 [http://mirrors.aliyun.com/pypi/simple/](http://mirrors.aliyun.com/pypi/simple/)

腾讯云：[https://mirrors.cloud.tencent.com/pypi/simple](https://mirrors.cloud.tencent.com/pypi/simple)

豆瓣(douban) [http://pypi.douban.com/simple/](http://pypi.douban.com/simple/)

中国科技大学 [https://pypi.mirrors.ustc.edu.cn/simple/](https://pypi.mirrors.ustc.edu.cn/simple/)[](http://pypi.douban.com/simple/)

清华大学 [https://pypi.tuna.tsinghua.edu.cn/simple/](https://pypi.tuna.tsinghua.edu.cn/simple/)

中国科技大学 [https://pypi.mirrors.ustc.edu.cn/simple/](https://pypi.mirrors.ustc.edu.cn/simple/)

华中理工大学：[http://pypi.hustunique.com/](http://pypi.hustunique.com/)

山东理工大学：[http://pypi.sdutlinux.org/](http://pypi.sdutlinux.org/) 
- maya从国内镜像安装maya-stubs (maya指令存根) 
```
mayapy -m pip install maya-stubs -i https://mirrors.cloud.tencent.com/pypi/simple
```

- 查看pip安装列表

```
mayapy -m pip list
```

- 查看

```
pip show flask
```

- 更新pip

```
mayapy -m pip install --upgrade pip
```

- pip 切换路径

```
cd C:\Program Files\Autodesk\Maya2023\bin
```

- pip安装pymel

```
mayapy -m pip install pymel
```

- To install within your user space, run

```
mayapy -m pip install --user pymel
```

- pip 安装whl文件
```
pip install C:\Users\xxx\Downloads\pymel-1.4.0-py2.py3-none-any.whl
```
- 设置代理

```
pip install requests --proxy=127.0.0.1:7890
```

- 创建名为venv311的虚拟环境

```
python -m venv venv311
```

- 调用activate.bat进入该虚拟环境

```
venv311\scripts\activate
```

- 调用deactivate.bat退出该虚拟环境,回到全局环境

```
deactivate
```

- unreal pip

```python
"F:\DGSHRes\Engine\Binaries\ThirdParty\Python3\Win64\python.exe" -m pip install PySide2
```

```python
"F:\DGSHRes\Engine\Binaries\ThirdParty\Python3\Win64\python.exe" -m pip install mypy -i https://mirrors.cloud.tencent.com/pypi/simple
```

在maya编程中，Python语言可以用到哪些标准库和第三方库？

在Maya编程中，可以使用许多标准库和第三方库，包括但不限于以下几个：

1. 标准库

- os：用于访问操作系统功能

- sys：用于访问Python解释器相关的变量和函数

- re：用于正则表达式

- math：用于数学计算

- json：用于处理JSON数据

- logging：用于记录日志信息

1. 第三方库

- PySide/PyQt：用于创建图形用户界面

- requests：用于HTTP请求

- pillow：用于图像处理

- numpy：用于科学计算

- pandas：用于数据处理

- matplotlib：用于绘制图表

需要注意的是，Maya使用的是Python 2.7版本，因此在使用第三方库时需要确认其支持Python 2.7。此外，Maya还提供了一些专门针对Maya的Python模块，如maya.cmds和maya.api，用于访问Maya的API。

```
python -m pip install C:\Program Files\Autodesk\FBX\FBX Python SDK\2020.3.4\fbx-2020.3.4-cp310-none-win_amd64.whl
```