1. 动画曲线选中，在值栏输入：/=-1。可以使曲线上下镜像

2. 根骨骼动画中hip和root的关系：

	hipX=rootZ
	
	hipY=rootY
	
	hipZ=-rootX

3. joint -e -zso:统一骨骼局部旋转轴和局部位移轴

4. 传递动画用骨骼约束控制器时使用父子约束，用父子约束时选择要使用位移旋转还是只使用旋转，可保证约束后控制器数值为0.

5. 虚幻和maya轴向：位移中Y轴相反，旋转中YZ轴相反。常用于根据maya中Locator的位置定位引擎中socket的位置
6. maya在启动时崩溃可能由OpenCL引起。通过在Maya.env文件中添加“MAYA_DISABLE_OPENCL=1”（不带引号）来禁用OpenCL。


