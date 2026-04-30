from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
# 本地调用
from langchain_ollama import ChatOllama
# 模型对象
# model = ChatTongyi(model="tongyi-xiaomi-analysis-pro")
model = ChatOllama(model="qwen3:4b")
# 准备消息列表
# 静态的
messages = [
    SystemMessage(content="你是一个唐诗作者"),
    HumanMessage(content="给我写一首唐诗"),
    AIMessage(content="北翎有燕，羽若雪兮，朔风哀哀，比翼南飞。朔风凛凛，一羽折兮，奈之若何。终不离兮"),  # 少样本
    HumanMessage(content="按照上面的回复格式，再写一首唐诗"),
]
# 简写版--动态的
"""
messages1 = [
    ("system","你是一个唐诗作者"),
    ("human","给我写一首唐诗"),
    ("ai","北翎有燕，羽若雪兮，朔风哀哀，比翼南飞。朔风凛凛，一羽折兮，奈之若何。终不离兮"),  # 少样本
    ("human","按照上面的回复格式，再写一首唐诗"),
]
"""

res = model.stream(input=messages)
for chunk in res:
    print(chunk.content,end="",flush=True)  # 聊天模型需要加入content筛选内容
