---
date created: 2023-12-10 10:34
tags:
  - "#markdown"
  - "#obsidian"
---

# 链接
## 插入链接
- 语法
```md
[[笔记名称]]
[笔记别名](笔记路径)
```
- [Git入门](program/Git入门指南.md)
```md
# 适用于所有markdown编辑器
[Git入门指南](Notes/code/Git入门指南.md)
```
- [[program/Git入门指南]]
```md
# 仅适用于obsidian
[[Git入门指南]]
```

## 插入链接并启用链接别名
- 语法
```md
[[目标笔记路径|链接别名]]
[笔记别名](笔记路径)
```

- 我今天学习了有关于[[../math/2.0-向量(Vector)|向量]]的知识
```md
[[Notes/math/向量(Vector)|向量]]
```
- 我今天学习了关于[向量](../math/2.0-向量(Vector).md)的知识
```md
[向量](Notes/math/向量(Vector).md)
```
## 链接到其他笔记中的段落
- 语法
```md
[[目标笔记路径#笔记标题|链接别名]]
```
- 我今天学习了有关[[../math/2.0-向量(Vector)#向量的点积|向量点乘]]的知识
```md
[[Notes/math/向量(Vector)#向量的点积|向量点乘]]
```
- 我今天学习了有关[向量点乘](../math/2.0-向量(Vector).md#向量的点积)的知识
```md
[向量点乘](Notes/math/向量(Vector)#向量的点积)
```
## 链接到笔记中的某句话
我今天学习了[[program/Git入门指南#^ec11be]]
```md
[[Git入门指南^]]
```
## 嵌入其他笔记
- 语法
```md
![[笔记名称#标题]]
![[笔记名称^某句话]]
```
![[../program/Python/pip入门指南#maya安装pymel]]
![[../program/Python/pip入门指南#^c5dc9e]]
## 链接外部网站
- 语法
```md
[链接别名](链接地址)
```
[bilibili](https://www.bilibili.com/)
# 文字编辑
## 标题
	# heading1
	## heading2
	### heading3
	#### heading4
	##### heading5
	###### heading6 
## 高亮
==两个等号是高亮==
## 加粗
**双星号是加粗**
__双下划线是也加粗__
## 斜体
*单星号是斜体*
_单下划线也是斜体_
## 删除线
~~双波浪线是删除~~
## 列表
### 无序列表
- Item1 
- item2
- item3
	- item3-1
	- item3-2
### 有序列表
1. item1
2. item2
3. item3
	1. item3-1
	2. item3.2
### 待办
- [ ] task1
- [x] task2
- [ ] task3
	- [x] task3-1
	- [ ] task3-2
## 引用
> 真理是经得起经验的考验的。
> ——爱因斯坦
> > 或许他真的说过
> > 谁知道呢。
## 标注
> [!INFO] INFO
> 多喝白水

> [!TODO] TODO
> 多喝白水

> [!NOTE] NOTE
> 多喝白水

> [!BUG] BUG
> 多喝白水

> [!WARNING] WARNING
> 多喝白水

> [!Danger] Danger
> 多喝白水

> [! question]  question
> 多喝白水

> [! example]-  example
> - 多喝白水
> - 多吃蔬菜
## 注释
- 语法
```
正文^注释
```
1. 医之好治不病以为功[^01]
2. 天姥连天向天横，势拔五岳掩赤城。^[出自《梦游天姥吟留别》]
3. git的使用。^[[[program/Git入门指南]]]

[^01]:出自《扁鹊见蔡桓公》
# 插入图片
![[45dc3fe36651bc0b91d083a5340129eb_MD5.png]]
# 插入图表
| head1 | head2 | head3 |
| ------|-------|-------|
|asdasdas |asdadssaa|asdad|
|asdasd|asdasdas|asdasdsd|
|15|12|33|
# 插入代码
## 行内代码
`import os`
## 代码块
```python
import math
print(math.pi)
```