from langchain_community.embeddings import DashScopeEmbeddings

model = DashScopeEmbeddings()  #默认使用text-embeddiongs-v1

print(model.embed_query("你好"))  #单个
print(model.embed_documents(["你好","你好吗"]))  # 多个
 

from langchain_ollama import OllamaEmbeddings

