
# jason
```python
"""----------------------案例1--------------------"""

import json

"""
如果你要处理的是文件而不是字符串，你可以使用 json.dump() 和 json.load() 来编码和解码JSON数据
"""
data = {"abc": 123, "Path": r"D:\Work_MobilGame\Test", "123": 1.0}

#  写入
with open("testttttt.json", "w") as f:
    json.dump(data, f, indent=4, sort_key=True)  # indent=4 意为缩进空格数量,sort_key按字母顺序排序


#  读取
with open("test.json", "r") as f:
    data = json.load(f)
print(data)

"""-----------------------案例2---------------------"""

#  创建一一对应列表
attrList = [
    "translateX",
    "translateY",
    "translateZ",
    "rotateX",
    "rotateY",
    "rotateZ",
    "scaleX",
    "scaleY",
    "scaleZ",
]
attrVal = [1.046, 1.712, 3.438, -14.464, 15.652, 50.186, 1, 1, 1]
#  将两个列表压缩成一一对应的元组列表
zipList = zip(attrList, attrVal)
#  将一一对应的元组列表生成字典
data = dict(zipList)


#  设置保存路径和写入的变量
path = r"C:\Users\tianc\Documents\maya\2020\prefs\scripts\pSphere1.json"
jsonData = json.dumps(data)
# 写入
with open(path, "w") as f:
    f.write(jsonData)
#  读取
with open(path, "r") as f:
    sourceData = f.read()
# 编码为maya可用
targetData = json.JSONDecoder().decode(sourceData)
# 字典循环使用方法
for key, value in targetData.items():
    print(key, value)

    """
with open(mode: OpenTextMode = "r")
'r'	open for reading (default)
'w'	open for writing, truncating the file first
'x'	create a new file and open it for writing
'a'	open for writing, appending to the end of the file if it exists
'b'	binary mode
't'	text mode (default)
'+'	open a disk file for updating (reading and writing)
'U'	universal newline mode (deprecated)
    """
```
# sys
```python
import sys
print(sys.path)  # 检索python解释器的环境路径
print(sys.version)  # 检索python解释器的版本
print(sys.argv)  # 检索python文件的参数列表
print(sys.platform)  # 检索python解释器的平台
print(sys.maxsize)  # 检索python解释器的平台
print(sys.getdefaultencoding())  # 检索python默认编码
print(sys.getfilesystemencoding())  # 检索python文件系统默认编码
print(sys.getrecursionlimit())  # 获取python递归次数限制
print(sys.setrecursionlimit(1000))  # 设置python递归次数限制

sys.path.append(r'G:\Code\Python')
sys.exit(0)  # 退出状态码
```
# os
```python
import json
import os

# 系统相关内容
print(os.name)  # 系统名称
print(os.environ)  # 环境变量
print(os.sep)  # 获取当前平台分隔符 "\"
print(os.pathsep)  # 获取当前平台路径分隔符 ";"
print(os.getcwd())  # 获取文件所在目录
# 文件和目录操作
os.mkdir("test")  # 创建目录
os.rmdir("test")


def main():
    print(os.getcwd())  # 获取当前maya执行路径

    filePath1 = os.path.abspath('__file__')  # 当前脚本绝对路径（包含文件名）
    filePath2 = os.path.dirname(filePath1)  # 当前脚本所在的位置（不包含文件名）

    currentFilePath = rf'{os.path.dirname(__file__)}'  # 获取py文件当前路径
    json_file = os.path.join(currentFilePath, "data.json")  # 在py文件当前路径下创建json文件路径
    print(json_file)

    os.chdir(filePath2)  # 切换maya执行路径

    print(os.getcwd())
    with open("path.json", "r") as f:
        data = json.load(f)
    print(data)


file_path = r'D:\Backup\Documents\maya\2020\prefs\scripts\delete.txt'
# 删除文件
os.remove(file_path)
# 重命名文件
os.rename(file_path,
          r'D:\Backup\Documents\maya\2020\prefs\scripts\nodelete.txt')
# 分割文件的路径和文件名
os.path.split(file_path)
# 获取路径
os.path.dirname(file_path)
# 获取文件名
os.path.basename(file_path)
# 提取文件扩展名
os.path.splitext(file_path)
#  : 将path进行组合，若其中有绝对路径，则之前的path将被删除。
os.path.join(path1, path2)
# 打开路径
os.startfile(file_path)

filePath = os.path.abspath('__file__')
print(filePath)


# 通过os.path.walk递归遍历，可以访问子文件夹
def file_name_walk(file_dir):
    for parent, dirnames, filenames in os.walk(file_dir):
        # 显示所有子目录路径
        for dirname in dirnames:
            print(os.path.join(parent, dirname))
        # 显示目录下所有文件
        for filename in filenames:
            print(os.path.join(parent, filename))
```
# logging
```python
import logging


"""------------------------------------------------基础-----------------------------------------------------------"""
"""
默认日志级别是warning
使用baseConfig()来指定日志存储和日志输出级别,filemode参数中‘a’是追加模式（日志会向后追加），‘W’是写入模式（日志会被重写）。
"""
# logging.basicConfig(filename="demo.log", filemode="w", level=logging.INFO)
#
# logging.debug("this is a debug log")
# logging.info("this is an info log")
# logging.warning("this is a warning log")
# logging.error("this is an error log")
# logging.critical("this is a critical log")

# print("this is print log")

"""
输出格式和添加公共信息
%(asctime)s:显示log时间，%(levelname)-8s：显示log级别，-8：占8个字符，'-'为左对齐，
%(filename)s:显示文件名，%(lineno)s:显示行数，%(message)s:显示log信息，中间用|区隔
"""
# logging.basicConfig(format="%(asctime)s|%(levelname)-8s|%(filename)s:%(lineno)s|%(message)s", level=logging.DEBUG)
#
# logging.debug("this is a debug log")
# logging.warning("this is a warning log")


"""----------------------------------------------进阶------------------------------------------------------------"""
# 记录器 Logger，用于创建日志
logger = logging.getLogger("ccc.applog")  # 记录器，默认是‘root’
logger.setLevel(logging.DEBUG)  # 设置记录器log级别为debug
# 处理器 Handler，用于输出日志
consoleHandler = logging.StreamHandler()  # 流处理器handler
consoleHandler.setLevel(logging.DEBUG)  # 流处理器log级别为debug

fileHandler = logging.FileHandler(filename="addDemo.log")  # 文件处理器，没有指定日志级别，使用记录器的日志级别
fileHandler.setLevel(logging.INFO)  # 文件处理器log级别为info

"""记录器log级别设为最低，处理器分别设置log级别"""

# 格式 Formatter，用于输出的格式
formater = logging.Formatter("%(asctime)s|%(levelname)-8s|%(filename)s:%(lineno)s|%(message)s")  # 日志格式

# 给处理器设置格式
consoleHandler.setFormatter(formater)
fileHandler.setFormatter(formater)

# 给记录器设置处理器
logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)

# 过滤器 Filter
flt = logging.Filter("ccc")  # 定义过滤器为名称空间‘ccc’
logger.addFilter(flt)  # 记录器关联过滤器
fileHandler.addFilter(flt)  # 处理器关联过滤器

# 打印日志的代码
logger.debug("this is a debug log")
logger.info("this is a info log")
logger.warning("this is a warning log")
logger.error("this is a error log")
logger.critical("this is a critical log")
```