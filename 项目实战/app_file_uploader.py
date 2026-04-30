# 基于streamlit的文件上传服务
# 注意：页面发生变化重新执行代码

import streamlit as st
from knowledge_base import KnowledgeBaseService
import time

# 添加网页标题
st.title("知识库更新服务")

# file_uploader
uploader_file = st.file_uploader(
    label="请上传TXT文件",
    type=["txt"],
    accept_multiple_files=False,  # False表示仅接受一个文件的上传
)

service = KnowledgeBaseService()
#  session_state就是一个字典 不随页面刷新而变化，解决streamlit的bug
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()
count = 0
if uploader_file is not None:
    # 提取文件的信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024  # KB

    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")

    # get_value -> bytes -> decode('utf-8')
    text = uploader_file.getvalue().decode("utf-8")


    with st.spinner("正在载入数据库中..."):  # 在spinner内的代码执行过程中，会有转圈动画
        time.sleep(1)
        result=st.session_state["service"].upload_by_str(text,file_name)
        st.write(result)
