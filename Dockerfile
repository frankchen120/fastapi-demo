FROM python:3.11-slim

# 不產生 .pyc，log 直接輸出
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 系統套件（給 psycopg2 / bcrypt 用）
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 先裝套件（利用 Docker layer cache）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再 copy 專案（避免每次改 code 都重裝套件）
COPY . .

# 對外開 port（文件用途）
EXPOSE 8000

# 啟動 FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
