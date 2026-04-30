from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system","你是一个诗人，可以作诗"),
        MessagesPlaceholder("history"),    #创建类对象，支持后续动态注入
        ("human","再来一首唐诗")
    ]
)

history_data = [
    ("human","你来写一首唐诗"),
    ("ai","窗前明月光，疑是地上霜，举头望明月，低头思故乡"),
    ("human","好诗，再来一首"),
    ("ai","锄禾日当午，汗滴禾下土，谁之盘中餐，粒粒皆辛苦")
]
# 使用to_string()方法从StringPromptValue变为string类型
prompt_text = chat_prompt_template.invoke({"history":history_data}).to_string()
model = ChatTongyi(model="tongyi-xiaomi-analysis-pro")
# res = model.invoke(prompt_text)
# print(res.content)

chain = chat_prompt_template | model
# 通过链调用invoke和stream方法
res = chain.invoke({"history":history_data})
print(res.content)

for chunk in chain.stream({"history":history_data}):
    print(chunk.content,end="",flush=True)