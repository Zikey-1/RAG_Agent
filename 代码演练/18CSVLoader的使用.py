from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path="#####",
    encoding="utf-8",           
    csv_args={
        "delimiter":","            # 指定分隔符
    }
)
# 批量加载   -> [Document,Document,...]
documents = loader.load()

# 懒加载     -> 迭代器[Document]
for document in loader.lazy_load():
    print(document)