# SimpleConfigExclude 插件教程

可视化管理 Unreal Engine 项目打包时配置文件（.ini）的包含/排除规则。

---

## 配置说明

**位置**：编辑器 > 项目设置 > 插件 > Simple Config Exclude

### Settings 分类

#### Hide Plugin Config（隐藏插件配置）
- **默认值**：开启
- **作用**：在配置列表中隐藏 DefaultSimpleConfigExclude.ini
- **原因**：防止意外排除插件自身的设置文件

#### Clean Config Before Copy（复制前清理）
- **默认值**：开启
- **作用**：复制排除文件前，先删除目标目录下的 Config 文件夹
- **用途**：确保目标目录只包含最新的排除文件，避免残留旧文件

### Copy 分类

#### Copy Target Directory（复制目标目录）
- **默认值**：/Windows
- **作用**：指定复制排除配置文件的目标目录
- **路径格式**：相对于项目目录（如 `/Windows`、`/Build/Output`）
- **跨平台**：支持 Windows、Mac、Linux
- **目录结构**：复制时保持原有目录结构（`目标目录/项目名/Config/xxx.ini`）
- **Copy 按钮**：点击将所有标记为 Disallowed 的配置文件复制到目标目录

### Config Exclude Rules 分类

Config 文件夹中所有 .ini 文件的三态选择器：

| 策略 | 说明 |
|------|------|
| **Default** | 使用 UE 默认行为（通常根据文件类型决定是否打包） |
| **Allowed** | 强制允许打包（即使 UE 默认会排除） |
| **Disallowed** | 强制排除打包 |

#### Refresh Config List 按钮

点击重新扫描 Config 文件夹。使用场景：
- 添加了新的配置文件
- 删除了配置文件
- 列表与实际文件不同步

---

## 使用示例

### 示例 1：排除调试配置

如果你有一个 `DefaultDebugSettings.ini` 包含调试快捷键，不想打包到发布版本：

1. 打开项目设置 > 插件 > Simple Config Exclude
2. 在列表中找到 `Config/DefaultDebugSettings.ini`
3. 选择 "Disallowed"
4. 打包项目 - 该文件会被排除

### 示例 2：强制包含自定义配置

如果你有一个自定义配置 `DefaultCustomSettings.ini`，想确保一定被打包：

1. 打开插件设置
2. 找到 `Config/DefaultCustomSettings.ini`
3. 选择 "Allowed"
4. 打包项目 - 该文件会被强制打包

### 示例 3：复制排除文件到打包目录

打包后，你可能想手动添加被排除的配置文件到特定环境：

1. 设置 "Copy Target Directory" 为打包输出路径（如 `/Windows`）
2. 将需要排除的配置文件设置为 "Disallowed"
3. 打包项目
4. 点击 "Copy" 按钮
5. 文件会复制到 `Windows/YourProject/Config/xxx.ini`

---

## 重要说明

### 默认行为

所有配置文件默认处于 "Default" 状态，使用 UE 的默认打包行为。UE 会根据文件类型自动决定是否打包（如 engine.ini、game.ini、input.ini 等会被打包）。

### 插件配置保护

插件默认隐藏 `DefaultSimpleConfigExclude.ini`，因为：
- 它包含插件自身的设置
- 排除它可能导致插件功能异常
- 可以通过取消勾选 "Hide Plugin Config" 来显示它

### 设置持久化

- 插件设置保存在 `DefaultSimpleConfigExclude.ini`
- 排除规则保存在 `DefaultGame.ini` 的 `[Staging]` section
- 两个文件都应该提交到版本控制

### 复制前清理

开启 "Clean Config Before Copy" 时：
- 复制前会删除 `目标目录/项目名/Config/` 整个文件夹
- 然后只复制当前标记为 Disallowed 的文件
- 确保目标目录只包含最新状态

---

## 故障排除

### 文件不显示在列表中

1. 点击 "Refresh Config List" 按钮
2. 确保文件在 `Config` 文件夹或其子文件夹中
3. 确保文件有 `.ini` 扩展名

### 打包后规则没有生效

1. 检查 `DefaultGame.ini` 是否包含 `[Staging]` section
2. 尝试点击 "Refresh Config List"
3. 重启编辑器后再打包

### 插件配置显示在列表中

检查 "Hide Plugin Config" 设置，开启它来隐藏 DefaultSimpleConfigExclude.ini

### 复制后目标目录有多余文件

开启 "Clean Config Before Copy" 选项，复制前会清理目标 Config 文件夹

---

## 常见问题

**Q：这会影响游戏运行时吗？**
A：不会，这是仅编辑器插件，只影响打包过程。

**Q：支持子文件夹吗？**
A：支持，插件会递归扫描 Config 文件夹及其所有子文件夹，复制时保持原有目录结构。

**Q：排除的配置文件复制过去能用吗？**
A：取决于配置类型。运行时配置（如 Input）可以，编译时固化的配置（如渲染设置）不行。

---

## 支持

**邮箱**：mengzhishanghun@outlook.com

**报告问题时请包含**：
- Unreal Engine 版本
- 插件设置截图
- DefaultGame.ini 的 `[Staging]` section 内容
