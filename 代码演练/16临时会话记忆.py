from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser

model = ChatTongyi(model="tongyi-xiaomi-analysis-pro")
# prompt = PromptTemplate.from_template(
#     "你需要过呢据会话历史回应用户问题，对话历史:{chat_history},用户提问:{input},请回答"
# )
prompt = ChatPromptTemplate.from_messages([
    ("system", "你需要根据会话历史回应用户问题"),
    MessagesPlaceholder("chat_history"),
    ("human","请回答如下问题--{input}")
])

str_parser = StrOutputParser()

def print_prompt(full_prompt):
    print("="*20,full_prompt.to_string(),"="*20)
    return full_prompt

base_chain = prompt | print_prompt | model | str_parser

store = {}  
def get_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

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
    res = conversion_chain.invoke({"input":"小明有2猫"},session_config)
    print("第1次执行",res)
    res = conversion_chain.invoke({"input":"小泓有1条狗"},session_config)
    print("第2次执行",res)
    res = conversion_chain.invoke({"input":"共有多少动物"},session_config)
    print("第3次执行",res)