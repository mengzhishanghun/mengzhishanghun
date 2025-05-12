在c++中

# 灵活使用软链接和硬链接

声明类类型可以使用TSubclassOf，类对象使用TObjectPtr，但这是硬链接

如果要使用软链接，可以考虑TSoftObjectPtr和TSoftClassPtr，其中

TSoftObjectPtr一般用于资源加载，可以代替TObjectPtr使用

TSoftClassPtr一般用于UClass类加载，这个获取出来是个Uclass*,可以代替TSubclassOf使用

# 如何实例化一个UObject并在属性表中配置

在类的UCLASS中添加EditInlineNew如下

![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/00-%E9%99%84%E4%BB%B6%E8%B5%84%E6%BA%90/%E5%9B%BE%E7%89%87/Pasted%20image%2020240309153657.png)
在引用类的时候，在UPROPERTY中添加Instanced，当然别忘了EditAnywhere，不然无法编辑

![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/00-%E9%99%84%E4%BB%B6%E8%B5%84%E6%BA%90/%E5%9B%BE%E7%89%87/Pasted%20image%2020240309153755.png)

# 类属性后加CollapseCategories

CollapseCategories的作用是不显示类内属性的所属类，这样看着整个配置就是一体的感觉

# 如何在UObject蓝图中调用需要世界上下文的静态函数

有两个方法
## 在类的UCLASS中添加meta=(ShowWorldContextPin)

![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/00-%E9%99%84%E4%BB%B6%E8%B5%84%E6%BA%90/%E5%9B%BE%E7%89%87/Pasted%20image%2020240309155742.png)

## 在静态函数的UFUNCTION中添加CallableWithoutWorldContext

![](https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/Blog/Assets/00-%E9%99%84%E4%BB%B6%E8%B5%84%E6%BA%90/%E5%9B%BE%E7%89%87/Pasted%20image%2020240309155736.png)






---

<p align="center">
  <img src="https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/PayCodes/WeChatPay.jpg" width="220"/>
</p>
> 如果我的文章对您有所帮助，欢迎赞赏支持，让我有更多动力持续分享 🙏   
> 💼 业务合作 / Python 脚本 & UE 插件定制 → [mengzhishanghun@outlook.com](mailto:mengzhishanghun@outlook.com)