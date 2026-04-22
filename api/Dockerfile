FROM python:3.11-slim

WORKDIR /app

# 環境変数の設定 (Pythonがpycファイルを出力しないようにし、バッファリングを無効化)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 依存関係のインストール
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

# アプリケーションのコードをコピー
COPY . .

# Uvicornサーバーの起動コマンド (ホットリロード有効化)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0", "--port", "8000", "--reload"]
