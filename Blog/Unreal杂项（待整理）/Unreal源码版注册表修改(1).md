# bat指令
创建一个bat文件，输入以下指令
```
set str=%~dp0
set name=%~n0
REG ADD "HKCU\SOFTWARE\Epic Games\Unreal Engine\Builds" /v "%name%" /t REG_SZ  /f /d "%str:~0,-1%"
```
这个脚本会把当前路径下的虚幻源码添加到注册表，名字就是这个脚本的命名
这样做的好处是统一源码的.uproject文件版本号
![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/01-%E5%9B%BE%E7%89%87/Pasted%20image%2020240710163255.png)
这样做的好处是可以防止每台电脑源码引擎的注册表名字不同导致的.uproject不同，而重新编译

## bat指令更新
```bat
@echo off
setlocal

REM 设置当前批处理脚本的路径并去掉最后的反斜杠
set str=%~dp0
set str=%str:~0,-1%
set name=%~n0
set key=HKCU\SOFTWARE\Epic Games\Unreal Engine\Builds

REM 查找并删除所有数据值等于 %str% 的项
for /f "tokens=1" %%i in ('REG QUERY "%key%" /f "%str%"') do (
    echo %%i
    REG DELETE "%key%" /v "%%i" /f
)

REG ADD "%key%" /v "%name%" /t REG_SZ  /f /d "%str%"

endlocal
```
新增功能删除所有值等于当前文档的数据，不然会出现添加不上的问题

---

<p align="center">
  <img src="https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/PayCodes/WeChatPay.jpg" width="220"/>
</p>
> 如果我的文章对您有所帮助，欢迎赞赏支持，让我有更多动力持续分享 🙏   
> 💼 业务合作 / Python 脚本 & UE 插件定制 → [mengzhishanghun@outlook.com](mailto:mengzhishanghun@outlook.com)