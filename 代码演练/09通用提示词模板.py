from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

prompt_template = PromptTemplate.from_template(
    "我的邻居姓{last_name},生了一个{gender},你帮我起一个名字，简单回答"
)
model = Tongyi(model="tongyi-xiaomi-analysis-pro")

chain = prompt_template | model #将prompt_template注入到model中

res = chain.invoke(input={"last_name":"张","gender":"女儿"})
print(res)
