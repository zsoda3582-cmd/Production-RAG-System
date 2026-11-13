import json
from pathlib import Path
from evaluation.generation_judge import judge_generation

def save_generation_record(
        question:str,
        answer:str,
        retrieved_chunks:list[dict],
        output_path:str = "evaluation/generation_records.jsonl"#jsonl:每一行保存一条独立的json记录
):
    record = {
        "question":question,
        "answer":answer,
        "retrieved_chunks":[
            {
                "source_id":i,
                "title":chunk["metadata"]["title"],
                "content":chunk["content"],
                "score":float(chunk["score"])
            }
            for i,chunk in enumerate(retrieved_chunks,start = 1)
        ]
    }

    path = Path(output_path) #Path()函数：把output_path代表的这个字符串转换成一个Path路径对象，但它不能真正创建一个文件，只是构造一个表示路径的对象
    path.parent.mkdir(parents=True,exist_ok=True)

    with path.open("a",encoding="utf-8")as f: #“a”=append,追加
        f.write(json.dumps(record,ensure_ascii=False)+"\n")

def run_generation_evaluation(
        input_path = "evaluation/generation_records.jsonl",
        output_path = "evaluation/generation_results.jsonl"
):
    #读取之前保存的问答记录
    records = [
        json.loads(line)
        for line in Path(input_path).read_text(encoding = "utf-8").splitlines()
        if line.strip()
    ]

    results = []

    for i,record in enumerate(records,start=1):
        #调用LLM Judge
        judgement = judge_generation(record)

        result = {
            "question":record["question"],
            "answer":record["answer"],
            **judgement
        }

        results.append(result)

        print(
            f"[{i}/{len(records)}]"
            f"Answer={judgement['answer_faithfulness']}"
            f"Citation={judgement['citation_faithfulness']}"
        )

    #保存评测结果
    output = Path(output_path)
    output.parent.mkdir(parents=True,exist_ok=True)

    with output.open("w",encoding="utf-8")as f:#"w"会覆盖上次的评测结果
        for result in results:
            f.write(json.dumps(result,ensure_ascii=False))

    #统计整体指标
    if not results:
        return {
            "count":0,
            "answer_faithfulness":None,
            "citation_faithfulness":None
        }

    summary = {
    "count": len(results),
    "answer_faithfulness_rate": sum(
        result["answer_faithfulness"] for result in results
    ) / len(results),
    "citation_faithfulness_rate": sum(
        result["citation_faithfulness"] for result in results
    ) / len(results)
}

    return summary
