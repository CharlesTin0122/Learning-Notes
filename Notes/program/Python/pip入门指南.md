## pip安装模块,‘-m’以模块的形式运行pip模块

```
py -m pip <pip arguments>

py -m pip install SomePackage            # latest version
py -m pip install SomePackage==1.0.4     # specific version
py -m pip install 'SomePackage>=1.0.4'   # minimum version
```

## 国内源安装模块

阿里云 [http://mirrors.aliyun.com/pypi/simple/](http://mirrors.aliyun.com/pypi/simple/)  
腾讯云：[https://mirrors.cloud.tencent.com/pypi/simple](https://mirrors.cloud.tencent.com/pypi/simple)  
豆瓣(douban) [http://pypi.douban.com/simple/](http://pypi.douban.com/simple/) ^c5dc9e

中国科技大学 [https://pypi.mirrors.ustc.edu.cn/simple/](https://pypi.mirrors.ustc.edu.cn/simple/)  
清华大学 [https://pypi.tuna.tsinghua.edu.cn/simple/](https://pypi.tuna.tsinghua.edu.cn/simple/)  
中国科技大学 [https://pypi.mirrors.ustc.edu.cn/simple/](https://pypi.mirrors.ustc.edu.cn/simple/)  
华中理工大学：[http://pypi.hustunique.com/](http://pypi.hustunique.com/)  
山东理工大学：[http://pypi.sdutlinux.org/](http://pypi.sdutlinux.org/)
## 通过国内镜像安装库
```
mayapy -m pip install scipy -i https://mirrors.cloud.tencent.com/pypi/simple
```
## 查看pip安装列表
```
mayapy -m pip list
```
## 查看库信息
```

pip show flask
```
## 更新pip
```
mayapy -m pip install --upgrade pip
```
## 查看Python版本
```shell
python --version
```
## 更新python版本
```shell
pip install --upgrade python
```
## maya安装pymel
```
mayapy -m pip install pymel
```
## To install within your user space
```

mayapy -m pip install --user pymel
```
## pip设置代理
```

pip install requests --proxy=127.0.0.1:7890
```
## 创建名为venv311的虚拟环境
```

python -m venv venv311
```
## 调用activate.bat进入该虚拟环境
```

 activate venv311
```
## 调用deactivate.bat退出该虚拟环境,回到全局环境
```

deactivate
```
## unreal pip 安装PySide2
```

"F:\DGSHRes\Engine\Binaries\ThirdParty\Python3\Win64\python.exe" -m pip install PySide2
"F:\DGSHRes\Engine\Binaries\ThirdParty\Python3\Win64\python.exe" -m pip install mypy -i https://mirrors.cloud.tencent.com/pypi/simple
```