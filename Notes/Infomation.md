这会导致命令返回一个字符串数组，其中包含所有现有事件的名称。以下是描述对于所有现有事件：

_angularToleranceChanged：_

当角度单位的公差发生变化时。可以通过以下方式更改此公差：

1. 使用 MEL 命令，带有“-angular”标志的“公差”
2. 更改选项->常规首选项->下的首选项建模选项卡->切向公差

_angularUnitChanged：_

当用户更改角度单位时。

_axisAtOriginChanged：_

当轴在原点处发生变化时。

_axisInViewChanged：_

当轴在特定视图处发生变化时。

_ColorIndex已更改：_

当颜色索引值发生变化时。

_constructionHistoryChanged：_

当施工历史记录打开或关闭时。

_currentContainerChanged：_

当用户设置或取消设置当前容器时。

_currentSoundNodeChanged：_

每当时间滑块中显示的声音发生变化时 由于：

1. 声音被删除（或不再显示）[时间滑块中的人民币]
2. 显示新声音 [时间滑块中的 RMB]
3. 切换声音显示 [动画选项]
4. 正在更改声音显示模式 [动画选项]

_DagObjectCreated：_

创建新的 DAG 对象时。

_deleteAll：_

当出现新文件时

_DisplayColorChanged：_

当显示颜色发生变化时。

_displayLayerChange：_

创建或销毁图层时。

_displayLayerManagerChange：_

当显示图层管理器发生更改时。

_DisplayRGBColorChanged：_

当 RGB 显示颜色发生变化时。

_glFrameTrigger 中：_

仅供内部使用。

_ChannelBoxLabelSelected：_

当通道框标签（第一列）选择发生变化时。

_gridDisplayChanged：_

仅供内部使用。

_怠：_

当 Maya 处于空闲状态且没有高优先级空闲任务时

_闲置高：_

当玛雅闲置时。在低优先级空闲之前调用 任务。您几乎应该始终使用“空闲”。

_lightLinkingChanged：_

当发生任何修改光链接的变化时 关系。

_lightLinkingChangedNonSG：_

当发生任何修改光链接的变化时 关系，除非更改是阴影的更改 分配。

_linearToleranceChanged：_

当线性公差已更改时。这种公差 可以通过以下方式更改：

- 使用 MEL 命令，带有“-linear”标志的“tolerance”
- 更改 Options->GeneralPreferences-> 下的首选项 建模选项卡->位置公差

_linearUnitChanged：_

当用户通过“选项”菜单更改线性单位时。

_MenuModeChanged：_

当用户更改 Maya 主窗口中菜单栏的菜单集时 （例如，从“建模”到“动画”）。

_RecentCommandChanged：_

仅供内部使用。

_新场景打开：_

打开新场景时。

_后场景阅读：_

在阅读场景之后。特别是在文件打开、导入或所有子文件之后 已阅读参考文献。

_nurbsToPolygonsPrefs已更改：_

当任何 NURBS 到多边形的首选项发生更改时。这些 可以通过以下方式更改首选项：

- 使用 Mel 命令“nurbsToPolygonsPref”
- 将 Polygons->Nurbs 下的首选项更改为 多边形->选项框

_playbackRangeChanged：_

当播放关键帧范围发生变化时。

_playbackRangeSliderChanged：_

当动画开始/结束范围（即最左边的 或时间滑块范围内最右边的入口单元格，即内部 调整播放范围）改变

_preferredRendererChanged：_

当首选渲染器发生变化时。

_退出应用：_

当用户选择退出时，无论是通过退出 MEL 命令，或通过退出菜单项。

_重做：_

当用户从菜单中选择重做并且有东西时 重做。此回调可用于更新 UI 或本地 存储。在此期间不要更改场景或 DG 的状态 回调。

_renderLayerChange：_

创建或删除渲染层节点时。

_renderLayerManagerChange：_

当前渲染层发生更改时。

_RebuildUIValues：_

仅供内部使用。

_场景打开：_

当场景已打开时。

_场景保存：_

当场景被保存时。

_SelectionChanged：_

进行新选择时。

_UFESelection已更改：_

当进行新的 UFE 选择时。

_SelectModeChanged：_

当选择模式发生变化时。

_SelectPreferenceChanged：_

仅供内部使用。

_SelectPriorityChanged：_

当选择优先级发生变化时。

_SelectTypeChanged：_

当选择类型发生变化时。

_setEditorChanged：_

过时。不再使用。

_SetModified：_

当使用 set 命令修改集合时

_SequencerActiveShotChanged：_

当活动Sequencer镜头发生变化时。

_snapModeChanged：_

当捕捉模式更改时。例如，对网格捕捉的更改。

_时间更改：_

当时间变时。

_timeUnitChanged：_

当用户更改时间单位时。

_工具更改：_

当用户更改工具/上下文时。

_PostToolChanged：_

在用户更改工具/上下文后。

_名称更改：_

当用户使用 rename 命令更改对象的名称时。

_撤消：_

当用户从菜单中选择撤消并且有 要撤消的东西。此回调可用于更新 UI 或本地 存储。在此期间不要更改场景或 DG 的状态 回调。

_modelEditorChanged：_

当用户更改模型编辑器的选项时。

_colorMgtEnabledChanged：_

当全局每场景颜色管理启用标志更改时。

_colorMgtConfigFileEnableChanged：_

启用全局每场景色彩管理OCIO配置时 标志更改。

_colorMgtPrefsViewTransformChanged：_

当全局“每个场景颜色管理”视图变换首选项时 转换更改。

_colorMgtWorkingSpaceChanged：_

当全局每个场景颜色管理工作空间发生变化时。

_colorMgtConfigFilePathChanged：_

当全局每场景色彩管理OCIO配置文件路径 变化。

_colorMgtConfigChanged：_

当颜色管理模式从原生更改为 OCIO 时，或当 加载不同的 OCIO 配置。

_colorMgtPrefsReloaded：_

当重新加载所有全局每个场景颜色管理设置时。

_colorMgtUserPrefsChanged：_

当任何用户级别的颜色管理首选项发生更改时。

_colorMgtOutputChanged：_

当颜色管理转换或其启用状态发生更改时。

_colorMgtOCIORules已更改：_

当 OCIO 模式下的规则类型发生变化时。

_colorMgtRefreshed：_

刷新颜色管理以捕获环境变量更改时。

_metadataVisualStatusChanged：_

仅供内部使用。

_shapeEditorTreeviewSelectionChanged：_

在形状编辑器的树视图中进行新选择时。

_RenderViewCamera已更改：_

当渲染视图的当前摄像机发生更改时。

_tabletModeChanged：_

仅限 Windows：如果您的设备是平板电脑，则可转换模式具有 改变。您可以使用命令 _about -tabletMode_ 查询您的设备是否 当前在平板电脑或笔记本电脑（连接键盘）模式下运行。