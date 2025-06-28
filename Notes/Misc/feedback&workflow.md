# rigging of Master Key
## feedback
- 眉毛模型Eyebrows_LOD0和眼睛模型Eyes_LOD0并未按照要求将模型冻结变换，其旋转属性仍有数值
- ![](attachments/feedback&workflow.png)   ![](attachments/feedback&workflow-2.png) 
- 因此导致其局部旋转轴也是错误的并非跟世界坐标一致
- ![|300](attachments/feedback&workflow-1.png)
- 身体模型在关节转折处有过多的星状点和三角面，可能会影响变形效果
- ![](attachments/feedback&workflow-3.png)
## workflow
- 根据测试需求的描述，Master Key模型可以使用熟悉的工具进行绑定，主要考察关节放置和变形效果。为了节省时间，不再采用手工绑定的模式。
- 我熟悉的绑定工具有mGear绑定框架和Advanced Skeleton绑定插件。而mGear绑定框架绑定的模型必须在安装该框架的maya环境中才能使用，所以这里使用Advanced Skeleton绑定插件进行绑定。
- maya软件版本为2024.2，轴向为Y轴向上，单位为厘米。Advanced Skeleton绑定插件版本为Advanced Skeleton-6.574
# rigging of Minigun
## feedback
## workflow
# Simulate Physics In-Engine
# workflow