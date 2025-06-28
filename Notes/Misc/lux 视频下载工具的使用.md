#  安装scoop
[Scoop](https://scoop.sh/)是Windows下的一个包管理器。
1. 在 PowerShell 中输入下面内容，保证允许本地脚本的执行：
```
set-executionpolicy remotesigned -scope currentuser
```
2. 然后执行下面的命令安装 Scoop：
```
iex (new-object net.webclient).downloadstring('https://get.scoop.sh')
```
3. 静待脚本执行完成就可以了，安装成功后，让我们尝试一下：
```
scoop help
```
# 安装 lux
```
scoop install lux
```
# Usage:
- 语法：`lux [OPTIONS] URL [URL...]
1. 下载视频
```
lux "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

2. 该 -i 选项显示视频的所有可用质量，而无需下载。
```
lux -i "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```
4. 使用 `lux -f stream "URL" `下载在 -i 选项的输出中列出的特定流。
3. 使用 -p 选项可以下载整个播放列表，而不是单个视频。
```
lux -i -p "https://www.bilibili.com/bangumi/play/ep198061"
```