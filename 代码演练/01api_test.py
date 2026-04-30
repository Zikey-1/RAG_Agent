from openai import OpenAI
import os

client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    # api_key="sk-be4c369a*****9929baf73caad8c34",
    #base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    base_url="http://localhost:11434/v1"
    # 如果使用ollama本地部署，改为--http://localhost:11434/v1
    # 并同步修改下面的model
)

messages = [{"role": "user", "content": "你是谁"}]
completion = client.chat.completions.create(
    # model="tongyi-xiaomi-analysis-pro",  # 您可以按需更换为其它深度思考模型
    model="qwen3:4b",
    messages=messages,
    # extra_body={"enable_thinking": True},
    stream=True
)
is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20)
for chunk in completion:
    delta = chunk.choices[0].delta
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20)
            is_answering = True
        print(delta.content, end="", flush=True)