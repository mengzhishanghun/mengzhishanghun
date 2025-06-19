# 问题简述

通常情况下，当你新建一个蓝图继承自UObejct的时候，你会发现不仅不能获取到PlayerController

![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/Pasted%20image%2020250615205900.png)

也不能够创建UI，否则会报错

![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/Pasted%20image%2020250615205934.png)

造成这个的原因是因为父类里没有重写GetWorld这个函数，导致蓝图编译时拿不到上下文，引发报错。

# 解决方案

知道问题的原因后就不难解决这个问题，只需要在父类中重写GetWorld函数即可，但是有几点需要注意

在.h中添加
```C++
virtual UWorld* GetWorld() const override;
```

在.cpp中添加

```C++
UWorld* UAIFlow::GetWorld() const  
{  
    if (IsTemplate() || !GetOuter())  
    {  
       return nullptr;  
    }  
  
    return GetOuter()->GetWorld();  
}
```

注意这里不能直接return，这样并不能直接解决问题，必须要这样写才可以。

这里因为我是在Actor中创建的对象，所以GetOuter直接指向那个Actor，所以我能正确拿到GetWorld，所以return这里需要根据情况自己写。

---

![微信支付](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/PayCodes/WeChatPay.jpg)

> 📢 如果我的文章对您有所帮助，欢迎赞赏支持，让我有更多动力持续分享 🙏  
> 💼 业务合作 / Python 脚本 & UE 插件定制，请联系 ↓  
> 📧 [mengzhishanghun@outlook.com](mengzhishanghun@outlook.com)