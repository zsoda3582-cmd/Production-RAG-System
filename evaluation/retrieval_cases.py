# RETRIEVAL_CASES = [
#     {
#         "question": "What is an agent?",
#         "expected_titles": ["Agents"]
#     },
#     {
#         "question": "What is middleware in LangChain?",
#         "expected_titles": ["Middleware overview"]
#     },
#     {
#         "question": "What are multi-agent systems?",
#         "expected_titles": ["Multi-agent"]
#     },
#     {
#         "question": "How do subagents work?",
#         "expected_titles": ["Subagents"]
#     },
#     {
#         "question": "How does long-term memory work?",
#         "expected_titles": ["Long-term memory"]
#     },
#     {
#         "question": "What is Model Context Protocol?",
#         "expected_titles": ["Model Context Protocol (MCP)"]
#     },
# ]


RETRIEVAL_CASES = [
    # 1. Concepts
    {
        "question": "What is an agent in LangChain?",
        "expected_titles": ["Agents"]
    },
    {
        "question": "What is middleware in LangChain?",
        "expected_titles": ["Middleware overview"]
    },
    {
        "question": "What are multi-agent systems?",
        "expected_titles": ["Multi-agent"]
    },
    {
        "question": "What is Model Context Protocol (MCP)?",
        "expected_titles": ["Model Context Protocol (MCP)"]
    },
    {
        "question": "What are tools in LangChain?",
        "expected_titles": ["Tools"]
    },
    {
        "question": "What is structured output in LangChain?",
        "expected_titles": ["Structured output"]
    },
    {
        "question": "What is runtime context in LangChain?",
        "expected_titles": ["Runtime"]
    },
    {
        "question": "What is LangSmith Observability?",
        "expected_titles": ["LangSmith Observability"]
    },

    # 2. Mechanisms
    {
        "question": "How do subagents work?",
        "expected_titles": ["Subagents"]
    },
    {
        "question": "How does long-term memory work?",
        "expected_titles": ["Long-term memory"]
    },
    {
        "question": "How does short-term memory work in an agent?",
        "expected_titles": ["Short-term memory"]
    },
    {
        "question": "How does tool calling work with language models?",
        "expected_titles": ["Tool calling"]
    },
    {
        "question": "How does streaming work in LangChain?",
        "expected_titles": ["Streaming"]
    },
    {
        "question": "How does human-in-the-loop work in LangChain?",
        "expected_titles": ["Human-in-the-Loop", "Human-in-the-loop"]
    },
    {
        "question": "How do handoffs work in multi-agent systems?",
        "expected_titles": ["Handoffs"]
    },
    {
        "question": "How does a router select between different agents?",
        "expected_titles": ["Router"]
    },
    {
        "question": "How does context engineering improve agent behavior?",
        "expected_titles": ["Context engineering in agents"]
    },
    {
        "question": "How do guardrails control agent behavior?",
        "expected_titles": ["Guardrails"]
    },

    # 3. Implementation
    {
        "question": "How do I install LangChain?",
        "expected_titles": ["Install LangChain"]
    },
    {
        "question": "How do I build a SQL agent using LangChain?",
        "expected_titles": ["Build a SQL agent"]
    },
    {
        "question": "How do I build a semantic search engine with LangChain?",
        "expected_titles": ["Build a semantic search engine with LangChain"]
    },
    {
        "question": "How do I create custom middleware?",
        "expected_titles": ["Custom middleware"]
    },
    {
        "question": "How do I build a custom agent workflow?",
        "expected_titles": ["Custom workflow"]
    },
    {
        "question": "How do I build a personal assistant using subagents?",
        "expected_titles": ["Build a personal assistant with subagents"]
    },
    {
        "question": "How do I build a multi-source knowledge base with routing?",
        "expected_titles": ["Build a multi-source knowledge base with routing"]
    },
    {
        "question": "How do I deploy a LangChain application?",
        "expected_titles": ["Deployment"]
    },
    {
        "question": "How do I write unit tests for LangChain applications?",
        "expected_titles": ["Unit testing"]
    },
    {
        "question": "How do I perform integration testing?",
        "expected_titles": ["Integration testing"]
    },

    # 4. Comparison and design
    {
        "question": "What is the difference between short-term and long-term memory?",
        "expected_titles": ["Short-term memory", "Long-term memory"]
    },
    {
        "question": "When should I use a multi-agent architecture?",
        "expected_titles": ["Multi-agent"]
    },
    {
        "question": "What is the difference between built-in and custom middleware?",
        "expected_titles": ["Prebuilt middleware", "Custom middleware"]
    },
    {
        "question": "When should I use structured output instead of plain text?",
        "expected_titles": ["Structured output"]
    },
    {
        "question": "How do models and tools interact in an agent?",
        "expected_titles": ["Agents", "Tools", "Tool calling"]
    },

    # 5. Errors and reliability
    {
        "question": "How do I fix an INVALID_PROMPT_INPUT error?",
        "expected_titles": ["INVALID_PROMPT_INPUT"]
    },
    {
        "question": "What causes INVALID_TOOL_RESULTS errors?",
        "expected_titles": ["INVALID_TOOL_RESULTS"]
    },
    {
        "question": "How do I handle MODEL_RATE_LIMIT errors?",
        "expected_titles": ["MODEL_RATE_LIMIT"]
    },
    {
        "question": "How do I resolve MODEL_AUTHENTICATION errors?",
        "expected_titles": ["MODEL_AUTHENTICATION"]
    },
    {
        "question": "What causes OUTPUT_PARSING_FAILURE?",
        "expected_titles": ["OUTPUT_PARSING_FAILURE"]
    },
    {
        "question": "How do I evaluate an agent's performance?",
        "expected_titles": ["Agent Evals"]
    },
    {
        "question": "How can I debug agents using LangSmith Studio?",
        "expected_titles": ["LangSmith Studio"]
    }
]
