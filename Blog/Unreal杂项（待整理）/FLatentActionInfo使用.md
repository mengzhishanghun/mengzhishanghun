```C++
FLatentActionInfo LatentActionInfo;
		LatentActionInfo.CallbackTarget = Subsystem;
		LatentActionInfo.ExecutionFunction = TEXT("HandleUnLoadStreamLevel");
		LatentActionInfo.UUID = FMath::Rand();
		LatentActionInfo.Linkage = 1;
```
CallbackTarget是Uobject指针
Function是object里的函数
UUID用来识别重复，可以随机生成或者直接指定
Linkage必须=1才能生效


---

![微信支付](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/PayCodes/WeChatPay.jpg)

> 📢 如果我的文章对您有所帮助，欢迎赞赏支持，让我有更多动力持续分享 🙏  
> 💼 业务合作 / Python 脚本 & UE 插件定制，请联系 ↓  
> 📧 [mengzhishanghun@outlook.com](mengzhishanghun@outlook.com)