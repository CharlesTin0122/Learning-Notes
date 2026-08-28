#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ChaosCloth XPBD 织物库生成 + 引擎约束校验。

数值来源分三级，全部在输出里标注：
  base   = UE 演讲幻灯片原始三列（Silk/Cotton/Leather），一字未改
  epic   = Epic 引擎源码 SimulationMassConfigNode.h 注释里的官方密度锚点
  interp = 本脚本按 GSM + HandFactor 工程插值推出（推理值，需实测校准）

引擎约束区间全部取自 UE 5.8 源码
  D:/ProgramFiles/EpicGames/UE_5.8/Engine/Plugins/ChaosClothAssetDataflowNodes/
    Source/ChaosClothAssetDataflowNodes/Public/ChaosClothAsset/
目标配置：SolverType = XPBD, DistributionType = Isotropic, ConstraintType = HingeAngles
"""
from __future__ import annotations
import json, sys
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. 引擎硬约束（源码实测，见文件头路径）
#    (UIMin, UIMax, ClampMin, ClampMax) —— UIMax 是滑条上限，超出需手动键入数值
# ---------------------------------------------------------------------------
LIMITS = {
    # SimulationMassConfigNode.h:44  DensityWeighted
    "Density":           (0.001, 1.0,   0.0, None),
    # SimulationStretchConfigNode.h:78  StretchStiffness (Isotropic 分支)
    "StretchStiffness":  (0.0,   10000, 0.0, 1_000_000_000),
    # SimulationStretchConfigNode.h:88  StretchDamping
    "StretchDamping":    (0.0,   10,    0.0, 1000),
    # SimulationBendingConfigNode.h:161 BendingStiffness (Isotropic 分支)
    "BendingStiffness":  (0.0,   10000, 0.0, 10_000_000),
    # SimulationBendingConfigNode.h:170 BendingDamping
    "BendingDamping":    (0.0,   10,    0.0, 1000),
    # SimulationBendingConfigNode.h:183 BucklingStiffness  ← UIMax 仅 10
    "BucklingStiffness": (0.0,   10,    0.0, 1000),
    # SimulationBendingConfigNode.h:190 BucklingRatioWeighted
    "BucklingRatio":     (0.0,   1.0,   0.0, 1.0),
}

# XPBDBendingConstraints.h:19 / XPBDStretchBiasElementConstraints.h:25
XPBD_MAX_STIFFNESS = 1e7

# ---------------------------------------------------------------------------
# 2. Epic 官方密度锚点（SimulationMassConfigNode.h:34-43 tooltip 注释原文）
#    这 7 个值同时出现在 legacy ChaosClothConfig.h:109-118，一字不差
# ---------------------------------------------------------------------------
EPIC_DENSITY = {
    "Melton Wool":   0.7,
    "Heavy leather": 0.6,
    "Polyurethane":  0.5,
    "Denim":         0.4,
    "Light leather": 0.3,
    "Cotton":        0.2,
    "Silk":          0.1,
}
# 验证 Density == GSM/1000 这条映射：官方 4 个锚点对上真实织物克重
GSM_CHECK = [
    ("Silk 薄绸缎",   100, 0.1),
    ("Cotton 中厚布", 200, 0.2),
    ("Denim 12oz",    400, 0.4),
    ("Melton 厚呢",   700, 0.7),
]

# ---------------------------------------------------------------------------
# 3. 幻灯片原始基准（用户表 = UE 演讲截图逐字核对，vision 已复核两张图一致）
# ---------------------------------------------------------------------------
BASE = {
    "Silk":    dict(Density=0.10, StretchStiffness=1000, StretchDamping=1.0,
                    BendingStiffness=1,  BendingDamping=0.6,
                    BucklingStiffness=0.2, BucklingRatio=0.7),
    "Cotton":  dict(Density=0.30, StretchStiffness=600,  StretchDamping=0.9,
                    BendingStiffness=5,  BendingDamping=0.9,
                    BucklingStiffness=1,   BucklingRatio=0.5),
    "Leather": dict(Density=0.75, StretchStiffness=400,  StretchDamping=0.5,
                    BendingStiffness=20, BendingDamping=0.2,
                    BucklingStiffness=15,  BucklingRatio=0.2),
}

# ---------------------------------------------------------------------------
# 4. 插值模型
#    BendingStiffness = (GSM/100) * HandFactor
#      HandFactor = 纺织业"手感/硬挺度"系数，与克重解耦——这是欧根纱(轻而硬)
#      和汗布(重而软)能被正确区分的唯一途径。三个基准反解出的锚点：
#        Silk    GSM100 硬挺1.0  -> 1
#        Cotton  GSM200 硬挺2.5  -> 5     （用 Epic 官方 200gsm，非幻灯片 300）
#        Leather GSM600 硬挺3.33 -> 20    （用 Epic heavy leather 0.6）
# ---------------------------------------------------------------------------
def bending_from(gsm: float, hand: float) -> float:
    v = gsm / 100.0 * hand
    return round(v, 2) if v < 10 else round(v)

# 织物定义： (名称, 分类, GSM, HandFactor, StretchStiff, StretchDamp,
#             BendingDamp, BucklingStiff, BucklingRatio, 备注)
# StretchStiffness 分档依据（基准反解）：
#   梭织紧密 900-1400 / 梭织常规 600-800 / 皮膜无纺 250-500 / 针织 90-250
# BucklingRatio 语义（PBDBendingConstraintsBase.h:277-282 实测）：
#   buckled 条件 (PI-|Angle|) < Ratio*(PI-|RestAngle|)
#   Ratio 越大 => 越早切到 BucklingStiffness => 褶多而细
#   Ratio=0 永不 buckle；Ratio=1 一离开静止角就 buckle
FABRICS = [
 # ---- 超轻薄（<100 GSM）----
 ("Tulle 网纱",            "ultralight",  30, 8.0,   900, 0.90, 0.30, 2.0,  0.90, "极轻但有骨，蓬起"),
 ("Chiffon 真丝雪纺",       "ultralight",  40, 0.5,  1200, 1.00, 0.50, 0.03, 0.85, "流体感，靠高 Drag 出飘感"),
 ("Organza 欧根纱",         "ultralight",  60, 13.0, 1400, 1.00, 0.30, 6.0,  0.30, "轻≠软：密度最低但极硬挺"),
 ("Ripstop 尼龙防风布",     "ultralight",  60, 5.0,  1300, 1.00, 0.40, 1.5,  0.55, "冲锋衣/降落伞，脆响鼓包"),
 ("Taffeta 塔夫绸",         "ultralight",  80, 6.0,  1100, 1.00, 0.40, 4.0,  0.45, "纸感沙沙，高回弹"),
 ("Silk 真丝绸缎",          "BASE",       100, 1.0,  1000, 1.00, 0.60, 0.2,  0.70, "幻灯片基准列，原值未改"),
 # ---- 轻中薄梭织 + 针织（100-250 GSM）----
 ("Cotton Voile 巴厘纱",    "light",      110, 0.8,   800, 0.95, 0.70, 0.15, 0.75, "棉里最垂"),
 ("Poplin 棉平纹衬衫布",     "light",      140, 1.8,   700, 0.90, 0.80, 0.50, 0.55, "衬衫标准件"),
 ("Linen 亚麻",            "light",      180, 3.5,   900, 0.95, 0.50, 0.12, 0.80, "留折痕：早切换+折后极软"),
 ("Jersey 棉针织汗布",      "knit",       180, 0.7,   220, 0.60, 0.90, 0.30, 0.70, "T恤，纬向拉伸远大于经向"),
 ("Spandex 氨纶莱卡",       "knit",       220, 0.3,    90, 0.50, 0.80, 0.20, 0.65, "紧身衣，基本贴身不飘"),
 # ---- 中厚（250-450 GSM）----
 ("Rib Knit 罗纹针织",      "knit",       260, 0.8,   150, 0.55, 0.90, 0.50, 0.65, "领口袖口，纬向超弹"),
 ("Worsted Wool 精纺西装料","medium",     280, 1.6,   550, 0.85, 1.00, 0.60, 0.50, "垂顺带体感，阻尼最高档"),
 ("Cotton 中厚棉斜纹",      "BASE",       200, 2.5,   600, 0.90, 0.90, 1.0,  0.50, "幻灯片基准列（密度改用 Epic 官方 0.2）"),
 ("Velvet 天鹅绒",         "medium",     320, 1.9,   500, 0.85, 1.00, 1.2,  0.55, "绒毛吃掉高频抖动"),
 ("Denim 12oz 牛仔",       "medium",     400, 4.5,   700, 0.90, 0.60, 2.5,  0.35, "官方密度锚点 0.4，命中 12oz"),
 ("Chunky Knit 粗针毛衣",   "knit",       450, 2.2,   130, 0.60, 1.00, 3.0,  0.60, "厚+弹，须开自碰撞"),
 # ---- 厚重硬挺（>450 GSM）----
 ("Polyurethane 聚氨酯革",  "heavy",      500, 2.6,   350, 0.60, 0.50, 6.0,  0.25, "官方密度锚点 0.5"),
 ("Suede 翻毛皮",          "heavy",      520, 2.2,   420, 0.60, 0.80, 4.0,  0.30, "死沉不回弹，比光面皮软"),
 ("Canvas 帆布/篷布",      "heavy",      500, 5.0,   800, 0.95, 0.40, 8.0,  0.28, "军包、篷帆"),
 ("Leather 皮革",          "BASE",       600, 3.33,  400, 0.50, 0.20, 15,   0.20, "幻灯片基准列（密度改用 Epic heavy leather 0.6）"),
 ("Vinyl 漆皮/PVC",        "heavy",      650, 3.4,   500, 0.70, 0.30, 12,   0.22, "高光面须配低摩擦"),
 ("Melton Wool 麦尔登呢",   "heavy",      700, 4.3,   450, 0.70, 0.50, 22,   0.25, "官方密度锚点 0.7；不留折痕、高回弹"),
 ("Neoprene 3mm 潜水料",   "heavy",      750, 4.7,   250, 0.60, 0.60, 25,   0.18, "弹+极硬挺，永不起皱"),
 # ---- 非织物 / 道具 ----
 ("Paper 纸/羊皮纸",        "prop",        80, 18.0, 2000, 1.00, 0.20, 0.05, 0.95, "永久折痕：极早切换+折后近零刚度"),
 ("Burlap 麻袋布",         "prop",       350, 3.4,   750, 0.90, 0.50, 3.0,  0.40, "粗糙、大尺度褶"),
 ("Tarp 防水涂层布",        "prop",       450, 4.4,  1200, 1.00, 0.30, 9.0,  0.35, "涂层布，脆响"),
 ("Rubber Raincoat 橡胶雨衣","prop",      650, 1.8,   300, 0.65, 0.90, 5.0,  0.30, "高阻尼、高摩擦"),
 ("Chainmail 锁子甲",      "armor",     2000, 0.075, 8000, 1.00, 0.80, 0.40, 0.85, "重+不可拉伸+极易弯，反直觉"),
 ("Scale Mail 鳞甲",       "armor",     2500, 0.48, 9000, 1.00, 0.70, 8.0,  0.30, "片状单元，弯曲受限"),
]

# 每类的配套非本表参数（Aero/Friction/Collision/Damping/SubStep）
# Friction 默认 = FDefaultFabric::Friction = 0.8（源码值，比常见直觉偏高）
CATEGORY_EXTRA = {
 "ultralight": dict(Drag=0.40, Lift=0.15, Friction=0.40, CollisionThickness=0.3, DampingCoefficient=0.008, NumSubsteps=3),
 "light":      dict(Drag=0.15, Lift=0.06, Friction=0.60, CollisionThickness=0.5, DampingCoefficient=0.015, NumSubsteps=2),
 "knit":       dict(Drag=0.10, Lift=0.04, Friction=0.70, CollisionThickness=0.8, DampingCoefficient=0.025, NumSubsteps=2),
 "medium":     dict(Drag=0.08, Lift=0.03, Friction=0.80, CollisionThickness=1.0, DampingCoefficient=0.040, NumSubsteps=3),
 "heavy":      dict(Drag=0.03, Lift=0.01, Friction=0.85, CollisionThickness=1.5, DampingCoefficient=0.080, NumSubsteps=4),
 "prop":       dict(Drag=0.12, Lift=0.05, Friction=0.80, CollisionThickness=1.0, DampingCoefficient=0.050, NumSubsteps=3),
 "armor":      dict(Drag=0.02, Lift=0.00, Friction=0.90, CollisionThickness=1.5, DampingCoefficient=0.100, NumSubsteps=5),
 "BASE":       dict(Drag=0.10, Lift=0.04, Friction=0.80, CollisionThickness=1.0, DampingCoefficient=0.030, NumSubsteps=2),
}
# 目标网格边长（cm）——褶皱波长由分辨率决定，参数救不回来
MESH_EDGE = {"ultralight": (0.5, 1.0), "light": (1.0, 1.5), "knit": (1.0, 2.0),
             "medium": (1.5, 2.0), "heavy": (2.0, 3.5), "prop": (1.5, 3.0),
             "armor": (2.0, 3.0), "BASE": (1.0, 2.0)}


def build() -> list[dict]:
    out = []
    for (name, cat, gsm, hand, sst, sdmp, bdmp, bst, brat, note) in FABRICS:
        real_cat = cat
        if cat == "BASE":
            real_cat = {"Silk 真丝绸缎": "ultralight", "Cotton 中厚棉斜纹": "medium",
                        "Leather 皮革": "heavy"}[name]
        base_row = BASE.get(name.split()[0])
        if cat == "BASE":
            bend = base_row["BendingStiffness"]
            source = "base(幻灯片原值) + epic(密度锚点)"
        else:
            bend = bending_from(gsm, hand)
            source = "interp(GSM×HandFactor 插值，推理值)"
        row = dict(
            name=name, category=real_cat, source=source, note=note,
            GSM=gsm, HandFactor=hand,
            Density=round(gsm / 1000.0, 3),
            StretchStiffness=sst, StretchDamping=sdmp,
            BendingStiffness=bend, BendingDamping=bdmp,
            BucklingStiffness=bst, BucklingRatio=brat,
            **CATEGORY_EXTRA[real_cat],
        )
        row["TargetMeshEdge_cm"] = list(MESH_EDGE[real_cat])
        # 派生诊断量
        row["BucklingOverBending"] = round(bst / bend, 3) if bend else None
        row["k_over_rho"] = round(sst / row["Density"])
        out.append(row)
    return out


def validate(rows: list[dict]) -> tuple[list[str], list[str]]:
    errors, warns = [], []
    for r in rows:
        for key, (uimin, uimax, cmin, cmax) in LIMITS.items():
            v = r[key]
            if cmin is not None and v < cmin:
                errors.append(f"{r['name']}: {key}={v} < ClampMin {cmin}")
            if cmax is not None and v > cmax:
                errors.append(f"{r['name']}: {key}={v} > ClampMax {cmax}  [引擎会截断！]")
            if v > uimax:
                warns.append(f"{r['name']}: {key}={v} > UIMax {uimax} (滑条拖不到，须手动键入)")
            if key == "Density" and v < uimin:
                warns.append(f"{r['name']}: Density={v} < UIMin {uimin}")
        for key in ("StretchStiffness", "BendingStiffness"):
            if r[key] > XPBD_MAX_STIFFNESS:
                errors.append(f"{r['name']}: {key} 超 XPBD MaxStiffness 1e7")
        # 物理自洽性：Epic 注释明确 "Typically, Buckling Stiffness is set to be
        # less than Bending Stiffness"
        if r["BucklingStiffness"] > r["BendingStiffness"]:
            warns.append(f"{r['name']}: BucklingStiffness({r['BucklingStiffness']}) "
                         f"> BendingStiffness({r['BendingStiffness']}) —— 违反官方"
                         f"'typically less than'，会出现折后变硬的反直觉行为")
        # XPBD 抗重力伸长：k/rho 太低时重料会被拉成橡皮筋
        if r["k_over_rho"] < 1200:
            warns.append(f"{r['name']}: k/ρ={r['k_over_rho']} 偏低，"
                         f"重力下伸长明显，必须靠 TetherStiffness=1.0 兜住")
    return errors, warns


def main() -> int:
    # 先验证 Density == GSM/1000 这条映射对得上 Epic 官方锚点
    print("=" * 74)
    print("STEP 1  验证 Density = GSM/1000 映射 vs Epic 源码官方锚点")
    print("=" * 74)
    ok = True
    for label, gsm, epic in GSM_CHECK:
        got = gsm / 1000.0
        hit = abs(got - epic) < 1e-9
        ok &= hit
        print(f"  {label:16s} {gsm:>5d} g/m2 -> {got:.3f}   官方 {epic:.3f}   "
              f"{'MATCH' if hit else 'MISS'}")
    print(f"  => 映射{'成立（4/4 命中）' if ok else '不成立'}\n")

    rows = build()
    print("=" * 74)
    print(f"STEP 2  生成织物库：{len(rows)} 种")
    print("=" * 74)
    from collections import Counter
    for c, n in sorted(Counter(r["category"] for r in rows).items()):
        print(f"  {c:12s} {n:>2d} 种")

    print()
    print("=" * 74)
    print("STEP 3  引擎约束校验（区间取自 UE 5.8 源码 UPROPERTY meta）")
    print("=" * 74)
    errors, warns = validate(rows)
    print(f"  ERROR (会被引擎截断/拒绝): {len(errors)}")
    for e in errors:
        print("    x", e)
    print(f"  WARN  (合法但需注意): {len(warns)}")
    for w in warns:
        print("    !", w)

    out = Path(__file__).parent / "chaoscloth_fabric_library.json"
    payload = dict(
        schema="chaoscloth-xpbd-fabric-library/1",
        engine="UE 5.8 (D:/ProgramFiles/EpicGames/UE_5.8)",
        target_config=dict(SolverType="XPBD", DistributionType="Isotropic",
                           ConstraintType="HingeAngles", MassMode="Density"),
        provenance=dict(
            base="UE 演讲幻灯片 Silk/Cotton/Leather 三列，原值未改",
            epic_density_anchors=EPIC_DENSITY,
            epic_density_source="Engine/Plugins/ChaosClothAssetDataflowNodes/.../"
                                "SimulationMassConfigNode.h:34-43 (tooltip 注释)",
            engine_default_fabric="FDefaultFabric, CollectionClothFabricFacade.h:11",
            interp="其余织物 = GSM×HandFactor 工程插值，属推理值，须实测校准",
        ),
        limits=LIMITS, xpbd_max_stiffness=XPBD_MAX_STIFFNESS,
        validation=dict(errors=errors, warnings=warns),
        fabrics=rows,
    )
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  已写出 -> {out}  ({out.stat().st_size} bytes)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
