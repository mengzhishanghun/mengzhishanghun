# 🔐 SimpleSSHTunnel 插件简介（适用于 Unreal Engine）

**SimpleSSHTunnel** 是一款专为 Unreal Engine 蓝图项目开发的 **SSH 隧道连接插件**，允许开发者在不编写任何 C++ 代码的前提下，通过蓝图快速创建、管理和关闭 SSH 隧道连接。它适用于希望从 UE 内部访问远程服务、数据库、内网 API 或调试服务器的项目。

---

# ✨ 插件亮点

- ✅ **全蓝图接口封装**，无需写 C++ 代码即可操作
- 🔁 **支持多条 SSH 隧道同时管理**，通过名称索引
- ⚙️ **支持 DeveloperSettings 参数配置**，可一键修改连接信息
- 🧵 **使用后台线程非阻塞连接**，稳定可靠
- 🧩 **日志反馈友好**，便于排查连接异常或权限问题
- 🎯 适配 Unreal Engine 5.2 ~ 5.5，支持 Windows 平台

---

# 🔧 适用场景

- 在蓝图项目中连接远程 API 或数据库
- 通过 SSH 转发端口访问内网服务
- 调试部署在远程 Linux 服务器上的模型、游戏服务
- 教学、科研或跨区域项目的远程控制支持

---

# 📚 所用第三方库

SimpleSSHTunnel 插件基于以下开源组件构建：

|第三方库|用途|
|---|---|
|**libssh2**|实现 SSH 协议（包括用户认证、端口转发）|
|**OpenSSL**|提供底层加密支持，用于密钥交换和安全连接|

---

# 🧩 核心功能

|功能名称|描述|
|---|---|
|🔌 **蓝图创建 SSH 隧道**|提供 `CreateSSHTunnel(TunnelName)` 蓝图节点，支持一键启动指定名称的 SSH 隧道|
|🧪 **检查隧道是否运行**|提供 `CheckSSHTunnelIsRunning(TunnelName)` 蓝图节点，可判断某隧道是否已启动|
|🔐 **关闭指定隧道**|提供 `CloseSSHTunnel(TunnelName)` 蓝图节点，关闭某条 SSH 隧道并释放资源|
|🚫 **关闭全部隧道**|提供 `CloseAllSSHTunnel()` 蓝图节点，关闭当前所有已启动的 SSH 隧道|
|⚙️ **多隧道管理**|使用 `TMap<FString, FRunnableThread*>` 实现多条 SSH 隧道并发管理，通过名称索引控制|

---

# ⚙️ 使用方式与配置

- **支持通过 DeveloperSettings 配置连接参数**（通过 `USimpleSSHTunnelSettings::SSHTunnelPresets` 读取）
- 每个连接包含的参数类型为 `FSimpleSSHTunnelParams`，包括主机地址、端口、用户名、密码/密钥等（详见结构体定义）
- 使用 `FRunnableThread` 后台运行 SSH 隧道线程，确保非阻塞、异步执行

---

# 📘 蓝图接口汇总

|蓝图节点|说明|
|---|---|
|`CreateSSHTunnel(TunnelName)`|创建 SSH 隧道|
|`CheckSSHTunnelIsRunning(TunnelName)`|判断某隧道是否正在运行|
|`CloseSSHTunnel(TunnelName)`|关闭某条隧道|
|`CloseAllSSHTunnel()`|一键关闭所有隧道连接|

---
# 🛒 插件购买地址（Fab 官方商城）

📦 **购买链接**：[SimpleSSHTunnel | Fab](https://www.fab.com/zh-cn/listings/e86019ed-6e80-4f14-b70c-1fb2f0154721)

---
### 📬 联系作者

📧 **邮箱**：mengzhishanghun@outlook.com  
如有任何问题、功能建议，或需要 **定制 Unreal Engine 插件 / Python 脚本**，欢迎随时联系！

---

![微信支付](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/PayCodes/WeChatPay.jpg)

> 如果我的文章对您有所帮助，欢迎赞赏支持，让我有更多动力持续分享 🙏  
> 💼 业务合作 / Python 脚本 & UE 插件定制  
> 📧 [mengzhishanghun@outlook.com](mengzhishanghun@outlook.com)