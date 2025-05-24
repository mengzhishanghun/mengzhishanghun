## 简介

统一 C++ 和蓝图的日志输出格式，支持自定义格式和屏幕显示，便于调试与开发展示。

## 链接

[SimpleLogHelper | Fab](https://www.fab.com/zh-cn/listings/9e3442f9-3c0e-4454-abc4-205ab8e887ed)

## 特性

- 支持 Info / Warning / Error 三种日志级别
- 自定义格式模板（支持 `{LEVEL}`、`{TIME}`、`{CONTEXT}`、`{MESSAGE}` 占位符）
- 支持日志在屏幕显示，可配置颜色与显示时长
- 自动识别蓝图 / C++ 调用来源，蓝图中自动获取调用对象名称，C++ 中自动获取函数名
- 使用 `SIMPLE_LOG(...)` 宏在 C++ 中快速输出格式化日志
- 纯 C++ 编写，蓝图一键调用
- 适配 UE 5.2–5.5
- 支持全平台