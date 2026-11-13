from langchain_text_splitters import RecursiveCharacterTextSplitter

def analyze_document_lengths(documents:list[dict])->None:
    lengths = [len(document["content"]) for document in documents]

    print(f"Document count:{len(lengths)}")
    print(f"Shortest: {min(lengths)} characters")
    print(f"Longest: {max(lengths)} characters")
    print(f"Average: {sum(lengths) // len(lengths)} characters")

def split_documents(documents:list[dict])->list[dict]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )

    chunks = []

    for document in documents:
        texts = text_splitter.split_text(document["content"])

        for chunk_index,text in enumerate(texts):
            chunk = {
                "content":text,
                "metadata":{
                    **document["metadata"],#展开这个字典，把里面的东西复制进去
                    "chunk_index":chunk_index
                }
            }
            chunks.append(chunk)

    return chunks