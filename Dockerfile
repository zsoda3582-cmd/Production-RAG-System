#1.选择Python基础环境
FROM python:3.11-slim

#2.设置容器内的工作目录
WORKDIR /app

#3.设置python运行环境
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#4.复制依赖清单
COPY requirements.txt .

#5.安装项目依赖
RUN pip install --no-cache-dir \
    torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt

#6.复制项目代码和文档
COPY . .

#7.声明服务端口
EXPOSE 8000

#8.启动FastAPI
CMD [ "uvicorn","api:app","--host","0.0.0.0","--port","8000" ]
