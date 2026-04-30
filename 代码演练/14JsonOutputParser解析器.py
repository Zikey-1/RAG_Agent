from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

model = ChatTongyi(model="tongyi-xiaomi-analysis-pro")

first_name = PromptTemplate.from_template(
    "我的邻居姓{lastname},刚生了{gender},需要你帮我取一个名字,输出结果的key是name,value为取到的名字"
)
second_name = PromptTemplate.from_template(
    "名字是{name}，请帮我解析含义"
)

chain = first_name | model |json_parser | second_name | model | str_parser
#输入invoke/stream->firstname(PromptValue)->model(AImessage)->jsonparser(dict)->secondname(PromptValue)->model(AImessage)->strparser(字符串)

res = chain.invoke({"lastname":"张","gender":"女儿"})
print(res)
