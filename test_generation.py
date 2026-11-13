from rag.generation import build_context

chunks = [
    {
        "content":"MCP is an open protocol.",
        "metadata":{
            "title":"Model Context Protocol"
        }
    }
]

context = build_context(chunks)
print(context)

# assert断言语句，用法：assert 条件，“失败时的提示信息”
assert "[Source 1]" in context  #要求 context 中必须包含 [Source 1]，否则就报错
assert "Title: Model Context Protocol" in context
assert "MCP is an open protocol." in context

print("PASS:Context Construction")