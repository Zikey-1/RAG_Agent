from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate
from langchain_community.llms.tongyi import Tongyi

# 示例模板
exanple_template = PromptTemplate.from_template("单词:{word},反义词:{antoym}")
# 示例的动态数据注入，要求：list嵌套字典
examples_data = [
    {"word":"大","antoym":"小"},
    {"word":"上","antoym":"下"}
]

few_shot_template = FewShotPromptTemplate(
    examples=examples_data,                                            # 示例数据,list嵌套字典
    example_prompt=exanple_template,                                   # 示例数据的模板
    prefix="告知我单词的反义词，我提供如下的示例",                           # 示例之前的提示词
    suffix="基于我之前的示例告诉我，单词:{input_word}的反义词是？",           # 示例之后的提示词
    input_variables=["input_word"]                                     #声明再前缀或后缀中所需要注入的变量名
)

prompt_text = few_shot_template.invoke(input={"input_word":"左"}).to_string()  #最后转换为字符串输出，结果更直接
print(prompt_text)

model = Tongyi(model="tongyi-xiaomi-analysis-pro")
print(model.invoke(input=prompt_text))
