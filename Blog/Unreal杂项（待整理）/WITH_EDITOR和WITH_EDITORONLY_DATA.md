这两个宏用来分割编辑器代码和游戏代码

用*WITH_EDITOR*或*WITH_EDITORONLY_DATA*包裹的部分在打包的时候不会打进去

*WITH_EDITORONLY_DATA*算是*WITH_EDITOR*的进位，因为*WITH_EDITORONLY_DATA*可以包裹*UFNUNCTION*和*UPROPERTY*，而*WITH_EDITOR*包裹时会报错

但是函数声明为编辑器函数之后就不能在正常的蓝图被调用了，不知道是哪个版本做的更改，狗日的UE

目前的解决办法是
![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/%E5%9B%BE%E7%89%87/Pasted%20image%2020240605175636.png)
创建EditorUtilityActor等类型的Editor类，只有这种类里才能调用EditorFunction

如果后面有更好的办法会回来更新


---

<p align="center">
  <img src="https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/PayCodes/WeChatPay.jpg" width="220"/>
</p>
> 如果我的文章对您有所帮助，欢迎赞赏支持，让我有更多动力持续分享 🙏   
> 💼 业务合作 / Python 脚本 & UE 插件定制 → [mengzhishanghun@outlook.com](mailto:mengzhishanghun@outlook.com)