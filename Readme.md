# Production RAG System

基于检索增强生成（Retrieval-Augmented Generation，RAG）的文档智能问答系统，以 LangChain 官方文档为知识库，实现语义检索、答案生成与来源引用。

## 一、项目简介

本项目实现了一套端到端的 RAG 问答系统。

系统首先对 LangChain 官方文档进行加载、切分和向量化，利用 FAISS 构建向量索引。当用户提出问题时，系统通过语义检索获取相关文档片段，并结合 DeepSeek 大语言模型生成有参考依据的回答。

项目不仅实现了 RAG 核心流程，还包含检索与生成质量评测、FastAPI 接口封装、Docker 容器化部署以及 Streamlit 可视化交互界面。

## 二、核心功能

- **文档处理**：加载 LangChain 官方文档，进行文本切分和知识库构建。
- **语义检索**：使用 Sentence Transformers 生成文本向量，利用 FAISS 检索相关文档片段。
- **答案生成**：接入 DeepSeek API，根据检索结果生成答案，并提供来源引用。
- **系统评测**：通过检索评测和生成质量评测，验证系统的实际效果。
- **API 接口**：使用 FastAPI 封装 RAG 服务，支持 HTTP 请求调用。
- **容器化运行**：使用 Docker 打包后端应用及运行环境。
- **交互界面**：使用 Streamlit 构建简单的网页问答 Demo。

## 三、系统架构

本项目采用前后端分离的方式，将用户交互、API 服务和 RAG 核心逻辑进行模块化组织。

### 3.1 整体架构

```text
                 用户
                  │
                  ▼
          Streamlit 前端界面
                  │
             HTTP POST
                  │
                  ▼
           FastAPI 后端服务
                  │
                  ▼
             RAG Pipeline
                  │
       ┌──────────┴──────────┐
       │                     │
       ▼                     ▼
   Embedding 模型        FAISS 向量索引
       │                     ▲
       └─────向量检索────────┘
                  │
                  ▼
          Top-K 相关文档片段
                  │
                  ▼
           DeepSeek LLM
                  │
                  ▼
         答案 + 来源引用
                  │
                  ▼
          Streamlit 展示结果
```

### 3.2 知识库构建（离线阶段）

在用户提问之前，系统首先完成知识库的预处理和向量索引构建。

```text
LangChain 官方文档
        ↓
文档加载（Ingestion）
        ↓
文本切分（Chunking）
        ↓
文本向量化（Embedding）
        ↓
建立 FAISS 向量索引
```

这一阶段的目标是将原始文档转换为可检索的向量知识库，避免每次用户提问时重新加载和处理全部文档。

### 3.3 在线问答（在线阶段）

当用户通过 Streamlit 输入问题后，系统执行以下流程：

1. Streamlit 通过 HTTP POST 请求调用 FastAPI 的 `/ask` 接口。
2. FastAPI 接收用户问题并调用 RAG 核心模块。
3. Embedding 模型将用户问题转换为向量。
4. FAISS 执行相似度搜索，检索 Top-K 相关文档片段。
5. 系统将用户问题与检索到的文档内容组合为 Prompt。
6. DeepSeek 大语言模型根据参考内容生成答案。
7. FastAPI 返回包含答案和来源信息的 JSON 数据。
8. Streamlit 展示最终答案及检索来源。

### 3.4 工程模块划分

| 模块 | 主要职责 |
|---|---|
| `rag/ingestion.py` | 文档加载与预处理 |
| `rag/chunking.py` | 文本切分 |
| `rag/index.py` | Embedding 与 FAISS 索引管理 |
| `rag/retrieval.py` | 向量检索 |
| `rag/generation.py` | LLM 答案生成 |
| `evaluation/` | 系统评测相关文件 |
| `api.py` | FastAPI 后端接口 |
| `demo.py` | Streamlit 前端界面 |
| `Dockerfile` | Docker 镜像构建配置 |
| `requirements.txt` | Python 项目依赖 |


## 四、系统评测

为了验证 RAG 系统的实际效果，本项目分别从**检索质量**和**答案生成质量**两个方面进行评测。

### 4.1 检索质量评测（Retrieval Evaluation）

构建包含 40 条测试问题的评测集，用于验证系统能否从 LangChain 文档知识库中检索出相关内容。

**评测指标：Hit@5**

Hit@5 用于衡量：在返回的前 5 个检索结果中，是否至少有一个命中预期的相关文档。

**评测结果：**

| 指标 | 结果 |
|---|---|
| 测试问题数量 | 40 |
| 检索数量 Top-K | 5 |
| Hit@5 | 92.5% |
| 命中问题数量 | 37 / 40 |

该结果表明，在当前测试集和评测标准下，系统能够为大部分问题检索到预期的相关文档。

### 4.2 答案生成质量评测（Generation Evaluation）

在检索评测基础上，进一步评估大语言模型生成答案的可靠性。

本项目使用 LLM-as-a-Judge 方法，通过大语言模型对生成结果进行自动化评价。

主要评测维度包括：

- **Faithfulness（忠实性）**：生成答案中的事实性陈述是否得到检索上下文的支持。
- **Citation Faithfulness（引用忠实性）**：答案中的来源引用是否能够支持相应陈述。

**评测结果：**

| 指标 | 结果 |
|---|---|
| 测试问题数量 | 40 |
| Faithfulness | 40 / 40 通过 |
| Citation Faithfulness | 40 / 40 通过 |

以上结果基于当前 40 条测试样本和二元自动评判标准，仅代表该评测设置下的初步表现，不意味着系统在所有问题上都能保证回答正确。

### 4.3 评测总结

本项目建立了从检索到生成的基本评测流程：

1. 通过 Hit@5 检查检索阶段能否找到相关文档。
2. 通过 LLM-as-a-Judge 检查生成答案与参考内容的一致性。
3. 保存评测结果，为后续检索优化、模型调整和效果对比提供依据。

通过将评测流程纳入项目，系统不仅具备基本问答能力，也具备初步的质量验证能力。


## 五、项目运行指南（Quick Start）

### 5.1 环境要求

运行本项目需要以下环境：

- Python 3.11（Docker 容器内使用）
- Docker Desktop
- DeepSeek API Key
- Git（用于克隆项目）

### 5.2 获取项目

```bash
git clone https://github.com/zsoda3582-cmd/Production-RAG-System.git
cd Production-RAG-System
```


### 5.3 配置环境变量

在项目根目录创建 `.env` 文件，配置 DeepSeek API Key：

```env
DEEPSEEK_API_KEY=your_api_key_here
```

注意：

- `.env` 包含敏感信息，不应提交到 GitHub。
- Docker 启动时通过 `--env-file .env` 注入环境变量。
- 建议在仓库中提供 `.env.example` 作为配置模板。

### 5.4 构建 Docker 镜像

在项目根目录执行：

```bash
docker build -t production-rag:latest .
```

Docker 将根据 `Dockerfile` 安装 Python 依赖并构建后端运行环境。

首次构建可能需要较长时间，因为项目依赖 Sentence Transformers、PyTorch 等组件。

### 5.5 启动 FastAPI 后端

执行：

```bash
docker run --name production-rag-container -p 8001:8000 --env-file .env production-rag:latest
```

启动成功后，可以访问：

- API 地址：`http://127.0.0.1:8001`
- Swagger 接口文档：`http://127.0.0.1:8001/docs`

系统提供 `POST /ask` 接口，接收用户问题并返回生成答案及检索来源。

**请求示例：**

```json
{
  "question": "What is MCP?"
}
```

**响应结构示例：**

```json
{
  "question": "What is MCP?",
  "answer": "根据检索文档生成的回答...",
  "sources": [
    {
      "source_id": 1,
      "title": "相关文档标题",
      "score": 0.85
    }
  ]
}
```

以上响应为结构示意，非真实运行结果。

如果容器已经创建并处于停止状态，可以使用：

```bash
docker start production-rag-container
```

### 5.6 启动 Streamlit 前端

在本地 Python 环境中安装依赖：

```bash
python -m pip install -r requirements.txt
python -m pip install streamlit requests
```

确保 Docker 后端已经启动，然后运行：

```bash
python -m streamlit run demo.py
```

浏览器访问：

```text
http://localhost:8501
```

在网页中输入问题，点击 Ask，即可查看生成答案及对应的检索来源。

### 5.7 运行说明
### 5.7 运行说明

当前项目采用前后端分离的运行方式：

- **FastAPI 后端**：运行在 Docker 容器中，容器端口为 `8000`，通过端口映射 `8001:8000` 对外提供服务。
- **Streamlit 前端**：运行在本地 Python 环境中，默认访问地址为 `http://localhost:8501`。
- **前后端通信**：Streamlit 通过 HTTP POST 请求访问 `http://127.0.0.1:8001/ask`。

系统通过 FastAPI 的 `lifespan` 机制，在服务启动时自动加载 LangChain 文档、执行文本切分并构建 FAISS 向量索引。

索引、Embedding 模型及文档 Chunks 保存在服务进程的内存中，无需提前手动生成索引文件。每次重新启动 FastAPI 应用时，系统都会重新执行初始化流程，因此启动时间可能较长。

运行前需确保知识库文档目录 `temp_langchain_docs/src/oss/langchain` 存在，并在构建 Docker 镜像时被正确复制到容器中。

## 六、项目局限性与未来改进

目前 Production RAG System 已实现完整的检索增强生成流程，并完成基础评测、API 服务化和容器化运行，但仍存在以下改进空间。

### 6.1 检索能力

当前系统主要采用 Embedding + FAISS 进行语义检索。对于精确术语、缩写或特定关键词，单一向量检索可能无法始终返回最相关的文档片段。

未来可根据实际检索失败案例，考虑引入 Hybrid Search 或 Reranking 等方法，进一步提高检索质量。

### 6.2 评测体系

当前使用 40 条测试问题进行检索与生成质量评测，初步验证了系统效果。

但评测集规模仍然有限，且生成质量评测依赖 LLM-as-a-Judge，可能受到评判模型和评判标准的影响。

未来可以扩展测试集，并引入更多类型的测试问题，提高评测结果的代表性。

### 6.3 工程可靠性

目前系统已经完成 FastAPI 服务封装和 Docker 容器化运行，但尚未系统验证并发请求、长期运行稳定性以及异常情况下的恢复能力。

未来可逐步补充自动化测试、日志监控和性能评测，提高系统的可维护性与可靠性。

### 6.4 部署与扩展

当前项目采用 Docker 运行 FastAPI 后端，Streamlit 前端在本地环境中运行。

未来可进一步完成服务器部署，使系统能够通过外部网络访问，并根据实际需求完善配置管理和部署流程。
