# 🔄 SimpleByteConversion 插件简介（适用于 Unreal Engine）

**SimpleByteConversion** 是一款为 Unreal Engine 开发者量身打造的 **蓝图字节转换工具插件**，支持常见基本类型（如整型、浮点型、布尔、字符串、结构体）与字节数组之间的相互转换。适用于网络通信、序列化、数据打包等多种场景。

---

# ✨ 插件功能特性

|支持类型|可用函数|
|---|---|
|`int32`|`IntToBytes` / `BytesToInt`|
|`int64`|`Int64ToBytes` / `BytesToInt64`|
|`float`|`FloatToBytes` / `BytesToFloat`|
|`double`|`DoubleToBytes` / `BytesToDouble`|
|`bool`|`BoolToBytes` / `BytesToBool`|
|`FString`|`StringToBytes` / `BytesToString`|
|任意 `Struct`（结构体）|`StructToBytes` / `BytesToStruct`（支持自定义结构体）|

> ✅ 所有函数均为 **纯蓝图节点**，可直接使用于 Blueprint 项目中，无需 C++ 编码。

---

# 📦 插件用途举例

- 网络传输前将数据转为 `ByteArray` 格式，便于打包发送
    
- 接收网络消息后，将 `ByteArray` 恢复为原始结构体或数值
    
- 在数据存档、数据校验、二进制解析等场景中高效使用
    

---

# 💡 技术亮点

- 🧩 **支持任意结构体序列化与反序列化**（使用 UE 的 `CustomThunk` 支持）
    
- 🔁 双向转换，保证数据完整性与兼容性
    
- 🎮 适配 Unreal Engine **5.2 ~ 5.5**
    
- 🧰 插件体积轻巧，**不依赖任何第三方库**
    
- ⚙️ 蓝图自动补全，适合纯蓝图项目或跨平台项目中使用
    

---

# 🛒 插件购买地址（Fab 官方商城）

📦 [SimpleByteConversion | Fab](https://www.fab.com/zh-cn/listings/ee68b12e-30b4-4904-8f80-3cc43c1e6002)

---

# 📬 联系作者

📧 **邮箱**：mengzhishanghun@outlook.com  
如有任何问题、功能建议，或需要 **定制 Unreal Engine 插件 / Python 脚本开发**，欢迎随时联系！

---

<p align="center">
  <img src="https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/PayCodes/WeChatPay.jpg" width="220"/>
</p>
> 如果我的文章对您有所帮助，欢迎赞赏支持，让我有更多动力持续分享 🙏   
> 💼 业务合作 / Python 脚本 & UE 插件定制 → [mengzhishanghun@outlook.com](mailto:mengzhishanghun@outlook.com)