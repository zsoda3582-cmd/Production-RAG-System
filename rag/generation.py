import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def build_context(retrieved_chunks:list[dict])->str:
    context = "\n\n".join(
            f"[Source {i}]\n"
            f"Title: {chunk['metadata']['title']}\n"
            f"Content: {chunk['content']}"
            for i,chunk in enumerate(retrieved_chunks,start = 1)
        )#在检索结果retrieved_chunks中找到这些成分，把它们拼接起来，整理成上下文传给LLM

    return context

def generate_answer( #用于构造prompt 调用LLM 返回答案
        question:str,
        retrieved_chunks:list[dict]
    )->str:

    #1.构造context
    context = build_context(retrieved_chunks)

    #2.构造prompt
    messages = [
        {
            "role":"system",
            "content":(
                "You are a documentation QA assistant. "
                "Answer the question using only the provided context. "
                "If the context does not contain enough information, "
                "say you don't know based on the retrieved documents. "
                "Cite relevant source numbers such as [Source 1]."
            )
        },
        {
            "role":"user",
            "content":f"Context:\n{context}\n\nQuestion:\n{question}",
        }
    ]

    #3.初始化LLM客户端
    client = OpenAI(
        api_key = os.environ["DEEPSEEK_API_KEY"],
        base_url = "https://api.deepseek.com"
    )

    #4.调用LLM
    response = client.chat.completions.create(
        model = "deepseek-chat",
        messages = messages,
        temperature = 0,
        max_tokens = 256,
        timeout=20
    )

    #5.返回回答
    return response.choices[0].message.content or ""