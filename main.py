# from rag.ingestion import load_documents
# from rag.chunking import split_documents
# from rag.index import build_index
# from rag.retrieval import retrieve
# from evaluation.retrieval_cases import RETRIEVAL_CASES
# from evaluation.retrieval_eval import evaluate_retrieval

# DOCUMENT_DIR = "temp_langchain_docs/src/oss/langchain"

# documents = load_documents(DOCUMENT_DIR)

# chunks = split_documents(documents)

# # titles = sorted({
# #     chunk["metadata"]["title"]
# #     for chunk in chunks
# # })#{}用于去重，再用sorted排序，便于查看
# # print(f"Total documents:{len(titles)}")
# # for title in titles:
# #     print(title)

# model,index = build_index(chunks)

# evaluation = evaluate_retrieval(
#     RETRIEVAL_CASES,
#     model = model,
#     index = index,
#     chunks = chunks,
#     top_k = 5
# )
# # print(f"\nHit@5:{evaluation['hit_rate']}")

# # for result in evaluation["results"]:
# #     print(f"\nQuestion: {result['question']}")
# #     print(f"Expected: {result['expected']}")
# #     print(f"Retrieved: {result['retrieved_titles']}")
# #     print(f"Hit: {result['hit']}")

# #====================定位Middleware为什么没有命中======================
# middelware_chunks = [
#     chunk for chunk in chunks
#     if chunk["metadata"]["title"] == "Middleware overview"
# ]

# print("Middleware chunks:",len(middelware_chunks))

# for chunk in middelware_chunks:
#     print("\nChunk index:",chunk["metadata"]["chunk_index"])
#     print(chunk["content"][:500])

# queries = [
#     "What is middleware in Langchain?",
#     "What is LangChain agent middleware?",
#     "Middleware provides a way to control agent behavior",
# ]

# for question in queries:
#     query_vector = model.encode(
#         [question],
#         normalize_embeddings = True
#     )

#     scores,indices = index.search(
#         query_vector,
#         index.ntotal
#     )

#     for rank,(score,idx) in enumerate(
#         zip(scores[0],indices[0]),
#         start = 1
#     ):
#         chunk = chunks[int(idx)]

#         if (
#             chunk["metadata"]["title"] == "Middleware overview"
#             and chunk["metadata"]["chunk_index"] == 0
#         ):
#             print(
#                 f"Query:{question}\n"
#                 f"Rank:{rank} | "
#             )
#             break

from rag.ingestion import load_documents
from rag.chunking import split_documents
from rag.index import build_index
from rag.retrieval import retrieve
from rag.generation import generate_answer
from evaluation.retrieval_cases import RETRIEVAL_CASES
from evaluation.retrieval_eval import evaluate_retrieval
from evaluation.generation_eval import save_generation_record
from evaluation.generation_eval import run_generation_evaluation

from pathlib import Path


DOCUMENT_DIR = "temp_langchain_docs/src/oss/langchain"

#1.文档加载与切分
documents = load_documents(DOCUMENT_DIR)
chunks = split_documents(documents)

#2.构建向量索引
model,index = build_index(chunks)


#清空旧的演示记录
records_path = Path("evaluation/generation_records.jsonl")
records_path.parent.mkdir(parents=True,exist_ok=True)
records_path.write_text("",encoding="utf-8")

#批量执行真实RAG
for i,case in enumerate(RETRIEVAL_CASES,start=1):
    question = case["question"]

    retrieved_chunks = retrieve(
        question,
        model,
        index,
        chunks,
        top_k=5
    )

    answer = generate_answer(question,retrieved_chunks)

    save_generation_record(question,answer,retrieved_chunks)

    print(f"[{i}/{len(RETRIEVAL_CASES)}] Generated:{question}")

#批量执行LLM Judge
summary = run_generation_evaluation()

print("\n============Generation Evaluation================")
print(summary)


# #3.====== 端到端RAG测试 ======
# question = "What is MCP?"

# #3.1 检索(负责在库中寻找证据)
# retrieved_chunks = retrieve(
#     question,
#     model,
#     index,
#     chunks,
#     top_k = 5
# )

# #3.2 生成Answer（负责根据证据生成回答)
# answer = generate_answer(question,retrieved_chunks)

# #3.3 打印结果
# print("\n========= RAG Answer =========")
# print("Question:",question)
# print("Answer:",answer)

# print("\n======= Retrieved Sources =======")
# for i,chunk in enumerate(retrieved_chunks,start=1):
#     print(f"[Source {i}] {chunk['metadata']['title']}")
#     print(chunk["content"][:500])

# answer = (
#     "MCP stands for the Model Context Protocol. "
#     "It lets an agent connect to external servers "
#     "that provide tools and resources [Source 5]."
# )

# save_generation_record(
#     question = question,
#     answer = answer,
#     retrieved_chunks=retrieved_chunks
# )

# #4.批量检索评测
# evaluation = evaluate_retrieval(
#     RETRIEVAL_CASES,
#     model = model,
#     index = index,
#     chunks = chunks,
#     top_k = 5
# )


# failed_cases = [
#     result for result in evaluation["results"]
#     if not result["hit"]
# ]
# print(f"\nHit@5:{evaluation['hit_rate']:.2%}")
# print(f"Failed cases:{len(failed_cases)}")

# for result in failed_cases:
#     print(f"\nQuestion:{result['question']}")
#     print(f"\nExpected:{result['expected']}")
#     print(f"\nRetrieved:{result['retrieved_titles']}")

# question_to_check = {
#     "What is an agent in LangChain?",
#     "What are tools in LangChain?",
#     "How does tool calling work with language models?"
# }

# for question in question_to_check:
#     results = retrieve(
#         query = question,
#         model = model,
#         index = index,
#         chunks = chunks,
#         top_k = 5
#     )

#     print("========== Question ========")

#     for rank,chunk in enumerate(results,start = 1):
#         print(f"Rank:{rank}")
#         print(f"Title:{chunk['metadata']['title']}")
#         print(f"Content:{chunk['content'][:800]}")

#====================定位MCP为什么没有命中======================
# query = "What is Model Context Protocol?"

# #找到正确的MCP Chunk 0
# mcp_chunk = next(
#     chunk for chunk in chunks
#     if chunk["metadata"]["title"] == "Model Context Protocol (MCP)"
#     and chunk["metadata"]["chunk_index"] == 0
# )

# #分别讲问题和正确Chunk编码称向量
# query_vector = model.encode(
#     [query],
#     normalize_embeddings = True
# )

# mcp_vector = model.encode(
#     [mcp_chunk["content"]],
#     normalize_embeddings = True
# )

# #计算二者的相似度
# similarity = float(query_vector[0] @ mcp_vector[0])
# #@是Numpy的矩阵乘法运算符，点乘的两个向量都是一维向量，所以此处计算的是点积，
# #经过normalize归一化以后，点积相当于计算余弦相似度

# print(f"\nMCP Chunk 0 similarity:{similarity:.4f}")

# #查看FAISS实际排在前面的结果及其分数
# results = retrieve(query,model,index,chunks,top_k=5)

# for rank,result in enumerate(results,start=1):
#     print(
#         f"Rank{rank}:"
#         f"{result['metadata']['title']}"
#         f"|Score:{result['score']:.4f}"
#     )

# clean_mcp_text = (
#     "Model Context Protocol (MCP) is an open protocol "
#     "that standardizes how applications provide tools "
#     "and context to language models."
# )

# clean_mcp_vector = model.encode(
#     [clean_mcp_text],
#     normalize_embeddings = True
# )

# clean_similarity = float(
#     query_vector[0] @ clean_mcp_vector[0]
# )

# print(f"Original MCP similarity:{similarity:.4f}")
# print(f"Clean MCP similarity:{clean_similarity:.4f}")

# print("\n================== MCP Chunks ===================")

# for chunk in chunks:
#     if chunk["metadata"]["title"] == "Model Context Protocol (MCP)":
#         print(f"\nChunk{chunk['metadata']['chunk_index']}")
#         print(chunk["content"][:1000])

# results = retrieve(
#     query = query,
#     model = model,
#     index = index,
#     chunks = chunks,
#     top_k = 5
# )

# print(f"Loaded {len(documents)} documents")
# print(f"Created {len(chunks)} chunks")
# print(f"Vector count {index.ntotal}") #FAISS里目前有多少个向量
# print(f"Vector dimension:{index.d}") #打印每个向量的维度

# print(f"\nQuery:{query}")

# for rank,result in enumerate(results,start = 1):
#     print(f"\nRank:{rank}")
#     print(f"Score:{result["score"]}")
#     print(f"Title:{result["metadata"]["title"]}")
#     print(f"\nContent:\n{result["content"][:500]}")