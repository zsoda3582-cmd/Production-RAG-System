from rag.generation import generate_answer

question = "What is MCP?"

retrieved_chunks = [
    {
        "content":{
            "MCP is an open protocol that standardizes "
            "how applications provide context to LLMs."
        },
        "metadata":{
            "title":"Model Context Protocol"
        }
    }
]

answer = generate_answer(question,retrieved_chunks)

print("Question",question)
print("Answer",answer)