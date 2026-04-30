md5_path="./md5.txt"


#  Chroma数据库配置
collection_name = "rag"
persist_directory = "./chroma_db"

# splitter
chunk_size=1000
chunk_overlap=100
separators=["\n\n","\n",",","，","。","!","！","？","?"]
max_split_char_number = 1000  # 文本分割阈值


# 相似度检索返回匹配的文档数量
similarity_threshold = 1

embedding_model_name = "text-embedding-v4"
chat_model_name = "MiniMax-M2.1"

session_config = {
    "configurable": {
        "session_id": "user_zzk"
    }
}