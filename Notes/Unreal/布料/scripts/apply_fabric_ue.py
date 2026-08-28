#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""在 UE 编辑器内把织物库套用到 ClothAsset —— 运行时 Interactor 方案。

【运行位置】UE 5.8 编辑器 → Output Log 的 Cmd 切到 Python，或 Tools > Execute Python Script。
           不要用外部 python 跑，import unreal 会失败。

【工作原理】走 UChaosClothAssetInteractor 的 Set*Value 接口。属性名(PropertyName)
    必须与引擎源码里 UPROPERTY meta 的 InteractorName 完全一致，已逐个核对：
      SimulationStretchConfigNode.h : StretchStiffness / StretchDamping
      SimulationBendingConfigNode.h : BendingStiffness / BendingDamping /
                                      BucklingStiffness / BucklingRatio
      SimulationMassConfigNode.h    : Density
      SimulationCollisionConfigNode.h: FrictionCoefficient / CollisionThickness
      SimulationDampingConfigNode.h : DampingCoefficient
      SimulationAerodynamicsConfigNode.h: Drag / Lift
    API 签名核实自 ClothAssetInteractor.h:155-203：
      SetFloatValue(PropertyName, LODIndex=-1, Value=0.0)
      SetWeightedFloatValue(PropertyName, LODIndex=-1, Value=FVector2D(low, high))
    LODIndex = -1 表示套用到全部 LOD。

【重要】这些 Set 调用作用于**运行时模拟参数**，不写回 Dataflow 图，不落盘。
    要持久化，请在 Dataflow 图的对应 Config 节点上手填（见笔记附的数值表），
    或用 EditorAssetLibrary 改 Dataflow 节点属性（引擎未暴露稳定 Python API，
    5.8 下需 C++ 或 Dataflow 内置节点完成）。

【状态】本脚本尚未在 UE 编辑器内实测运行（撰写时无可用工程）。
    API 签名与属性名均已从 5.8 源码逐字核对，但首次执行请先用 --dry-run 观察输出。
"""
from __future__ import annotations
import json
import os

try:
    import unreal
except ImportError:  # 便于在编辑器外做纯逻辑自检
    unreal = None

# 织物库 JSON 路径（build_library.py 的产物），按需改成你的实际位置
LIBRARY_JSON = r"C:\Users\dalaotian\AppData\Local\Temp\cloth_fabric\chaoscloth_fabric_library.json"

# 织物库字段名 -> 引擎 InteractorName。None 表示该字段不经 Interactor 下发。
# 已逐个与 UE 5.8 源码的 UPROPERTY(..., InteractorName="...") 核对。
FIELD_TO_INTERACTOR = {
    "Density":            ("Density",            "weighted"),
    "StretchStiffness":   ("StretchStiffness",   "weighted"),
    "StretchDamping":     ("StretchDamping",     "weighted"),
    "BendingStiffness":   ("BendingStiffness",   "weighted"),
    "BendingDamping":     ("BendingDamping",     "weighted"),
    "BucklingStiffness":  ("BucklingStiffness",  "weighted"),
    "BucklingRatio":      ("BucklingRatio",      "weighted"),
    "Friction":           ("FrictionCoefficient", "weighted"),
    "CollisionThickness": ("CollisionThickness", "float"),
    "DampingCoefficient": ("DampingCoefficient", "weighted"),
    "Drag":               ("Drag",               "weighted"),
    "Lift":               ("Lift",               "weighted"),
    # 以下是 Solver 节点的整数属性，不走 float 接口，单独处理
    "NumSubsteps":        (None, "int"),
}


def load_library(path: str = LIBRARY_JSON) -> dict:
    """读取织物库，返回 {织物名: 参数字典}。"""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"找不到织物库 JSON：{path}")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return {row["name"]: row for row in data["fabrics"]}


def list_fabrics(path: str = LIBRARY_JSON) -> None:
    """打印全部可用织物名与关键参数，方便挑选。"""
    lib = load_library(path)
    print(f"共 {len(lib)} 种织物：")
    for name, r in lib.items():
        print(f"  [{r['category']:10s}] {name:26s} "
              f"ρ={r['Density']:<5} Stretch={r['StretchStiffness']:<5} "
              f"Bend={r['BendingStiffness']:<6} Buck={r['BucklingStiffness']:<5} "
              f"Ratio={r['BucklingRatio']}")


def apply_fabric(cloth_component, fabric_name: str,
                 lod_index: int = -1, dry_run: bool = False,
                 path: str = LIBRARY_JSON) -> dict:
    """把指定织物参数套到一个 ClothComponent 上。

    Args:
        cloth_component: UChaosClothComponent 实例（或任何能 GetClothAssetInteractor 的组件）
        fabric_name: 织物库里的名字，如 "Denim 12oz 牛仔"
        lod_index: -1 = 全部 LOD
        dry_run: True 时只打印将要下发的值，不真的调用 Set*
    Returns:
        实际下发的 {InteractorName: value} 字典
    """
    lib = load_library(path)
    if fabric_name not in lib:
        raise KeyError(f"织物库里没有 '{fabric_name}'，可用：{list(lib)}")
    fabric = lib[fabric_name]

    interactor = None
    if not dry_run:
        if unreal is None:
            raise RuntimeError("不在 UE 编辑器内，无法取得 Interactor；请用 dry_run=True")
        # ClothComponent 上取交互器；不同组件类型方法名可能不同，做兼容
        for getter in ("get_cloth_asset_interactor", "get_cloth_interactor",
                       "get_current_interactor"):
            if hasattr(cloth_component, getter):
                interactor = getattr(cloth_component, getter)()
                break
        if interactor is None:
            raise RuntimeError(
                "在该组件上找不到 Interactor 取值方法。请在 Output Log 里执行 "
                "dir(your_component) 查看实际方法名，并补进上面的 getter 列表。")

    applied = {}
    for field, (prop_name, kind) in FIELD_TO_INTERACTOR.items():
        if field not in fabric or prop_name is None:
            continue
        value = float(fabric[field])
        applied[prop_name] = value
        if dry_run:
            print(f"  [dry-run] {kind:8s} {prop_name:22s} = {value}")
            continue
        if kind == "weighted":
            # WeightedValue 的 Low/High 都设为同一个值 = 不使用权重贴图时的行为
            interactor.set_weighted_float_value(
                prop_name, lod_index, unreal.Vector2D(value, value))
        else:
            interactor.set_float_value(prop_name, lod_index, value)

    print(f"{'[dry-run] ' if dry_run else ''}已套用织物 '{fabric_name}' "
          f"({fabric['category']})，共 {len(applied)} 个属性")
    print(f"  提示：Solver 建议 NumSubsteps={fabric['NumSubsteps']}，"
          f"目标网格边长 {fabric['TargetMeshEdge_cm'][0]}~{fabric['TargetMeshEdge_cm'][1]} cm"
          f"（这两项须在 SolverConfig 节点与建模阶段设置，Interactor 管不到）")
    if fabric["k_over_rho"] < 1200:
        print(f"  警告：k/ρ={fabric['k_over_rho']} 偏低，重力下会明显伸长，"
              f"请把 LongRangeAttachment 的 TetherStiffness 设为 1.0")
    return applied


def apply_to_selected(fabric_name: str, dry_run: bool = False) -> None:
    """把织物套到当前关卡里选中的所有 Actor 的 ClothComponent 上。"""
    if unreal is None:
        raise RuntimeError("必须在 UE 编辑器内运行")
    actors = unreal.EditorLevelLibrary.get_selected_level_actors()
    if not actors:
        print("没有选中任何 Actor")
        return
    count = 0
    for actor in actors:
        for comp in actor.get_components_by_class(unreal.ActorComponent):
            if "Cloth" in type(comp).__name__:
                try:
                    apply_fabric(comp, fabric_name, dry_run=dry_run)
                    count += 1
                except Exception as exc:  # noqa: BLE001
                    unreal.log_warning(f"{actor.get_name()}: {exc}")
    print(f"共处理 {count} 个布料组件")


if __name__ == "__main__":
    # 编辑器外可安全执行的自检：验证 JSON 能读、映射表完整
    lib = load_library()
    print(f"织物库加载成功：{len(lib)} 种")
    missing = [f for f in FIELD_TO_INTERACTOR
               if f not in next(iter(lib.values())) and f != "NumSubsteps"]
    print(f"映射表缺失字段：{missing or '无'}")
    print()
    list_fabrics()
    print()
    print("=== dry-run 示例：Denim 12oz 牛仔 ===")
    apply_fabric(None, "Denim 12oz 牛仔", dry_run=True)
