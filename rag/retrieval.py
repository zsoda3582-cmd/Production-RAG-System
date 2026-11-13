def retrieve(
        query:str,
        model,
        index,
        chunks:list[dict],
        top_k:int=5
)->list[dict]:
    query_embedding = model.encode(
        [query],
        normalize_embeddings = True
    )

    scores,indices = index.search(query_embedding,top_k)

    results = []

    for score,chunk_index in zip(scores[0],indices[0]):
        result = {
            "score":float(score),
            "content":chunks[chunk_index]["content"],
            "metadata":chunks[chunk_index]["metadata"]
        }
        results.append(result)

    return results