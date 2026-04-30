from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from  langchain_core.messages import AIMessage

model = ChatTongyi(model="tongyi-xiaomi-analysis-pro")
parser = StrOutputParser()
prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname},刚生了{gender},需要你帮我取一个名字"
)

chain = prompt | model | parser | model | parser

# model 返回AImessage的类对象，使用parser解析为str
# 最后使用parser直接输出结果，否则需要使用.content方法提取AImessage的内容

res: str = chain.invoke({"lastname":"王","gender":"男"})
print(res)