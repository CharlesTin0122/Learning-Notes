在上一篇中介绍了如何配置Visual Studio的Maya C++开发配置，然后又介绍了如何写一个最简单的无参命令。

这一篇将介绍如何写一个带参数的命令。最终效果如下：

[Decrypt929 播放 · 1 赞同视频![点击可播放视频](attachments/4ff5460ed8d569d7775e35d098cd7ed8_MD5.jpg)​](https://www.zhihu.com/zvideo/1622770246682378240)

  

## 1.加密解密函数

首先需要创建两个文件来写加密和解密功能。

![](attachments/96aebf4464daece6b46f9a75b81d1522_MD5.png)

在头文件中定义了一个加密类，然后声明了两个静态成员函数。

![](attachments/24e052049ae7bace73e96d62bdb767b3_MD5.webp)

在函数定义部分，加密函数通过打开一个已有的文件，然后读取获取其中的文本内容。加密的计算就只是简单的将字符码的值+3。

![](attachments/173fae50488dab582ccc7b407ff95a82_MD5.webp)

解密部分和加密部分类似，也是通过打开一个已有的文件，然后获取其中的文本内容。解密的计算是加密的逆向操作，所以将字符码的值-3。由于参数使用了一个函数指针，所以需要判断一下函数指针是否有效。

![](attachments/28bd3cc0680ec995914c3ec7f097c9da_MD5.png)

  

## 2.命令类

接着是定义Maya的命令类。

![](attachments/e2af5d2b73412b8b47554c25e394cda6_MD5.png)

与无参命令不同，有参命令需要添加参数和进行参数解析。

doIt()函数并不是真正执行命令的部分，而是参数解析和变量存储的部分。真正执行命令的是redoIt()。而在Maya中通过按G键可以重复执行命令，也是执行了redoIt()。

![](attachments/adde663552b34e7614adc665f9b7c30f_MD5.webp)

接着实现函数定义

先实现newSyntax()，该函数用来添加命令参数，因为之后要传递的参数是文件路径，所以这里使用字符串类型。

![](attachments/96a30ab069461631a30d5046f7fb4570_MD5.webp)

parseArgs()函数用来解析参数，通过判断参数flag然后后获取对应的参数。

![](attachments/d98904de30c6d152fde166a1f8dc464d_MD5.webp)

关于如何解析多个重名的flag，可以参考文档解释：

![](attachments/64f452250f9538a0bdfd1e33cefeafe8_MD5.png)

在doIt()函数中调用了parseArgs()函数来执行参数解析。

参数解析完成之后获取文件大小，然后解密文件。通过buffer来获取解密后的文本内容，通过lambda函数来打印未解密的文本内容。

参数解析、变量数据存储后完成后，执行redoIt()来真正执行命令。

![](attachments/1b1e7b924130dde6ca62d8f06d479440_MD5.png)

在redoIt()函数中，通过MGlobal::executePythonCommandStringResult()函数来执行字符串形式的Python命令。第二个参数是表示是否回显在ScriptEditor中。

![](attachments/365db2275bb9918e6861d9253305b17a_MD5.png)

之后的流程就和之前一样，不过在registerCommand()函数中，多了一个参数。

![](attachments/cb1c665763457b3f0b648bcea513e429_MD5.webp)

![](attachments/20b8da786a12e94569cd39e8235bf3f6_MD5.png)

编译之后就获得了一个mll的Maya插件。

  

测试插件：

这是一个简单的创建控制器层级和设置控制器颜色的Python脚本。

![](attachments/23866d1de30c4c7ddf2991202cedd4db_MD5.png)

通过简单的字符码值+3后，它长这样：

![](attachments/3e53e61f8ab64adb73085c6945758a2c_MD5.webp)

在Maya中加载插件会有如下提示：说明插件加载成功。

![](attachments/a0ba971ab0f1a87394beb8d89f88b247_MD5.webp)

此时执行该命令会直接报错。因为还没有执行Python脚本。

![](attachments/2928fc115acf82c4e75c75fc1139ecdb_MD5.webp)

先执行解密的命令：

正如之前写的那样，该命令将加密和解密的文本内容都打印了出来。

![](attachments/40f5166d87b4a3b7c21b2a4d0f28ddb0_MD5.webp)

![](attachments/10567a77cb15d7dd692e75a12d6f0337_MD5.png)

此时Python脚本已被执行，就可以执行刚才的控制器创建函数了：

![](attachments/f93ca9d2230f349cc94434ab67578693_MD5.webp)