import streamlit as st
import requests

API_URL = "http://127.0.0.1:8001/ask"

st.set_page_config(page_title="Production RAG",page_icon="📚")

st.title("📚 Production RAG System")
st.write("Ask questions about Langchain documentation.")

question = st.text_input("Your question",placeholder="What is MCP?")
#st.text_input():负责在网页上创建一个输入框，并获取用户输入的问题

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching and generating answer..."):
            try:
                response = requests.post( #类似于之前在S哇嘎个人UI中执行的POST/ask请求是同一件事，现在由python代码自动发送thhp请求
                    API_URL,
                    json = {"question":question},
                    timeout=120
                )
                response.raise_for_status()
                result = response.json()

                st.subheader("Answer")
                st.markdown(result["answer"]) #将fastapi返回的json中的answer提取出来，显示在网页上

                st.subheader("Retrieved Sources")
                for source in result["sources"]:
                    st.write(
                        f"[Source{source['source_id']}]"
                        f"{source['title']}"
                        f"(score:{source['score']:.3f})"
                    )

            except requests.RequestException as error:
                st.error(f"API request failed:{error}")
