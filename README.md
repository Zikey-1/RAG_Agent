# 🚀 RAG_Agent：大模型检索增强生成与智能体系统

## 📌 项目简介
本项目是一个基于 **RAG（Retrieval-Augmented Generation）** 构建的智能问答系统，结合大语言模型（LLM）与外部知识库，实现高质量、可溯源的问答能力。

通过引入 Agent 机制，实现复杂任务的自动化处理与多步骤推理。

---

## 🧠 核心能力

- 🔍 **文档检索（Retrieval）**
  - 基于向量数据库实现语义搜索
- 🤖 **生成增强（Generation）**
  - 使用大模型生成上下文感知回答
- 🧩 **Agent智能体**
  - 支持任务分解与工具调用
- 📚 **知识库构建**
  - 支持文本 / PDF / 多数据源
- ⚡ **高扩展性架构**
  - 模块化设计，易于扩展

---

## 🏗️ 技术架构

```text
用户问题
   ↓
Embedding 向量化
   ↓
向量数据库检索（Top-K）
   ↓
上下文拼接（Prompt）
   ↓
大模型生成回答（LLM）
   ↓
返回结果

## 项目结构
RAG_Agent/
│── src/                # 核心代码
│── data/               # 知识库数据
│── docs/               # 文档说明
│── tests/              # 测试代码
│── requirements.txt    # 依赖
│── README.md

## 技术栈
| 模块    | 技术                           |
| ----- | ---------------------------- |
| LLM   | OpenAI / 本地模型                |
| 框架    | LangChain / LangGraph        |
| 向量数据库 | Chroma / FAISS               |
| 数据处理  | BeautifulSoup / TextSplitter |
| Agent | ReAct / Tool Calling         |
