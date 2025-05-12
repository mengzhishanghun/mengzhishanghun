# 第一步，声明枚举
```C++
/**  
 * Mode 
 */
UENUM(BlueprintType)  
enum class EDrivingMode : uint8  
{  
    None UMETA(DisplayName = "None")  
};  
  
/**  
 * Status 
 */
UENUM(BlueprintType)  
enum class EDrivingStatus : uint8  
{  
    None UMETA(DisplayName = "None")  
};
```

如上，先要声明枚举的名字

# 第二部，配置枚举
```C++
UCLASS(config = Game, defaultconfig)  
class MYDEMO_API UMyDrivingTestSettings : public UDeveloperSettings  
{  
    GENERATED_BODY()  
public:  
    UPROPERTY(config, EditAnywhere, BlueprintReadOnly)  
    bool EnableSubsystem = true;  
  
    UPROPERTY(config, EditAnywhere, BlueprintReadOnly)  
    TSoftObjectPtr<UMyDrivingTestDataAsset> DrivingTestDataAsset;  
  
    UPROPERTY(config, EditAnywhere, BlueprintReadOnly)  
    TArray<FString> DrivingProjectEnum;  
  
    UPROPERTY(config, EditAnywhere, BlueprintReadOnly)  
    TArray<FString> DrivingSubjectEnum;  
  
    UPROPERTY(config, EditAnywhere, BlueprintReadOnly)  
    TArray<FString> DrivingModeEnum;  
  
    UPROPERTY(config, EditAnywhere, BlueprintReadOnly)  
    TArray<FString> DrivingStatusEnum;  
  
    UPROPERTY(config, EditAnywhere, BlueprintReadOnly)  
    TArray<FString> DrivingScoreEnum;  
  
    UPROPERTY(config, EditAnywhere, BlueprintReadOnly)  
    TArray<FString> DrivingScoreTextTypeEnum;  
  
    UPROPERTY(config, EditAnywhere, BlueprintReadOnly)  
    TArray<FString> DrivingShowTextTypeEnum;  
  
    UPROPERTY(config, EditAnywhere, BlueprintReadOnly)  
    TArray<FString> DrivingCustomDelegateEnum;  
};
```

我们需要在编辑器里配置枚举的值，这样才能在蓝图中使用

# 第三步，在编辑子系统中处理枚举
```C++
UCLASS()  
class MYDEMO_API UMyDrivingTestEditorSubsystem : public UEditorSubsystem  
{  
    GENERATED_BODY()  
public:  
    UMyDrivingTestEditorSubsystem(){};  
  
    virtual bool ShouldCreateSubsystem(UObject* Outer) const override { return true; }  
  
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;  
  
    virtual void Deinitialize() override{}  
};

static void DynamicInitEnum(UEnum* DynamicEnum, TArray<FString> EnumArray, bool AddNone = true, bool AddMax = false)  
{  
    if(DynamicEnum == nullptr) return;  
    TArray<TPair<FName, int64>> EnumNameArray;  
    int64 CurEnumIndex = 0;  
    if(AddNone)  
    {      
	    EnumNameArray.Emplace(TPairInitializer<FName, int64>(FName(*DynamicEnum->GenerateFullEnumName(*FString("None"))), CurEnumIndex++));  
    }    
    for(auto It : EnumArray)  
    {      
		if(It.IsEmpty()) continue;  
		EnumNameArray.Emplace(TPairInitializer<FName, int64>(FName(*DynamicEnum->GenerateFullEnumName(*It)), CurEnumIndex++));  
    }    
    if(AddMax)  
    {      
		EnumNameArray.Emplace(TPairInitializer<FName, int64>(FName(*DynamicEnum->GenerateFullEnumName(*FString("Max"))), CurEnumIndex++));  
    }    
    DynamicEnum->SetEnums(EnumNameArray, DynamicEnum->GetCppForm());  
}
```
这里是创建动态枚举的核心，他会直接覆盖之前的枚举，在编辑子系统下执行的好处就是他优先于蓝图的构造，使得枚举可以在蓝图中正常使用，当然若枚举要在C++中使用也可以强转为int32使用


```C++
#define DYNAMICINITENUMONSETTINGSCHANGE(EnumType, EnumName) \  
if(PropertyChangedEvent.GetPropertyName() == #EnumName)\  
{\  
    DynamicInitEnum(StaticEnum<EnumType>(), DrivingTestSettings->EnumName);\  
}  
  
void UMyDrivingTestEditorSubsystem::Initialize(FSubsystemCollectionBase& Collection)  
{  
    Super::Initialize(Collection);  
  
    UMyDrivingTestSettings* MyDrivingTestSettings = GetMutableDefault<UMyDrivingTestSettings>();  
    MyDrivingTestSettings->OnSettingChanged().AddLambda([](UObject* Object, FPropertyChangedEvent& PropertyChangedEvent)  
    {       
    UMyDrivingTestSettings const* DrivingTestSettings = GetDefault<UMyDrivingTestSettings>();  
       DYNAMICINITENUMONSETTINGSCHANGE(EDrivingProject,DrivingProjectEnum);  
       DYNAMICINITENUMONSETTINGSCHANGE(EDrivingSubject, DrivingSubjectEnum);  
       DYNAMICINITENUMONSETTINGSCHANGE(EDrivingMode, DrivingModeEnum);  
       DYNAMICINITENUMONSETTINGSCHANGE(EDrivingStatus, DrivingStatusEnum);  
       DYNAMICINITENUMONSETTINGSCHANGE(EDrivingScore, DrivingScoreEnum);  
       DYNAMICINITENUMONSETTINGSCHANGE(EDrivingScoreTextType, DrivingScoreTextTypeEnum);  
       DYNAMICINITENUMONSETTINGSCHANGE(EDrivingShowTextType, DrivingShowTextTypeEnum);  
       DYNAMICINITENUMONSETTINGSCHANGE(EDrivingSimpleCustomDelegateType, DrivingCustomDelegateEnum);  
    });    
    DynamicInitEnum(StaticEnum<EDrivingProject>(), MyDrivingTestSettings->DrivingProjectEnum);  
    DynamicInitEnum(StaticEnum<EDrivingSubject>(), MyDrivingTestSettings->DrivingSubjectEnum);  
    DynamicInitEnum(StaticEnum<EDrivingMode>(), MyDrivingTestSettings->DrivingModeEnum);  
    DynamicInitEnum(StaticEnum<EDrivingStatus>(), MyDrivingTestSettings->DrivingStatusEnum);  
    DynamicInitEnum(StaticEnum<EDrivingScore>(), MyDrivingTestSettings->DrivingScoreEnum);  
    DynamicInitEnum(StaticEnum<EDrivingScoreTextType>(), MyDrivingTestSettings->DrivingScoreTextTypeEnum);  
    DynamicInitEnum(StaticEnum<EDrivingShowTextType>(), MyDrivingTestSettings->DrivingShowTextTypeEnum);  
    DynamicInitEnum(StaticEnum<EDrivingSimpleCustomDelegateType>(), MyDrivingTestSettings->DrivingCustomDelegateEnum);  
}
```

# 注意
经过打包实验，这里把编辑子系统EditorSubsystem替换成引擎子系统EngineSubsystem这样打包不需要修改

---

<p align="center">
  <img src="https://raw.githubusercontent.com/mengzhishanghun/mengzhishanghun/main/PayCodes/WeChatPay.jpg" width="220"/>
</p>
> 如果我的文章对您有所帮助，欢迎赞赏支持，让我有更多动力持续分享 🙏   
> 💼 业务合作 / Python 脚本 & UE 插件定制 → [mengzhishanghun@outlook.com](mailto:mengzhishanghun@outlook.com)