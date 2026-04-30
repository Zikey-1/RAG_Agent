from langchain_community.chat_models import ChatTongyi
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatTongyi(model="tongyi-xiaomi-analysis-pro")
prompt = ChatPromptTemplate.from_messages([
    ("system", "以我提供的已知资料为主，简洁和专业的回答用户问题，参考资料:{context}"),
    ("human","用户提问: {input}")
])

vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings()  # 这里需要添加model,不添加则默认使用text-embedding-v1
)

vector_store.add_texts(["减肥要少吃多练","减肥期间要控制饮食，减少卡路里摄入","跑步是好的运动方式"])

input_text = " 怎么减肥?"

#检索向量库
result = vector_store.similarity_search(input_text,k=2)

# 拿参考资料 -> 向量检索库
reference_text="["
for doc in result:
    reference_text+=doc.page_content
reference_text+="]"

#定义函数在输入模型之前，打印检查
def print_prompt(prompt):
    print(prompt.to_string())
    print("=" * 20)
    return prompt

chain = prompt | print_prompt | model | StrOutputParser()

res = chain.invoke({"input":input_text,"context":reference_text})
print(res)
