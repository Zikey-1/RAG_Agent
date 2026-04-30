from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

str_parser = StrOutputParser()
myfunc = RunnableLambda(lambda ai_msg:{"name":ai_msg.content})

model = ChatTongyi(model="tongyi-xiaomi-analysis-pro")

first_name = PromptTemplate.from_template(
    "我的邻居姓{lastname},刚生了{gender},需要你帮我取一个名字,输出结果的key是name,value为取到的名字"
)
second_name = PromptTemplate.from_template(
    "名字是{name}，请帮我解析含义"
)

chain = first_name | model | myfunc | second_name | model | str_parser

for chunk in chain.stream({"lastname":"王","gender":"男"}):
    print(chunk,end="",flush=True)
