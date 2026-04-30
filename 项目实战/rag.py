from xml.dom.minidom import Document
from vector_store import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnablePassthrough,RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from file_history_store import get_history
from langchain_core.runnables import RunnableLambda 



def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)

    return prompt

class RagService(object):
    def __init__(self):

        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name)
        )

        self.prompt_template = ChatPromptTemplate.from_messages (
            [
                ("system","根据我提供的已知参考资料为主,"
                 "简洁和专业的回答用户问题，参考资料:\n{context}"),
                 ("system","我提供用户的对话历史记录如下：\n"),
                 MessagesPlaceholder("chat_history"),
                 ("user","请回答用户提问：{input}")
            ]
        )

        self.chat_model = ChatTongyi(model=config.chat_model_name)

        self.chain = self.__get_chain()


    def __get_chain(self):
        #获取执行链
        retriever = self.vector_service.get_retriever()
        def format_document(docs: list[Document]):
            if not docs:
                return "无相关资料"
            
            formatted_str = ""
            for doc in docs:
                formatted_str += f"文件片段：{doc.page_content}\n文档元数据:{doc.metadata}\n\n"
            
            return formatted_str

        def temp1(value: dict) -> str:
            return value["input"]
        def temp2(value):
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["chat_history"] = value["input"]["chat_history"]
            return new_value


        chain = (
            {
            "input":RunnablePassthrough(),
            "context":RunnableLambda(temp1) | retriever | format_document   #检索器
            } | RunnableLambda(temp2) | self.prompt_template | print_prompt| self.chat_model | StrOutputParser()
        )

        conversion_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="chat_history"

        )

        
        return conversion_chain
    
if __name__ == "__main__":
    # session id 配置
    session_config = {
        "configurable": {
            "session_id": "user_zzk"
        }
    }
    # res = RagService().chain.invoke("我身高2米，体重200斤，尺码推荐",session_config)
    res = RagService().chain.invoke({"input": "我身高210cm"}, session_config)
    print(res)





