# Articles Project

This project contains a Vue 3 frontend and a FastAPI backend with PostgreSQL.

## チーム開発用セットアップガイド

リポジトリを `git clone` した後の手順です。

### 1. 環境変数の設定
`api` ディレクトリにある `.env.example` をコピーして `.env` ファイルを作成してください。
(※基本的にはコピーするだけでローカル開発用に動作します)
```bash
cd api
cp .env.example .env
```

### 2. バックエンド & DB の起動 (Docker Compose)
Dockerを利用して、FastAPIサーバーとPostgreSQLデータベースを立ち上げます。
```bash
# apiディレクトリにいることを確認
docker compose up -d --build
```
起動が完了すると、以下のURLでAPIのドキュメント(Swagger UI)にアクセスできます。
- API Docs: http://localhost:8000/docs

### 3. フロントエンドの起動
別ターミナルを開き、フロントエンド(`app`ディレクトリ)の依存パッケージをインストールしてサーバーを起動します。
```bash
cd app
npm install
npm run dev
```
起動後、コンソールに表示されるローカルサーバーのURL (例: `http://localhost:5173`) にアクセスしてください。

## 開発用Tips
- **FastAPIのホットリロード**: `api/src/` 以下のファイルを変更すると、自動でAPIサーバーがリロードされます。
- **パッケージの追加**: Pythonパッケージを追加した場合は `api/requirements.txt` (または `requirements-dev.txt`) に追記し、`docker compose up -d --build` で再ビルドしてください。
