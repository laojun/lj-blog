# 模型

## 使用

传给create_agent(可以动态)
单独使用

使用方式：
`init_chat_model`：可以定义更多详细参数，比如速率等

供应商提供的，如`ChatOpenAI`

**_对于深度思考的模型，比如deepseek-reasoner，使用该API，无法得到reasoning_content，需要自己包装取得_**

## 方法

- model.invoke
- model.stream
- model.batch(批量处理用户问题)

## 使用工具: model.bind_tools([tool1, tool2])

## 结构化输出：model.with_structured_output(MyModel)
