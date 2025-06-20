# 先查看当前的流有哪些

使用指令
```
p4 streams -a
```

![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/%E5%9B%BE%E7%89%87/Pasted%20image%2020250620122504.png)

test和Unreal Depot都是我要删除的Depot，区别是，test是完整的，而另一个则是先用stream -f -d 删除，结果被标记为deleted了，但是depot还是删除不了

# 强制删除

这里使用指令进行强制删除
```
p4 stream -d --obliterate -y -f //test/UEPublic/test1
```

![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/%E5%9B%BE%E7%89%87/Pasted%20image%2020250620122816.png)

这样就可以了，然后返回p4admin将Depot删除即可

# 提示has active clients; cannot delete until they are removed.

这个的意思是说还有一个工作区在用这个流，找到那个工作区删除或者切换到其他的流即可

---

![微信支付](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/PayCodes/WeChatPay.jpg)

> 📢 如果我的文章对您有所帮助，欢迎赞赏支持，让我有更多动力持续分享 🙏  
> 💼 业务合作 / Python 脚本 & UE 插件定制，请联系 ↓  
> 📧 [mengzhishanghun@outlook.com](mengzhishanghun@outlook.com)