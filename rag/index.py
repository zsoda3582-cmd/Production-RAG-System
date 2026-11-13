import faiss
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL = "all-miniLM-L6-v2"

def build_index(chunks:list[dict]):
    model = SentenceTransformer(EMBEDDING_MODEL)

    texts = [
        f"Document:{chunk['metadata']['title']}\n\n{chunk['content']}"
        for chunk in chunks
    ]

    embeddings = model.encode(
        texts,
        normalize_embeddings = True #向量归一化，将所有向量长度统一成1
    )

    dimension = embeddings.shape[1] #shape是在问这个二维数组是什么形状（chunk数量，每个chunk多少维度）
    #embeddings.shape[1]拿到embedding vector的维度

    index = faiss.IndexFlatIP(dimension) #用faiss方法来搜索匹配
    #index：FAISS的向量索引；Flat：暴力精确搜索；IP：用内积来计算向量相似度
    #19行：告诉FAISS——建一个embeddings.shape[1]维的索引，用内积来计算相似度
    index.add(embeddings)

    return model,index