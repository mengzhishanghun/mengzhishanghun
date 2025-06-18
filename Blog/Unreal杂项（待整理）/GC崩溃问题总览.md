# Disregard for GC object A referencing B which is not part of root set

![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/%E5%9B%BE%E7%89%87/Pasted%20image%2020240607152219.png)

这个问题比较好处理，锁定A的类，之中有声明B的地方，将B用弱指针TWeakObjectPtr包裹即可
这个问题的原因可能是因为A是免除GC的类，所以中间不能有通过UPROPERTY声明变量来免除GC



---

![微信支付](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/PayCodes/WeChatPay.jpg)

> 如果我的文章对您有所帮助，欢迎赞赏支持，让我有更多动力持续分享 🙏  
> 💼 业务合作 / Python 脚本 & UE 插件定制  
> 📧 [mengzhishanghun@outlook.com](mengzhishanghun@outlook.com)