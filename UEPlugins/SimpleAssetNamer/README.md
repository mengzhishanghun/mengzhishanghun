# Simple Asset Namer 使用教程

## 目录

1. [设置说明](#1-设置说明)
2. [使用方法](#2-使用方法)
3. [常见问题](#3-常见问题)

---

## 1. 设置说明

打开 **Edit → Project Settings → Simple Asset Namer**

### 1.1 General（通用设置）

| 选项 | 说明 |
|-----|------|
| Auto Rename on Create | 创建/导入资产时自动重命名 |
| Auto Rename on Rename | 手动重命名资产后自动修正为标准格式 |

### 1.2 Filter（路径筛选）

| 选项 | 说明 |
|-----|------|
| Filter Type | 筛选模式：Blacklist（排除指定路径）/ Whitelist（仅处理指定路径）|
| Exclude Paths | 黑名单模式下，这些路径的资产不会被处理 |
| Include Paths | 白名单模式下，只有这些路径的资产会被处理 |

**默认排除路径**：
- `/Game/__ExternalActors__` - World Partition 自动生成
- `/Game/__ExternalObjects__` - World Partition 自动生成
- `/Game/Developers` - 开发者个人文件夹
- `/Game/Collections` - 集合文件夹

### 1.3 Delimiter（分隔符设置）

| 选项 | 说明 | 默认值 |
|-----|------|-------|
| Delimiter | 生成名称时使用的分隔符 | `_` |
| Delimiter Detection List | 识别旧名称时的分隔符列表 | `_`, `-`, `.` |
| Legacy Affixes | 旧命名风格的词缀列表，用于识别历史命名 | - |

**示例**：输入 `bp-MyActor` 或 `bp.MyActor` → 输出 `BP_MyActor`

### 1.4 Naming Rules（命名规则）

| 选项 | 说明 |
|-----|------|
| Asset Type Naming Rules | 资产类型与前后缀的映射表，可自定义添加/修改/删除 |

**命名格式**：`前缀_名称_后缀`（后缀可选）

**默认规则（52 种）**：

| 类别 | 资产类型 | 前缀 | 后缀 | 示例 |
|-----|---------|------|------|------|
| Gameplay | GameModeBase | GM | | `GM_MyMode` |
| | GameStateBase | GS | | `GS_MyState` |
| | PlayerController | PC | | `PC_MyController` |
| | PlayerState | PS | | `PS_MyState` |
| | Character | CHAR | | `CHAR_MyCharacter` |
| 蓝图 | Blueprint | BP | | `BP_MyActor` |
| | BlueprintGeneratedClass | BPI | | `BPI_MyInterface` |
| | BlueprintFunctionLibrary | BPFL | | `BPFL_MyLib` |
| | BlueprintMacroLibrary | BPML | | `BPML_MyMacro` |
| | UserDefinedEnum | E | | `E_MyEnum` |
| | UserDefinedStruct | F | | `F_MyStruct` |
| 网格 | StaticMesh | SM | | `SM_Chair` |
| | SkeletalMesh | SK | | `SK_Character` |
| 材质 | Material | M | | `M_Wood` |
| | MaterialInstance | MI | | `MI_Wood_Dark` |
| | MaterialInstanceConstant | MI | | `MI_Wood_Const` |
| | MaterialFunction | MF | | `MF_Blend` |
| | MaterialParameterCollection | MPC | | `MPC_Global` |
| | SubsurfaceProfile | SSP | | `SSP_Skin` |
| 动画 | AnimBlueprint | ABP | | `ABP_Character` |
| | AnimSequence | AS | | `AS_Walk` |
| | AnimMontage | AM | | `AM_Attack` |
| | AnimComposite | AC | | `AC_Combo` |
| | AimOffsetBlendSpace | AO | | `AO_Aim` |
| | BlendSpace | BS | | `BS_Locomotion` |
| | Skeleton | SKEL | | `SKEL_Character` |
| 音频 | SoundWave | S | | `S_Footstep` |
| | SoundCue | SC | | `SC_Ambient` |
| | SoundAttenuation | ATT | | `ATT_Default` |
| | SoundClass | SClass | | `SClass_Music` |
| | SoundMix | Mix | | `Mix_Default` |
| 特效 | ParticleSystem | PS | | `PS_Fire` |
| | NiagaraSystem | NS | | `NS_Smoke` |
| | NiagaraEmitter | NE | | `NE_Spark` |
| 纹理 | Texture2D | T | | `T_Wood_D` |
| | TextureCube | T | Cube | `T_Sky_Cube` |
| | TextureRenderTarget2D | RT | 2D | `RT_Scene_2D` |
| | TextureRenderTargetCube | RT | Cube | `RT_Reflect_Cube` |
| | TextureRenderTargetVolume | RT | Volume | `RT_Cloud_Volume` |
| | MediaTexture | MT | | `MT_Video` |
| UI | UserWidget | WBP | | `WBP_MainMenu` |
| | Font | Font | | `Font_Default` |
| | EditorUtilityWidget | EUW | | `EUW_MyTool` |
| AI | BehaviorTree | BT | | `BT_Enemy` |
| | BlackboardData | BB | | `BB_Enemy` |
| | BTDecorator | BTD | | `BTD_IsAlive` |
| | BTService | BTS | | `BTS_UpdateTarget` |
| | AIController | AIC | | `AIC_Enemy` |
| | EnvQuery | EQS | | `EQS_FindCover` |
| 数据 | DataTable | DT | | `DT_Items` |
| | DataAsset | DA | | `DA_Config` |
| | CurveFloat | Curve | Float | `Curve_Damage_Float` |
| | CurveVector | Curve | Vector | `Curve_Path_Vector` |
| | CurveLinearColor | Curve | Color | `Curve_Fade_Color` |
| 物理 | PhysicsAsset | PHYS | | `PHYS_Character` |
| | PhysicalMaterial | PM | | `PM_Metal` |
| Input | InputAction | IA | | `IA_Jump` |
| | InputMappingContext | IMC | | `IMC_Default` |
| Sequencer | LevelSequence | LS | | `LS_Intro` |
| | CameraAnimationSequence | CA | | `CA_Shake` |
| 关卡 | World | MAP | | `MAP_Level1` |
| 地形 | LandscapeLayerInfoObject | LL | | `LL_Grass` |
| | LandscapeGrassType | LG | | `LG_Meadow` |
| 植被 | FoliageType | FT | | `FT_Tree` |
| Paper2D | PaperSprite | SPR | | `SPR_Player` |
| | PaperFlipbook | FB | | `FB_Walk` |
| | PaperTileSet | TS | | `TS_Ground` |
| | PaperTileMap | TM | | `TM_Level1` |

---

## 2. 使用方法

### 2.1 自动重命名

| 选项 | 触发时机 |
|-----|---------|
| Auto Rename on Create | 创建或导入资产时自动重命名 |
| Auto Rename on Rename | 手动重命名资产后自动修正为标准格式 |

**示例**：创建蓝图 `MyCharacter` → 自动重命名为 `BP_MyCharacter`

### 2.2 右键批量重命名

**资产右键菜单**
1. 选中一个或多个资产
2. 右键 → **Auto Rename**

**文件夹右键菜单**
1. 右键点击文件夹
2. 选择 **Auto Rename All Assets**

### 2.3 智能处理策略

文件夹批量重命名采用三层递进策略：

| 阶段 | 条件 | 处理方式 |
|-----|------|---------|
| 批量快速 | 总数 >= 100 | 分成 10 批处理 |
| 失败重试 | 有批次失败 | 合并失败批次重试一轮 |
| 逐个精细 | 仍有失败 | 逐个处理，提供详细错误 |

总数 < 100 时直接进入逐个精细处理。

### 2.4 结果弹窗

完成后弹出结果窗口，包含三个标签：
- **Success**：成功重命名的资产
- **Error**：失败的资产及错误原因
- **Skipped**：跳过的资产及原因

**常见错误**：
| 错误信息 | 说明 |
|---------|------|
| Source control not connected | 源代码管理未连接 |
| Checked out by another user | 被他人 Checkout |
| File is read-only | 文件只读 |
| Target file already exists | 目标文件已存在 |
| Asset has unsaved changes | 有未保存的更改 |

---

## 3. 常见问题

**Q：重命名后资产引用会断吗？**

不会。使用 UE 官方 API，自动处理引用并创建重定向器。

**Q：可以撤销吗？**

可以，支持 Ctrl+Z 撤销。

**Q：为什么有些资产没有被重命名？**

1. 已经是标准名称
2. 没有配置该类型的命名规则
3. 路径被筛选规则排除
4. 文件只读且无法 Checkout

**Q：如何添加自定义规则？**

Settings → Asset Type Naming Rules → 点击 + 添加新规则。

---

## 作者

Copyright (c) 2025
作者：mengzhishanghun
邮箱：mengzhishanghun@outlook.com
