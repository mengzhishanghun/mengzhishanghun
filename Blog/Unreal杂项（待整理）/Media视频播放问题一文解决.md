# MOV播放
原生UE播放器不支持MOV视频，需要安装两个插件
![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/%E5%9B%BE%E7%89%87/Pasted%20image%2020240722165101.png)
# 解决视频播放一帧残留
## 解决方案
![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/%E5%9B%BE%E7%89%87/Pasted%20image%2020240530161047.png)
如图，在MediaTexture中勾选AutoClear自动清理，并且将ClearColor的A通道设置为0

![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/%E5%9B%BE%E7%89%87/Pasted%20image%2020240530161442.png)
然后在创建的材质中，将材质混合模式修改为蒙板，将MediaTexture的A通道连接到蒙板输出即可

## 个人猜测
以下代码截图为UE5.3非源码版截图

![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/%E5%9B%BE%E7%89%87/Pasted%20image%2020240530162139.png)



如图，当勾选自动清理后，会检测清理颜色是否不同，再以清理颜色清理纹理

这里的纹理当然是指MediaTexture

这里的CurrentClearColor断点显示为0，0，0，1（断点很频繁，不能准确保证）

当把清理颜色的A设置为0时，MediaTexture在清理时的透明度就是0，所以咱们在材质中需要将A连接到蒙板，这样在清理时播放器是透明的，从而解决残留上一个视频最后一帧的问题

## 重要更新

刚发现这个办法还是无法完全消除残留，特地又研究了一下，发现在MediaTexture中有个UpdateTexture函数对蓝图开放，如图
![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/%E5%9B%BE%E7%89%87/Pasted%20image%2020240717150724.png)
所以要想完全消除残留还有一步，要在关闭或打开Media的时候给MediaTexture执行UpdateTexture函数，如图
![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/%E5%9B%BE%E7%89%87/Pasted%20image%2020240717150732.png)
开心o(*￣▽￣*)ブ完结散花！

# 修复视频循环播放时不会从0开始的问题
UE视频播放本身有的问题，需要安装一个ElectraPlayer插件来解决

# 视频直接通过OpenSource后play失败的原因

调用太快视频还没有加载出来，加个延迟或者在视频加载成功委托后再执行play


---

<p align="center">
  <img src="https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/PayCodes/WeChatPay.jpg" width="220"/>
</p>
> 如果我的文章对您有所帮助，欢迎赞赏支持，让我有更多动力持续分享 🙏   
> 💼 业务合作 / Python 脚本 & UE 插件定制 → [mengzhishanghun@outlook.com](mailto:mengzhishanghun@outlook.com)