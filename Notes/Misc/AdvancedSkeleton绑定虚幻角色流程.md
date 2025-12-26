# 骨骼模型导入maya
- 场景设为Y轴向上，然后导入模型
![|424x478](attachments/f2954a7bab47190341f0e50744ec408d_MD5.jpg)
# 移除空间名称
- 会发现我们的骨骼名称可能带有名称空间，要去掉名称空间
![](attachments/348f0c7dc38ff6758ae4263e8a6f2448_MD5.jpg)
- 打开空间名称编辑器
![](attachments/cffad5c5bd77392558fd7eced54fef65_MD5.jpg)
- 删除空间名称
![](attachments/f8568fb276d3322c5a55f984d68d7b28_MD5.jpg)
- 在弹出窗口选择合并到根
![](attachments/0d5ce671e02c149c33171503160f90bc_MD5.jpg)
# 绑定
- 使用advanced skeleton插件的NameMatcher工具进行绑定
![](attachments/72d07365c90db6c32fec199fc7a7b306_MD5.jpg)
- 模板选择Unreal 5
![](attachments/3790758d9c9509c3e4d2f15374308734_MD5.jpg)
- 点击下面的check按钮，会弹出提示，所有提示一律点击OK。
![](attachments/61fe5e7b6bd184cd31bdb02bad33b7c1_MD5.jpg)
- 然后点击Create + Place FitSkeleton，插件会生成对位骨骼
- 然后点击BuildAdvancedSkeleton，创建绑定
- 最后点击ConstraintToJoints，绑定到骨骼
# 后续
- 因为插件的原因，手臂和腿的扭转骨骼并没有约束，需要手动实现约束
![](attachments/19e7799342f2d8bf4f744134f9fd7ab1_MD5.jpg)
- 需要用下面一套骨骼的扭曲骨骼父子约束上面一套骨骼的扭曲骨骼
![](attachments/ffb5e6aeb577010a3ef99f996b763285_MD5.jpg)
- 腿部也一样，只不过只约束大腿扭曲骨骼就可以了
![](attachments/f752cd4be0c185e845c3e5aceae189ba_MD5.jpg)