# Simple Asset Namer 使用教程

## 目录

1. [安装方法](#1-安装方法)
2. [快速开始](#2-快速开始)
3. [功能详解](#3-功能详解)
4. [配置选项](#4-配置选项)
5. [命名规则](#5-命名规则)
6. [使用场景示例](#6-使用场景示例)
7. [常见问题](#7-常见问题)
8. [注意事项](#8-注意事项)

---

## 1. 安装方法

### 方法一：直接安装（推荐）

1. 下载插件压缩包
2. 解压到项目的 `Plugins` 文件夹下
3. 重启 Unreal Editor
4. 插件会自动加载

```
YourProject/
├── Content/
├── Plugins/
│   └── SimpleAssetNamer/    <-- 放在这里
│       ├── Source/
│       └── SimpleAssetNamer.uplugin
└── YourProject.uproject
```

### 方法二：引擎插件安装

将插件放到引擎的插件目录下，所有项目都可以使用：

```
UnrealEngine/Engine/Plugins/Marketplace/SimpleAssetNamer/
```

### 验证安装

1. 打开 **Edit → Plugins**
2. 搜索 "Simple Asset Namer"
3. 确认插件已启用（Enabled）

---

## 2. 快速开始

### 2.1 打开设置面板

**Edit → Project Settings → Simple Asset Namer**

这里可以配置所有插件选项。

### 2.2 三种使用方式

#### 方式一：自动重命名（推荐新项目使用）

1. 在设置中勾选 **Auto Rename on Create**
2. 创建或导入资产时，插件会自动应用命名规则

**示例**：创建一个蓝图 `MyCharacter`，会自动重命名为 `BP_MyCharacter`

#### 方式二：右键批量重命名

1. 在 Content Browser 中选中一个或多个资产
2. 右键 → **Auto Rename**
3. 选中的资产会被重命名

#### 方式三：文件夹批量重命名

1. 在 Content Browser 左侧文件夹树中，右键点击文件夹
2. 选择 **Auto Rename All Assets**
3. 该文件夹下所有资产都会被重命名

---

## 3. 功能详解

### 3.1 自动重命名

当启用自动重命名后，以下情况会触发：

| 触发时机 | 配置项 | 说明 |
|---------|-------|------|
| 资产创建/导入 | Auto Rename on Create | 新建或导入资产时自动重命名 |
| 手动重命名资产 | Auto Rename on Rename | 用户手动重命名后自动修正 |

### 3.2 批量重命名

支持多种批量重命名方式：

**资产右键菜单**（精细模式）
- 选中任意数量的资产
- 右键 → Auto Rename
- 逐个处理并弹出详情弹窗

**文件夹右键菜单**（两种模式）

| 菜单项 | 说明 |
|-------|------|
| **Quick Rename All Assets** | 快速批量模式：动态分批处理，只显示通知，不弹窗 |
| **Rename All Assets (Detailed)** | 精细模式：逐个处理，弹出详细结果弹窗 |

⚠️ **警告**：大规模重命名会修改大量文件，请确保已备份项目或使用版本控制！

### 3.4 进度通知

批量操作时，右下角会显示进度通知：

```
[4/4] Renaming 45/100...
```

完成后会显示最终结果（绿色=成功，红色=有错误）

### 3.5 结果弹窗

批量重命名完成后，会弹出结果详情窗口（自动置顶显示）：

- **Success 标签**：显示成功重命名的资产列表
- **Error 标签**：显示失败的资产及具体错误原因
- **Skipped 标签**：显示跳过的资产及原因

**常见错误信息**：
| 错误信息 | 说明 |
|---------|------|
| Source control not connected | 源代码管理未正确连接 |
| Checked out by another user | 文件被其他用户 Checkout |
| Not at latest revision, sync required | 文件不是最新版本，需要同步 |
| Cannot checkout file | 无法 Checkout 文件 |
| File is read-only | 文件只读 |
| Target file already exists | 目标文件已存在 |
| Asset has unsaved changes | 资产有未保存的更改 |

### 3.6 源代码管理支持

插件自动处理版本控制：

| 环境 | 行为 |
|-----|------|
| Perforce | 自动 Checkout 需要修改的文件 |
| Git | 自动 Checkout 需要修改的文件 |
| 无版本控制 | 自动移除文件只读属性 |

---

## 4. 配置选项

打开 **Edit → Project Settings → Simple Asset Namer**

### 4.1 General（通用设置）

| 选项 | 说明 | 默认值 |
|-----|------|-------|
| Auto Rename on Create | 资产创建/导入时自动重命名 | true |
| Auto Rename on Rename | 手动重命名后自动修正 | true |
| Min Batch Size | 快速重命名最小批次大小（范围 10-100） | 10 |
| Max Batch Size | 快速重命名最大批次大小（范围 50-500） | 200 |

**批次大小说明**：

快速重命名模式使用动态批次大小：`批次大小 = 总资产数 / 20`，结果会被限制在 Min~Max 范围内。

例如：
- 100 个资产 → 批次大小 5 → 实际使用 MinBatchSize（10）
- 2000 个资产 → 批次大小 100 → 实际使用 100
- 10000 个资产 → 批次大小 500 → 实际使用 MaxBatchSize（200）

### 4.2 Filter（路径筛选）

控制哪些路径下的资产会被处理：

| 选项 | 说明 |
|-----|------|
| **None** | 不筛选，处理所有 /Game/ 下的资产 |
| **Blacklist** | 黑名单模式，排除指定路径 |
| **Whitelist** | 白名单模式，仅处理指定路径 |

**示例：黑名单模式**
```
Exclude Paths:
- /Game/ThirdParty
- /Game/Marketplace
```
以上路径的资产不会被重命名。

**示例：白名单模式**
```
Include Paths:
- /Game/MyProject
- /Game/Characters
```
只有以上路径的资产会被重命名。

### 4.3 Delimiter（分隔符设置）

| 选项 | 说明 | 默认值 |
|-----|------|-------|
| Delimiter | 生成名称时使用的分隔符 | `_` |
| Delimiter Detection List | 识别旧名称时的分隔符列表 | `_`, `-`, `.` |

**示例**：
- 输入：`bp-MyActor` 或 `bp.MyActor` 或 `bp_MyActor`
- 输出：`BP_MyActor`（使用配置的分隔符 `_`）

### 4.4 Legacy Affixes（旧词缀识别）

用于识别各种历史命名风格的词缀列表：

```
默认值：BP, bp, Blueprint, SM, sm, StaticMesh, M, m, Mat, Material...
```

这些词缀会被识别并替换为标准前后缀。

### 4.5 Asset Type Naming Rules（命名规则）

资产类型与命名规则的映射表：

| 资产类型 | 前缀 | 后缀 |
|---------|-----|------|
| Blueprint | BP | |
| StaticMesh | SM | |
| SkeletalMesh | SK | |
| Material | M | |
| MaterialInstance | MI | |
| Texture2D | T | |
| ... | ... | ... |

你可以在设置中自定义这些规则。

---

## 5. 命名规则

### 5.1 命名格式

标准命名格式：`前缀_核心名称_后缀`

**示例**：
| 原名称 | 重命名后 | 说明 |
|-------|---------|------|
| MyCharacter | BP_MyCharacter | 蓝图加 BP_ 前缀 |
| rock_mesh | SM_rock_mesh | 静态网格加 SM_ 前缀 |
| wood_material | M_wood_material | 材质加 M_ 前缀 |
| hero_skeleton | SK_hero_skeleton | 骨骼网格加 SK_ 前缀 |

### 5.2 完整规则列表

#### 蓝图类
| 资产类型 | 前缀 | 示例 |
|---------|------|------|
| Blueprint | BP | BP_MyActor |
| BlueprintInterface | BPI | BPI_Interactable |
| BlueprintFunctionLibrary | BPFL | BPFL_MathUtils |

#### 网格类
| 资产类型 | 前缀 | 示例 |
|---------|------|------|
| StaticMesh | SM | SM_Rock |
| SkeletalMesh | SK | SK_Character |

#### 材质类
| 资产类型 | 前缀 | 示例 |
|---------|------|------|
| Material | M | M_Wood |
| MaterialInstance | MI | MI_Wood_Dark |
| MaterialFunction | MF | MF_Blend |
| MaterialParameterCollection | MPC | MPC_Global |

#### 动画类
| 资产类型 | 前缀 | 示例 |
|---------|------|------|
| AnimBlueprint | ABP | ABP_Character |
| AnimSequence | AS | AS_Walk |
| AnimMontage | AM | AM_Attack |
| BlendSpace | BS | BS_Locomotion |

#### 音频类
| 资产类型 | 前缀 | 示例 |
|---------|------|------|
| SoundWave | S | S_Explosion |
| SoundCue | SC | SC_Footstep |
| SoundAttenuation | ATT | ATT_Default |

#### 特效类
| 资产类型 | 前缀 | 示例 |
|---------|------|------|
| ParticleSystem | PS | PS_Fire |
| NiagaraSystem | NS | NS_Smoke |
| NiagaraEmitter | NE | NE_Sparks |

#### 纹理类
| 资产类型 | 前缀 | 示例 |
|---------|------|------|
| Texture2D | T | T_Wood_D |
| TextureRenderTarget2D | RT | RT_SceneCapture |

#### UI 类
| 资产类型 | 前缀 | 示例 |
|---------|------|------|
| WidgetBlueprint | WBP | WBP_MainMenu |
| Font | Font | Font_Roboto |

#### AI 类
| 资产类型 | 前缀 | 示例 |
|---------|------|------|
| BehaviorTree | BT | BT_Enemy |
| BlackboardData | BB | BB_Enemy |
| BTDecorator | BTD | BTD_IsInRange |
| BTService | BTS | BTS_UpdateTarget |
| EnvironmentQuery | EQS | EQS_FindCover |

#### 数据类
| 资产类型 | 前缀 | 示例 |
|---------|------|------|
| DataTable | DT | DT_Items |
| DataAsset | DA | DA_GameConfig |
| CurveFloat | Curve | Curve_Damage |

---

## 6. 使用场景示例

### 场景一：新项目配置

**目标**：从项目开始就保持命名规范

**步骤**：
1. 打开 Project Settings → Simple Asset Namer
2. 勾选 **Auto Rename on Create**
3. 开始正常开发，所有新资产会自动规范命名

### 场景二：整理旧项目

**目标**：批量修正项目中的不规范命名

**步骤**：
1. 确保项目已备份或使用版本控制
2. 配置好路径筛选（如果只想处理特定文件夹）
3. 右键目标文件夹 → Auto Rename All Assets
4. 查看进度通知，确认结果

### 场景三：团队协作规范

**目标**：统一团队命名标准

**步骤**：
1. 在设置中配置好命名规则
2. 勾选 **Auto Rename on Create** 和 **Auto Rename on Rename**
3. 将配置文件（Config/DefaultGame.ini）提交到版本控制
4. 团队成员同步后，命名规则自动生效

### 场景四：只处理特定类型

**目标**：只重命名蓝图和材质，不动其他资产

**方法**：
1. 在 Asset Type Naming Rules 中只保留需要的类型
2. 删除其他类型的规则
3. 没有规则的资产类型不会被处理

---

## 7. 常见问题

### Q1：重命名后资产引用会断吗？

**不会**。插件使用 UE 官方的 `AssetTools.RenameAssets()` API，会自动处理所有引用，并创建重定向器（Redirector）。

### Q2：可以撤销重命名吗？

**可以**。重命名操作支持 UE 的 Undo 系统（Ctrl+Z）。但建议在大规模操作前备份项目。

### Q3：为什么有些资产没有被重命名？

可能原因：
1. 资产已经是标准名称
2. 资产类型没有配置命名规则
3. 资产路径被筛选规则排除
4. 资产文件只读且无法 Checkout

### Q4：支持 Perforce 吗？

**支持**。插件会自动检测并 Checkout 需要修改的文件。

### Q5：如何添加自定义命名规则？

在 Project Settings → Simple Asset Namer → Asset Type Naming Rules 中添加：
1. 点击 + 号添加新规则
2. 选择资产类型
3. 设置前缀和后缀

### Q6：重命名速度慢怎么办？

插件已做批量优化（100 个资产 = 1 次 API 调用）。如果仍然慢，可能是：
1. 资产数量过多，等待即可
2. Perforce 服务器响应慢
3. 资产需要加载到内存

---

## 8. 注意事项

### ⚠️ 重要提醒

1. **备份项目**：大规模重命名前，请确保已备份项目或提交版本控制
2. **路径限制**：插件只处理 `/Game/` 路径下的资产，不会影响引擎或插件资产
3. **重定向器**：重命名后会生成重定向器，建议定期清理（右键 → Fix Up Redirectors）

### 💡 最佳实践

1. 新项目建议开启自动重命名
2. 旧项目建议分批处理，而不是一次性全局重命名
3. 配置好筛选规则，避免处理第三方资产
4. 团队项目把配置提交到版本控制，保持规则一致

### 🔧 性能说明

- 插件使用批量 API，100 个资产只需 1 次调用
- Checkout 也是批量执行，不会触发多次 SCM 对话框
- 大项目（1000+ 资产）可能需要几秒到几十秒

---

## 作者

Copyright (c) 2025
作者：mengzhishanghun
邮箱：mengzhishanghun@outlook.com
