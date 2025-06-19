# 类和资产
## 常用类
```python
import unreal

# 虚幻类的实例化
sys_lib = unreal.SystemLibrary()
# 编辑器工具类
editor_util_lib = unreal.EditorUtilityLibrary()
# 资产管理类
asset_editor = unreal.EditorAssetLibrary()
# 蒙皮权重修饰类
weight_modifier = unreal.SkinWeightModifier()
# 骨骼修饰类
skeleton_modifier = unreal.SkeletonModifier()
# 骨骼网格体管理类
skeletal_mesh_library = unreal.EditorSkeletalMeshLibrary()
# AnimationLibrary 是一个静态库，提供了一系列用于操作和查询动画数据的实用函数。
# 它主要用于在蓝图（Blueprints）或Python脚本中执行与动画相关的通用操作，而无需直接修改动画资产。
anim_lib = unreal.AnimationLibrary()
# AnimationDataController 是一个专门用于控制和修改动画数据的类，通常用于编辑器中对动画序列（Animation Sequence）的直接编辑。
# 它提供了对动画数据的低级别访问，允许用户动态修改动画的骨骼轨迹、帧数据等。
AnimDataCtrler = unreal.AnimationDataController()
# 用于在 AnimPose 上填充、检索和设置数据
anim_pose_ext = unreal.AnimPoseExtensions()
# 数学类
MathLibrary = unreal.MathLibrary()
# 字符串类
string_lib = unreal.StringLibrary()
```
## 获取资产
```python
selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
# 获取路径下所有资产路径
asset_path = unreal.EditorAssetLibrary.list_assets(unreal_path)
# 加载资产，通过路径获取对象
skel_mesh = unreal.EditorAssetLibrary.load_asset(unreal_path)
```