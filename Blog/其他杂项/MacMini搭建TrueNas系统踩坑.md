# 环境说明
我的安装环境是Mac mini M4 16G 256G版本
利用*Homebrew*安装UTM软件，然后通过TrueNas镜像文件安装系统
分配128G空间和4核心 4G内存给Nas 
目标是将Nas打造成家用影音存储器以及我的代码管理器

# 踩坑记录
## 下载ISO
建议下载*TrueNas-Scale-Dragonfish 24.04.1*版本，因为在新版中取消了dm_mod支持，导致使用Mac Mini存储空间做虚拟系统盘时会报错。

## 显卡选择
UTM会默认不会选择使用QXL,而且注意是这个QXL，选错打不开
![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/%E5%9B%BE%E7%89%87/Pasted%20image%2020250617100218.png)

## 虚拟系统盘设置
系统创建的虚拟驱动器不是VirtIO接口，需要手动修改成这样，否则打不开
![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/%E5%9B%BE%E7%89%87/Pasted%20image%2020250617100257.png)

---

![微信支付](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/PayCodes/WeChatPay.jpg)

> 📢 如果我的文章对您有所帮助，欢迎赞赏支持，让我有更多动力持续分享 🙏  
> 💼 业务合作 / Python 脚本 & UE 插件定制，请联系 ↓  
> 📧 [mengzhishanghun@outlook.com](mengzhishanghun@outlook.com)