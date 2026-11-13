from pathlib import Path
import frontmatter #一个专门解析 Markdown/MDX frontmatter 的工具,可以自动切割源数据（metadata）和文本（content）
import re

def clean_mdx_content(content:str)->str:
    content = re.sub(
        r"import\s+.*?;\s*$", #正则表达式，逐行找以“import”开头，以“；”结束的行并删除
        "",
        content,
        flags=re.MULTILINE
    )
    return content.strip()

def load_documents(document_dir:str)->list[dict]:
    document_path = Path(document_dir)
    documents = []

    for file_path in document_path.rglob("*.mdx"):
        post = frontmatter.load(file_path)

        document = {
            "content":clean_mdx_content(post.content),
            "metadata":{
                "source":str(file_path),
                "title":post.metadata.get("title",file_path.stem),
                "url":post.metadata.get("url")
            }
        }

        documents.append(document)

    return documents