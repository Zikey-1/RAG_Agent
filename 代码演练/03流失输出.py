from openai import OpenAI

# 1.获取client对象
client = OpenAI (
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 2.调用模型
response = client.chat.completions.create(
     model="tongyi-xiaomi-analysis-pro",
     messages=[
         {"role":"system","content":"你是python领域的专家，擅长处理python的相关问题和代码"},
         # {"role":"assistant","content":"好的，我是python专家，我可以解决任何python问题，你要问什么？"},
         {"role":"user","content":"给我输出1-10的数字，使用python代码"}
    ],
    stream=True
)
# 3.处理结果
# print(response.choices[0].message.content)
for a in response:
    print(a.choices[0].delta.content,
          end=" ",  # 输出隔了空格,可选
          flush=True,  # 立刻刷新缓冲区
)