说说我的方法吧，不知道正不正确，但是能用，哈哈哈哈，跟着官方的第三方库弄的
![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/00-%E9%99%84%E4%BB%B6%E8%B5%84%E6%BA%90/%E5%9B%BE%E7%89%87/Pasted%20image%2020240523184325.png)
打包dll那一套我就不赘述了，就说说拿到DLL和Lib怎么办
以官方模板创建得插件TestThird为例
将dll，lib文件放到`TestThird\Source\ThirdParty\TestThirdLibrary\x64\Release
然后在`TestThird\Binaries\ThirdParty\TestThirdLibrary\Win64`放个dll
这步理论上可以优化例如自动复制，不过还没时间看
添加之后在模块Build.cs中添加
![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/00-%E9%99%84%E4%BB%B6%E8%B5%84%E6%BA%90/%E5%9B%BE%E7%89%87/Pasted%20image%2020240523184539.png)
最后在模块中添加一个跟dll同名的.h文件，用来声明dll中可以调用的函数
![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/00-%E9%99%84%E4%BB%B6%E8%B5%84%E6%BA%90/%E5%9B%BE%E7%89%87/Pasted%20image%2020240523184544.png)
如果你不知道DLL中有哪些函数，下载这个软件[Dependencies](https://github.com/lucasg/Dependencies)
![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/00-%E9%99%84%E4%BB%B6%E8%B5%84%E6%BA%90/%E5%9B%BE%E7%89%87/Pasted%20image%2020240523184622.png)

把DLL拖进去就能看，很方便
最后在模块加载的时候，需要调用FPlatformProcess::GetDllHandle，我这里自己修改了一下，大概就是
这样,这里别照抄，为了展示临时改的，其实是要通过windll,macdll,linuxdll传入
![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/00-%E9%99%84%E4%BB%B6%E8%B5%84%E6%BA%90/%E5%9B%BE%E7%89%87/Pasted%20image%2020240523184647.png)
模块卸载的时候别忘了调用FPlatformProcess::FreeDllHandle
![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/00-%E9%99%84%E4%BB%B6%E8%B5%84%E6%BA%90/%E5%9B%BE%E7%89%87/Pasted%20image%2020240523184654.png)
现在可以调用了，调用起来就很方便，包含一下头文件正常调用即可
![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/00-%E9%99%84%E4%BB%B6%E8%B5%84%E6%BA%90/%E5%9B%BE%E7%89%87/Pasted%20image%2020240523184659.png)

参考文档[将第三方库整合进虚幻引擎 | 虚幻引擎 5.4 文档 | Epic Developer Community (epicgames.com)](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/integrating-third-party-libraries-into-unreal-engine)

---

<p align="center">
  <img src="https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/PayCodes/WeChatPay.jpg" width="220"/>
</p>
> 如果我的文章对您有所帮助，欢迎赞赏支持，让我有更多动力持续分享 🙏   
> 💼 业务合作 / Python 脚本 & UE 插件定制 → [mengzhishanghun@outlook.com](mailto:mengzhishanghun@outlook.com)