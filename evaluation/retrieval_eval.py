from rag.retrieval import retrieve

def evaluate_retrieval(
        cases:list[dict],
        model,
        index,
        chunks:list[dict],
        top_k:int=5
)->dict:
    hits = 0
    results = []

    for case in cases:

        print(case)

        retrieved_chunks = retrieve(
            query = case["question"],
            model = model,
            index = index,
            chunks = chunks,
            top_k = top_k
        )

        if case["question"] == "What is middleware in LangChain?":
            print("\n==== Middleware Top-5 Chunks ====")
            for rank,chunk in enumerate(retrieved_chunks,start = 1):
                print(f"\nRank:{rank}")
                print(f"Title:{chunk['metadata']['title']}")
                print(f"Chunk Index:{chunk['metadata']['chunk_index']}")
                print(f"Content:\n{chunk['content'][:600]}")

        retrieved_titles = [
            chunk["metadata"]["title"]
            for chunk in retrieved_chunks
        ]

        hit = any(
            title in retrieved_titles
            for title in case["expected_titles"]
        )

        if hit:
            hits += 1

        results.append({
            "question":case["question"],
            "expected":case["expected_titles"],
            "retrieved_titles":retrieved_titles,
            "hit":hit
        })

        hit_rate = hits / len(cases)

    return {
        "hit_rate":hit_rate,
        "results":results
    }