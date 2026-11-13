#用现有的generation_records.jsonl
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from evaluation.generation_judge import judge_generation

# 读取已有的真实评测记录
path = Path("evaluation/generation_records.jsonl")

with path.open("r",encoding = "utf-8")as f:
    record = json.loads(f.readline()) #只读取第一行

# 保留原始问题和检索证据，故意篡改回答
record["answer"] = (
    "MCP is a database developed by Microsoft "
    "for storing relational data [Source 1]."
)

result = judge_generation(record)

print("Question:",record["question"])
print("Judge Result:",result)