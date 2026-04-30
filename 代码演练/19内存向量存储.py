from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings()
)

loader = CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",           
    source_column="source"      # 指定文档的来源是哪里
)

documents = loader.load()
print(documents[1])
#
vector_store.add_documents(
    documents=documents,        #被添加的文档,类型->list[Document]
    ids=["id"+str(i) for i in range(1,len(documents)+1)]   # 文档id(字符串),类型->list[str]
)

#删除
vector_store.delete(
    document_ids=["id1","id2"]
)

#检索,返回类型->list[Document]
res = vector_store.similarity_search(
    query="今晚吃什么",   
    k=2       #检索的结果的数量
)
print(res)