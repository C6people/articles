# Articles API (Backend)

このディレクトリは、記事共有アプリケーションのバックエンド（API）のソースコードを含んでいます。
Pythonフレームワークの **FastAPI** を使用して構築されています。

## 技術スタック
- **フレームワーク**: FastAPI
- **データベース**: PostgreSQL
- **ORM**: SQLAlchemy (非同期)
- **マイグレーション**: Alembic
- **サーバー**: Uvicorn

---

## ディレクトリ構成

```text
api/
├── alembic/            # データベースマイグレーションファイル群
├── src/                # アプリケーションのソースコード
│   ├── cruds/          # データベース操作（CRUD処理）
│   ├── models/         # テーブル定義（SQLAlchemyモデル）
│   ├── routers/        # APIエンドポイントのルーティング
│   ├── schemas/        # データ型の定義とバリデーション（Pydanticモデル）
│   ├── database.py     # データベース接続設定
│   └── main.py         # アプリケーションのエントリポイント
├── docker-compose.yml  # Dockerコンテナの構成設定
├── Dockerfile          # バックエンド用Dockerイメージの構築手順
├── alembic.ini         # Alembicの設定ファイル
└── requirements.txt    # 必要なPythonパッケージ一覧
```

---

## 開発環境のセットアップと起動方法

バックエンドの起動には、**Dockerを使用する方法** と **ローカル環境で直接起動する方法** の2通りがあります。

### 1. Dockerを使用して起動する（推奨）
データベース（PostgreSQL）とAPIサーバーをまとめて立ち上げることができるため、こちらが一番簡単です。

1. ターミナルで `api/` ディレクトリに移動します。
   ```bash
   cd api
   ```
2. Docker Composeを使ってバックグラウンドで起動します。
   ```bash
   docker-compose up -d
   ```
3. コンテナを停止したい場合は以下のコマンドを実行します。
   ```bash
   docker-compose down
   ```

### 2. ローカル環境で直接起動する
Pythonをローカルにインストールしており、コードの変更を即座に反映させながら開発したい場合はこちらを使用します。（※別途データベースが起動している必要があります）

1. `api/` ディレクトリに移動します。
   ```bash
   cd api
   ```
2. （任意）仮想環境を作成して有効化します。
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linuxの場合
   ```
3. 必要なライブラリをインストールします。
   ```bash
   pip install -r requirements.txt
   ```
4. 開発用サーバー（Uvicorn）を起動します。
   ```bash
   uvicorn src.main:app --reload
   ```

---

## データベースのマイグレーション（Alembic）

データベースの構造（テーブルやカラム）を変更した場合は、以下の手順でデータベースに変更を反映させます。
※コマンドは `api/` ディレクトリ内で実行します。

1. **マイグレーションファイルの生成**（モデルを変更した場合）
   ```bash
   # 例: "Add new column" という名前で変更履歴を作成
   docker exec baymux-api alembic revision --autogenerate -m "Add new column"
   ```
2. **データベースへの反映**
   ```bash
   docker exec baymux-api alembic upgrade head
   ```

---

## API仕様書 (Swagger UI)

サーバー起動後、ブラウザで以下のURLにアクセスすると、自動生成されたインタラクティブなAPIドキュメント（Swagger UI）を閲覧・テストできます。

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

ここで直接APIを叩いて動作確認をすることが可能です。
