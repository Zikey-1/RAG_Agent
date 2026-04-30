"""
from langchain_community.llms.tongyi import Tongyi

# 这里需要使用llm-大语言模型
model = Tongyi(model="qwen-max")

result = model.invoke(input="你是谁？")
print(result)
"""


# 访问本地模型
from langchain_ollama import OllamaLLM

model1=OllamaLLM(model="qwen3:4b")

# res = model1.invoke(input="你是谁？")

# 流式输出 ，invoke和stream不同
res = model1.stream(input="你是谁?")
for chunk in res:
    print(chunk,end="",flush=True)

print(res)