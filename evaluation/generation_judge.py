import json
import os
from openai import OpenAI

client = OpenAI(
    api_key = os.environ["DEEPSEEK_API_KEY"],
    base_url = "https://api.deepseek.com",
    max_retries = 0
)

def judge_generation(record:dict)->dict:
    sources = "\n\n".join(
        f"[Source {chunk['source_id']}]\n"
        f"{chunk["content"]}"
        for chunk in record["retrieved_chunks"]
    )

    prompt = f"""
You are a strict RAG evaluation judge.

Evaluate the answer using ONLY the provided sources.

Question:
{record["question"]}

Answer:
{record["answer"]}

Sources:
{sources}

Evaluate two dimensions:

1. answer_faithfulness:
Are all factual claims in the answer supported by at least
one of the provided sources?

2. citation_faithfulness:
Does every cited [Source N] support the specific claim
associated with that citation?

Return ONLY valid JSON:
{{
  "answer_faithfulness": 0 or 1,
  "citation_faithfulness": 0 or 1,
  "reason": "Brief explanation"
}}

Scoring:
1 = all relevant claims pass
0 = at least one claim fails

For citation_faithfulness, missing citations for factual
claims also count as failure.
"""

    response = client.chat.completions.create(
        model = "deepseek-chat",
        messages = [
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature = 0,
        max_tokens = 512,
        timeout = 30,
        response_format = {
            "type":"json_object"
        }
    )

    return json.loads(response.choices[0].message.content)