# agent

方法：create_agent

## 核心props

### 模型(model)

模型可以是静态的，也可以是动态的

```python
# 静态模型
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
agent = create_agent("openai:gpt-5.4", tools=tools) # 静态

model = ChatOpenAI(model="gpt-5.4",temperature=0.1,max_tokens=1000,timeout=30)
agent = create_agent(model, tools=tools) # 静态，更具体的模型参数
```

动态模型

```python
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse

basic_model = ChatOpenAI(model="gpt-5.4-mini")
advanced_model = ChatOpenAI(model="gpt-5.4")

@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """根据对话选择模型"""
    message_count = len(request.state["messages"])
    if message_count > 10:
        # Use an advanced model for longer conversations
        model = advanced_model
    else:
        model = basic_model

    return handler(request.override(model=model))

agent = create_agent(model=basic_model,tools=tools,middleware=[dynamic_model_selection])
```

### 工具(tools)

工具使用@tool装饰器，可传参：description等

#### 动态工具：

动态工具分为两种:

1. 工具传入是静态，使用是动态（根据store/state/context）

- 使用中间件@wrap_model_call装饰器
- 在中间件方法获取状态：`request.state`(获取消息等信息)、`request.runtime.context`(获取上下文)、`request.runtime.store`
- 获取创建时传入的tool: `request.tools`
- 修改tools： `request.override(tools=new_tools)`
- `return handler(request)`

2. 工具在运行时动态注入：

- 创建class类中间件，继承`AgentMiddleware`
- 类中实现钩子方法 `wrap_model_call`
- 类中实现钩子方法 `wrap_tool_call`

#### 工具错误

- 用`@wrap_tool_call`装饰器创建中间件
- 捕获异常，return 一个 ToolMessage

### system prompt(system_prompt)

- 可以直接传递给 create_agent，参数：system_prompt: str | SystemMessage
- 动态提示词：使用`@dynamic_prompt`创建中间件，根据条件return str_prompt(可以根据用户角色返回不同prompt)

### 高级props

#### 结构化输出(response_format)

- ToolStrategy
  `response_format=ToolStrategy(ContactInfo)`

- ProviderStrategy: 使用模型提供商自身的结构化输出功能，仅限实现了的模型

#### 记忆

messages为短期记忆，用户可自定义状态

自定义状态：

1. 在agent.invoke中传入的都为状态
2. 状态的定义：使用中间件，或者props.`state_schema`，需要继承AgentState as TypeDict

#### stream方法

agent.stream：可以流式返回结果

#### 中间件
