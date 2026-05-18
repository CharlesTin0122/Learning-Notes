## 插件说明

通过安装该插件后，可以直接在[VS Code](https://zhida.zhihu.com/search?content_id=183801776&content_type=Article&match_order=1&q=VS+Code&zhida_source=entity)里使用P4的相关功能，提升工作效率。

大部分通过[Perforce](https://zhida.zhihu.com/search?content_id=183801776&content_type=Article&match_order=1&q=Perforce&zhida_source=entity) clone下来的项目，项目里的代码文件都是只读的，要修改代码需要先在[P4客户端](https://zhida.zhihu.com/search?content_id=183801776&content_type=Article&match_order=1&q=P4%E5%AE%A2%E6%88%B7%E7%AB%AF&zhida_source=entity)里找到该文件，再手动CheckOut，然后才能回到IDE里修改代码，步骤繁琐。安装Perforce插件后，就可以直接保存代码文件，同时会被自动CheckOut。

## 前提条件

需要安装好P4客户端，P4客户端完成配置，并且已下好相关项目。

## 下载插件

在VSCode里下载P4 插件，如下图所示

按Ctrl+Shift+X或者直接点击插件图标，输入“Perforce”找到Perforce for VS Code（简介下面是2020 Fork的那个），点击安装。

![](https://pica.zhimg.com/v2-6f2781698161caee61f56b332d6d7efc_1440w.jpg)

  

## P4插件配置

**注意需要在VSCode里先加载项目代码后才可以进行该插件的配置，否则没有"[Workspace](https://zhida.zhihu.com/search?content_id=183801776&content_type=Article&match_order=1&q=Workspace&zhida_source=entity)"标签页**

如下图所示，依次点击“图标”->“Settings”->“Workspace”-> "[Extensions](https://zhida.zhihu.com/search?content_id=183801776&content_type=Article&match_order=1&q=Extensions&zhida_source=entity)" ->“Perforce”即可进入Perforce插件配置设置。

![](https://pic2.zhimg.com/v2-639f0a43632f24dec0eb7590d5e9d729_1440w.jpg)

  

- **配置Client**

如下图所示，Perforce插件配置里的Client对应了P4的Workspace

![](https://pica.zhimg.com/v2-69422617402d1fac62e500bf9c75778a_1440w.jpg)

- **配置Dir**

dir的值为代码所在文件夹的路径，注意不是项目的路径（比如项目在D:\YourProject，代码在D:\YourProject\Script，那么该值为D:\YourProject\Script，而不是D:\YourProject）。

![](https://pica.zhimg.com/v2-00abf9652ddda71f195e478260034168_1440w.jpg)

- **配置Password**

密码为登录P4客户端所使用的的密码

![](https://pic1.zhimg.com/v2-ea23f7bbb2b333d83a8126278f20814e_1440w.jpg)

- **配置Port**

如下图所示，Perforce插件配置里的Port对应了P4的Server

![](https://pic2.zhimg.com/v2-a1eb59f4b857e9e4df77d0b24fe224d7_1440w.jpg)

- **配置User**

如下图所示，Perforce插件的User对应了P4的User

![](https://pic3.zhimg.com/v2-a1859f9fa812779f77a195cd4c48b00a_1440w.jpg)

至此Perforce插件配置完成。

## 其他

- **Perforce插件功能使用**

理论上配置了P4插件，直接在VS Code能操作P4客户端的大部分常用功能，只是个人不习惯在VS Code里直接操作P4，一般只用来CheckOut文件。看个人喜好吧。通用功能按Ctrl+P，输入“>perforce”可以查看和使用（如下图所示）。

![](https://pic4.zhimg.com/v2-a50f8ace058897812f3c130cbe162943_1440w.jpg)

- **注意点1**

该配置是跟项目相关的。因为每个项目的Dir、Client、Port、User都不同，所以如果有新的项目，需要根据以上方法再配置一遍。