import os,json
from typing import Sequence,List
from langchain_core.messages import message_to_dict,messages_from_dict,BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
# message_to_dict:单个消息对象(BaseMessage类实例) ->dict
# message_from_dict：[字典，字典...] -> [消息，消息...]

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path):
        self.session_id = session_id      #会话Id
        self.storage_path = storage_path  #不同会话id的存储文件，所在的文件夹路径
        self.file_path = os.path.join(self.storage_path,self.session_id)  #完整的路径
        #确保文件夹存在
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)

    def add_message(self,message:BaseMessage) ->None:
        self.add_messages([message])

    def add_messages(self,messages:Sequence[BaseMessage]) ->None:
        all_messages = list(self.messages)     # 已有的消息列表
        all_messages.extend(messages)          # 和已有的融合为一个list

        # new_messagges = []
        # for message in all_messages:
        #     d = message_to_dict(message)
        #     new_messagges.append(d)

        new_messagges = [message_to_dict(message) for message in all_messages]
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump(new_messagges,f)
    @property
    def messages(self) -> List[BaseMessage]:
        try:
            with open(self.file_path,"r",encoding="utf-8") as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []
    
    def clear(self) -> None:
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump([],f)


model = ChatTongyi(model="tongyi-xiaomi-analysis-pro")
# prompt = PromptTemplate.from_template(
#     "你需要过呢据会话历史回应用户问题，对话历史:{chat_history},用户提问:{input},请回答"
# )
prompt = ChatPromptTemplate.from_messages([
    ("system", "你需要根据会话历史回应用户问题,对话历史"),
    MessagesPlaceholder("chat_history"),
    ("human","请回答如下问题--{input}")
])

str_parser = StrOutputParser()

def print_prompt(full_prompt):
    print("="*20,full_prompt.to_string(),"="*20)
    return full_prompt

base_chain = prompt | print_prompt | model | str_parser


def get_history(session_id):
    return FileChatMessageHistory(session_id,"./chat_history")
  

conversion_chain = RunnableWithMessageHistory(
    base_chain,                          # 被增强的原始chain
    get_history,                         # 通过会话Id获取InMemoryChatMessageHistory类对象
    input_messages_key="input",
    history_messages_key="chat_history",
)

if __name__ == "__main__":
    session_config = {
        "configurable":{
            "session_id":"user_001"
        }
    }
    # res = conversion_chain.invoke({"input":"小明有2猫"},session_config)
    # print("第1次执行",res)
    # res = conversion_chain.invoke({"input":"小泓有1条狗"},session_config)
    # print("第2次执行",res)
    res = conversion_chain.invoke({"input":"共有多少动物"},session_config)
    print("第3次执行",res)