```C++
void AMyDrivingReplayActor::AddInterp(const UStruct* ObjectClass)
{
	for (TFieldIterator<FProperty> It(ObjectClass); It; ++It)
	{
		It->SetPropertyFlags(CPF_Interp);
			
		if (const FStructProperty* AsStructProperty =  CastField<FStructProperty>(*It))
		{
			AddInterp(AsStructProperty->Struct);
		}
	}	
}
```

这里通过递归，将这个Actor内需要记录的结构体设置为了CPF_Interp，这个属性代表这个值能被LevelSequence记录，这个函数会遍历结构体内的所有属性，同样也设置为CPF_Interp

![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/%E5%9B%BE%E7%89%87/Pasted%20image%2020240905102943.png)

同时因为是在BeginPlay中才调用，他不会影响正常状态下得属性，只会在游戏开始时改变这部分属性

---

![微信支付](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/PayCodes/WeChatPay.jpg)

> 📢 如果我的文章对您有所帮助，欢迎赞赏支持，让我有更多动力持续分享 🙏  
> 💼 业务合作 / Python 脚本 & UE 插件定制，请联系 ↓  
> 📧 [mengzhishanghun@outlook.com](mengzhishanghun@outlook.com)