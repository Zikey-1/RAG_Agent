from langchain_community.vectorstores import InMemoryVectorStore
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from typing import List

print("开始执行...")

# 创建一个简单的嵌入类，避免网络依赖
class SimpleEmbedding(Embeddings):
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # 简单的嵌入实现，返回固定长度的向量
        return [[0.1 for _ in range(768)] for _ in texts]
    
    def embed_query(self, text: str) -> List[float]:
        # 简单的查询嵌入实现
        return [0.1 for _ in range(768)]

# 测试简单嵌入模型
print("测试简单嵌入模型...")
try:
    embedding = SimpleEmbedding()
    print("嵌入模型创建成功")
    
    # 测试文本嵌入
    test_text = "测试文本"
    embedding_result = embedding.embed_query(test_text)
    print(f"文本嵌入成功，向量长度: {len(embedding_result)}")
except Exception as e:
    print(f"嵌入模型测试失败: {e}")

# 测试向量存储
print("测试向量存储...")
try:
    # 创建文档
    documents = [
        Document(page_content="减肥要少吃多练"),
        Document(page_content="减肥期间要控制饮食，减少卡路里摄入"),
        Document(page_content="跑步是好的运动方式")
    ]
    
    # 创建向量存储
    vector_store = InMemoryVectorStore.from_documents(
        documents=documents,
        embedding=SimpleEmbedding()
    )
    print("向量存储创建成功")
    
    # 测试相似性搜索
    query = "怎么减肥?"
    results = vector_store.similarity_search(query, k=2)
    print(f"相似性搜索成功，找到 {len(results)} 个结果")
    for i, result in enumerate(results):
        print(f"结果 {i+1}: {result.page_content}")
except Exception as e:
    print(f"向量存储测试失败: {e}")

print("执行完成...")