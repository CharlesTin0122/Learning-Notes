```cpp
// 从选中的资产数组中获取动画序列并尝试转换为 UAnimSequence 类型
UAnimSequence *AnimSequence = Cast<UAnimSequence>(SelectedAssets[AssetIdx].GetAsset());
if (!AnimSequence) { continue; } // 如果转换失败，跳过当前循环

// 获取动画序列的数据模型并转换为 IAnimationDataModel 接口类型
IAnimationDataModel *AnimDataModel = Cast<IAnimationDataModel>(AnimSequence->GetDataModel());
if (!AnimDataModel) { continue; } // 如果数据模型为空，跳过当前循环

// 获取动画数据控制器
TScriptInterface<IAnimationDataController> AnimDataController = AnimDataModel->GetController();
if (!AnimDataController) { continue; } // 如果控制器为空，跳过当前循环

// 打开一个操作括号，用于记录设置帧率的操作，便于撤销重做
AnimDataController->OpenBracket(LOCTEXT("SetFrameRateModifier_Bracket", "Set Frame Rate"), false);

// 定义目标帧率，分子为输入值，分母为 1
FFrameRate TargetFrameRate = FFrameRate(InTargetFrameRate, 1);
// 获取当前帧率的小数值
float CurrentFrameRate = AnimDataModel->GetFrameRate().AsDecimal();
// 获取动画的总播放长度
float AnimationLength = AnimSequence->GetPlayLength();
// 获取当前采样的关键帧数量
int32 CurrentNumberOfSampledKeys = AnimSequence->GetNumberOfSampledKeys();

// 如果当前帧率与目标帧率几乎相等，则跳过处理
if (FMath::IsNearlyEqual(CurrentFrameRate, InTargetFrameRate)) { continue; }

// 根据动画长度和目标帧率计算新的采样关键帧数量
int32 NewNumberOfSampledKeys = FMath::RoundToInt(AnimationLength * InTargetFrameRate);

// 定义一个数组，用于存储骨骼轨迹名称
TArray<FName> BoneTrackNames;
// 获取所有骨骼轨迹名称
AnimDataModel->GetBoneTrackNames(BoneTrackNames);

// 定义一个映射表，用于存储原始骨骼轨迹的变换数据
TMap<FName, TArray<FTransform>> OriginBoneTrackTransforms;
for (const FName &BoneTrackName : BoneTrackNames)
{
    // 为每个骨骼轨迹获取其变换数据并存入映射表
    AnimDataModel->GetBoneTrackTransforms(BoneTrackName, OriginBoneTrackTransforms.FindOrAdd(BoneTrackName));
}

// 设置新的帧率
AnimDataController->SetFrameRate(TargetFrameRate, false);
// 设置新的帧数
AnimDataController->SetNumberOfFrames(FFrameNumber(NewNumberOfSampledKeys), false);

// 定义一个结构体，用于存储新的变换数据（位置、旋转、缩放）
struct FTransformArray
{
    TArray<FVector> Positions; // 位置数组
    TArray<FQuat> Rotations;   // 旋转数组
    TArray<FVector> Scales;    // 缩放数组
};

// 定义一个映射表，用于存储新的骨骼轨迹变换数据
TMap<FName, FTransformArray> NewBoneTrackTransforms;
for (const TPair<FName, TArray<FTransform>> &OriginBoneTrackTransform : OriginBoneTrackTransforms)
{
    // 对每个原始骨骼轨迹进行处理
    for (int32 Frame = 0; Frame < NewNumberOfSampledKeys; ++Frame)
    {
        // 根据目标帧率计算当前帧的时间点
        float Time = (float)Frame / (float)InTargetFrameRate;
        FTransform InterpolatedTransform; // 用于存储插值后的变换

        // 将时间转换为原始帧率下的时间
        float OriginalTime = Time * CurrentFrameRate;
        int32 LowerFrame = FMath::FloorToInt(OriginalTime); // 下界帧
        int32 UpperFrame = FMath::CeilToInt(OriginalTime);  // 上界帧
        float Alpha = OriginalTime - LowerFrame;            // 插值权重

        // 如果下界和上界帧在有效范围内，进行插值
        if (LowerFrame >= 0 && UpperFrame < CurrentNumberOfSampledKeys)
        {
            const FTransform &LowerTransform = OriginBoneTrackTransform.Value[LowerFrame]; // 下界变换
            const FTransform &UpperTransform = OriginBoneTrackTransform.Value[UpperFrame]; // 上界变换
            InterpolatedTransform.Blend(LowerTransform, UpperTransform, Alpha);            // 插值计算
        }
        else
        {
            // 如果超出范围，使用最后一个有效变换
            InterpolatedTransform = OriginBoneTrackTransform.Value.Last();
        }

        // 将插值结果存入新的变换数组
        FTransformArray &NewNewBoneTrackTransform = NewBoneTrackTransforms.FindOrAdd(OriginBoneTrackTransform.Key);
        NewNewBoneTrackTransform.Positions.Add(InterpolatedTransform.GetLocation()); // 添加位置
        NewNewBoneTrackTransform.Rotations.Add(InterpolatedTransform.GetRotation()); // 添加旋转
        NewNewBoneTrackTransform.Scales.Add(InterpolatedTransform.GetScale3D());     // 添加缩放
    }
}

// 定义要设置的关键帧范围，从 0 到新的采样关键帧数量
const FInt32Range KeyRangeToSet(0, NewNumberOfSampledKeys);
for (TPair<FName, FTransformArray> &NewBoneTrackTransform : NewBoneTrackTransforms)
{
    // 更新骨骼轨迹的关键帧数据，包括位置、旋转和缩放
    AnimDataController->UpdateBoneTrackKeys(
        NewBoneTrackTransform.Key, KeyRangeToSet, NewBoneTrackTransform.Value.Positions,
        NewBoneTrackTransform.Value.Rotations, NewBoneTrackTransform.Value.Scales, false);
}

// 通知数据已更新
AnimDataController->NotifyPopulated();
// 关闭操作括号，完成帧率设置操作
AnimDataController->CloseBracket(false);
```
# 关于AnimDataController->OpenBracket 和 AnimDataController->CloseBracket
`AnimDataController->OpenBracket` 和 `AnimDataController->CloseBracket` 是 Unreal Engine 中动画数据控制器的接口方法（`IAnimationDataController`），用于管理动画数据的修改操作。它们通常用于支持撤销/重做功能（Undo/Redo），类似于事务（Transaction）机制。下面是对这两个方法的详细介绍：

---

### 1. `AnimDataController->OpenBracket`
- **函数签名**（示例）：
  ```cpp
  void OpenBracket(const FText& InDescription, bool bShouldTransact = true);
  ```
- **功能**：
  - `OpenBracket` 用于开启一个操作范围（或称为“括号”），表示接下来的一系列修改操作将被视为一个整体。
  - 它的主要作用是将后续的动画数据修改操作分组，以便在需要时可以通过撤销（Undo）一次性回滚整个操作组。
  - 这在编辑器中非常有用，比如调整帧率、关键帧或其他动画属性时，可以确保这些更改作为一个原子操作记录下来。
- **参数**：
  - `InDescription`（类型 `FText`）：描述这个操作的文本，通常用于在编辑器的撤销历史中显示。例如，在代码中使用了 `LOCTEXT("SetFrameRateModifier_Bracket", "Set Frame Rate")`，表示这个操作是“设置帧率”。
  - `bShouldTransact`（类型 `bool`）：是否启用事务支持（即是否记录到撤销历史中）。在您的代码中传入 `false`，表示不启用事务，可能是在特定场景下不需要撤销功能。
- **代码中的使用**：
  ```cpp
  AnimDataController->OpenBracket(LOCTEXT("SetFrameRateModifier_Bracket", "Set Frame Rate"), false);
  ```
  - 这里开启了一个名为“Set Frame Rate”的操作组，但由于 `bShouldTransact = false`，这次操作不会记录到撤销历史中。

---

### 2. `AnimDataController->CloseBracket`
- **函数签名**（示例）：
  ```cpp
  void CloseBracket(bool bShouldTransact = true);
  ```
- **功能**：
  - `CloseBracket` 用于关闭之前由 `OpenBracket` 开启的操作范围，表示这一组修改操作已完成。
  - 如果事务支持是启用的（即 `bShouldTransact = true`），关闭括号后，引擎会将这组操作作为一个整体提交到撤销系统中。
  - 它与 `OpenBracket` 配对使用，确保操作的开始和结束明确定义。
- **参数**：
  - `bShouldTransact`（类型 `bool`）：是否将这组操作提交到事务系统中。在您的代码中传入 `false`，与 `OpenBracket` 的设置保持一致，表示不记录事务。
- **代码中的使用**：
  ```cpp
  AnimDataController->CloseBracket(false);
  ```
  - 这里关闭了之前开启的操作组。由于 `bShouldTransact = false`，这次操作不会被记录为可撤销的操作。

---

### 工作原理与用途
- **事务机制**：
  - `OpenBracket` 和 `CloseBracket` 类似于数据库中的“开始事务”和“提交事务”。它们将一系列动画数据修改（例如设置帧率、更新关键帧等）封装为一个单元。
  - 如果启用了事务支持（`bShouldTransact = true`），这些操作会被记录到 Unreal Engine 的 `Transaction` 系统，用户可以通过编辑器的“撤销”功能回滚到操作前的状态。
- **配对使用**：
  - 这两个方法必须配对调用，否则可能会导致未定义行为（例如括号未关闭，影响后续操作的正确性）。
- **禁用事务的场景**：
  - 在您的代码中，`bShouldTransact` 被设置为 `false`，可能是因为：
    1. 这段代码是在非交互式环境中运行（例如批量处理脚本），不需要用户撤销。
    2. 为了性能优化，避免频繁记录事务。
    3. 操作本身是临时的或不需要持久化。

---

### 代码中的上下文
在您的代码中，这两个方法用于包裹帧率调整和关键帧重新采样的逻辑：
```cpp
AnimDataController->OpenBracket(LOCTEXT("SetFrameRateModifier_Bracket", "Set Frame Rate"), false);
// 中间执行帧率设置、关键帧插值等操作
AnimDataController->CloseBracket(false);
```
- **目的**：将整个帧率修改流程（包括设置新帧率、计算新关键帧、更新骨骼变换等）作为一个逻辑单元。
- **效果**：即使 `bShouldTransact = false`，这种分组仍然有助于代码的结构化和调试，确保操作的边界清晰。

---

### 总结
- **`OpenBracket`**：开启一个操作组，定义修改的起点。
- **`CloseBracket`**：关闭操作组，定义修改的终点。
- **事务支持**：通过 `bShouldTransact` 参数控制是否记录到撤销历史。
- **用途**：在动画编辑中提供结构化的修改管理，支持编辑器的高级功能（如撤销/重做）。

如果您有更多关于这两个方法的具体问题或需要进一步的代码分析，请告诉我！