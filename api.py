from contextlib import asynccontextmanager

from fastapi import FastAPI,HTTPException
from openai import APIConnectionError,APITimeoutError,APIStatusError
from pydantic import BaseModel,Field,field_validator

from rag.ingestion import load_documents
from rag.chunking import split_documents
from rag.index import build_index
from rag.retrieval import retrieve
from rag.generation import generate_answer

DOCUMENT_DIR = "temp_langchain_docs/src/oss/langchain"

rag_state = {}

#1.服务启动时初始化RAG
@asynccontextmanager
async def lifespan(app:FastAPI): #lifespan可被理解为一个管理服务生命周期的函数

    documents = load_documents(DOCUMENT_DIR) #先加载文件
    chunks = split_documents(documents) #切分加载好的文件为一个个chunks

    model,index = build_index(chunks)

    rag_state["chunks"] = chunks
    rag_state["model"] = model
    rag_state["index"] = index

    print("RAG system initialized.")

    yield

    rag_state.clear()

#2.创建FastAPI应用
app = FastAPI(lifespan=lifespan)

class AskRequest(BaseModel): #定义请求的数据结构
    question:str = Field( #Field要求question至少有一个字符
        min_length = 1,
        description = "用户提出的问题"
    )

    @field_validator("question") #进一步检查question，去掉首尾空格后，不能是空字符串
    @classmethod
    def validate_question(cls,value):
        value = value.strip()

        if not value:
            raise ValueError("Question cannot be empty")

        return value

class SourceInfo(BaseModel): #规定每条检索来源应该包含什么
    source_id:int
    title:str
    score:float

class AskResponse(BaseModel): #整个问答产生的结果应该包含什么
    question:str
    answer:str
    sources:list[SourceInfo]

@app.post("/ask",response_model=AskResponse)
def ask(request:AskRequest):
    question = request.question

    retrieved_chunks = retrieve(
        question,
        rag_state["model"],
        rag_state["index"],
        rag_state["chunks"],
        top_k = 5
    )

    try:
        answer = generate_answer(question,retrieved_chunks)

    except APITimeoutError: #等待deepseek'响应超时
        raise HTTPException(
            status_code=504,
            detail="LLM service timeout"
        )

    except APIConnectionError: #暂时无法连接deepseek
        raise HTTPException(
            status_code=503,
            detail="LLM service temporarily available"
        )

    except APIStatusError: #deepseek返回了错误状态
        raise HTTPException(
            status_code=502,
            detail="LLM service returned an error"
        )

    sources = []

    for i ,chunk in enumerate(retrieved_chunks,start=1):
        sources.append(
            {
                "source_id":i,
                "title":chunk["metadata"]["title"],
                "score":float(chunk["score"])
            }
        )

    return {
        "question":question,
        "answer":answer,
        "sources":sources
    }