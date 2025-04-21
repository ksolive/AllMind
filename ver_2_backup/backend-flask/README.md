# 核心后端部分

[x] 基础对话
[ ] session管理
[ ] 配置管理

## 基础对话

使用openai api进行对话

## session管理

使用flask的session管理用户的对话历史，这种实现有问题，因为以pywebview为前端的话，每次启动都是一个新的session

## 配置管理

配置包含

* 模型
  * key
  * topk
  * temperature
  * max_tokens
  * 其他的模型参数
* 显示内容
  * debug mode
  * token数
* 插件相关
  * 