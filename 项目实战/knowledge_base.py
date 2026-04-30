import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

def check_md5(md5_str: str):
    # 检查传入的md5字符串是否已经处理
    if not os.path.exists(config.md5_path):
        open(config.md5_path,"w",encoding="utf-8").close()
        return False
    else:
        for line in open(config.md5_path,"r",encoding="utf-8"):
            line = line.strip()
            if line == md5_str:    
                return True       # 已处理
        return False
        

def save_md5(md5_str: str):
    # 将传入的md5字符串保存到文件
    with open(config.md5_path,"a",encoding="utf-8") as f:
        f.write(md5_str+"\n")

def get_string_md5(input_str: str,encoding='utf-8'):
    #将字符串转换为bytes字节数组
    str_bytes = input_str.encode(encoding=encoding)

    # 创建md5对象
    md5_obj = hashlib.md5()
    # 更新md5对象
    md5_obj.update(str_bytes)
    # 获取md5值
    md5_str = md5_obj.hexdigest()
    return md5_str

    pass

class KnowledgeBaseService(object):
    def __init__(self):
        # 初始化数据库
        os.makedirs(config.persist_directory,exist_ok=True)

        self.chroma = Chroma(
            collection_name=config.collection_name,   # 数据库表名
            embedding_function=DashScopeEmbeddings(model=config.embedding_model_name),
            persist_directory=config.persist_directory,   # 数据库本地存储文件夹

        )
        # 文本分割器
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=1000,   # 分割后的文本段最大长度
            chunk_overlap=100,  # 分割后的文本段最大重叠长度
            separators=config.separators,  # 分割符
            length_function=len,  # 分割函数
        )

    def upload_by_str(self,data:str,filename):
        # 将传入的字符串进行向量化，存入向量数据库
        # 拿到传入字符串的md5值
        md5_hex = get_string_md5(data)
        # 检查md5值是否已经处理
        if check_md5(md5_hex):
            return "【跳过】，内容已存在知识库中"
        
        if len(data) > config.max_split_char_number:
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadata = {
            "source":filename,
            "create_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        self.chroma.add_texts(      # 内容加载到向量库中
            # iterable -> list / tuple
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]
        )
        return "【成功】，内容已加载到知识库中"
      



if __name__ == "__main__":
    service = KnowledgeBaseService()
    with open("e:/Development/AI大模型RAG与智能体开发/项目实战/尺码推荐.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    metadata = {
        "source": "尺码推荐.txt",
        "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    service.chroma.add_texts(
        texts=lines,
        metadatas=[metadata for _ in lines]
    )
    print(f"【成功】，{len(lines)}条内容已加载到知识库中")