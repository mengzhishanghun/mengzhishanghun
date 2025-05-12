# 什么是像素流送

[UE5.4像素流送](https://dev.epicgames.com/documentation/en-us/unreal-engine/getting-started-with-pixel-streaming-in-unreal-engine?application_version=5.4)

# 怎么使用

## 启用插件
![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/%E5%9B%BE%E7%89%87/Pasted%20image%2020240927114953.png)
开启PixelStreaming插件即可
## 添加启动参数 

>-AudioMixer -PixelStreamingIP=127.0.0.1 -PixelStreamingPort=8888 -PixelStreamingEncoderCodec=VP9

### 通过编辑器设置

![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/%E5%9B%BE%E7%89%87/Pasted%20image%2020240927113255.png)

编辑器偏好->播放->额外启动参数

注意事项：

1. 官方写的是-PixelStreamingIP=localhost，实测localhost不能使用，这里直接填127.0.0.1
2. 这种只会在独立模式下运行有效，可以通过上面的窗口设置修改默认独立窗口大小
3. 5.3视频编码流送只支持AV1 H264 VP8 VP9，5.4支持H265，这里建议使用VP9，适用性更广，三个4K屏幕也没问题，编码效率也高

### 通过快捷方式启动

这个就属于是老生常谈了，我就不加赘述了

## 启动信令服务器

### GitHub下载

[EpicGamesExt/PixelStreamingInfrastructure: The official Pixel Streaming servers and frontend. (github.com)](https://github.com/EpicGamesExt/PixelStreamingInfrastructure/)

![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/%E5%9B%BE%E7%89%87/Pasted%20image%2020240927115200.png)
直接去发布页面

找到与你引擎对应的版本下载即可，为什么要直接下发布版呢，因为这是以及编好可以直接使用的，要是直接下主干，或者分支版本，会提示缺少player.html文件

### Node下载安装

[Node.js — Download Node.js® (nodejs.org)](https://nodejs.org/en/download/prebuilt-installer/current)

下载后全默认安装即可

### 启动信令服务器

打开你下载的github文件->SignallingWebServer

打开cmd到这个路径下

执行指令即可
> node cirrus.js

![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/%E5%9B%BE%E7%89%87/Pasted%20image%2020240927115932.png)

成功后是这样

![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/%E5%9B%BE%E7%89%87/Pasted%20image%2020240927120124.png)

# 在网页端访问

直接在网页输入127.0.0.1即可，其他电脑输入IP即可

这里因为默认监听是80端口，所以可以省略，如果是其他端口需要显示修改






---

<p align="center">
  <img src="https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/PayCodes/WeChatPay.jpg" width="220"/>
</p>
> 如果我的文章对您有所帮助，欢迎赞赏支持，让我有更多动力持续分享 🙏   
> 💼 业务合作 / Python 脚本 & UE 插件定制 → [mengzhishanghun@outlook.com](mailto:mengzhishanghun@outlook.com)