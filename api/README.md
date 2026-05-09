# Articles API (Backend)

このディレクトリは、プログラミング情報共有アプリケーションのバックエンド（API）のソースコードを含んでいます。
Pythonフレームワークの **FastAPI** を使用して構築されています。

## 技術スタック
- **フレームワーク**: FastAPI
- **データベース**: PostgreSQL
- **ORM**: SQLAlchemy (非同期)
- **マイグレーション**: Alembic
- **サーバー**: Uvicorn
- **認証**: JWT (PyJWT) + bcryptパスワードハッシュ

---

## 主要パッケージ

### requirements.txt (本番で必要)
| パッケージ | 用途 |
|-----------|------|
| `fastapi` | WebフレームワークAPI |
| `uvicorn[standard]` | ASGIサーバー |
| `sqlalchemy` | ORM（データベース操作） |
| `asyncpg` | PostgreSQL非同期ドライバ |
| `psycopg2-binary` | PostgreSQL同期ドライバ（Alembic用） |
| `alembic` | データベースマイグレーション |
| `PyJWT` | JWTトークンの生成・検証 |
| `passlib[bcrypt]` | パスワードハッシュ化 |
| `bcrypt` | bcryptアルゴリズム実装 |

### requirements-dev.txt (開発時のみ)
| パッケージ | 用途 |
|-----------|------|
| `ruff` | コードフォーマッター・リンター |
| `pytest` | テストフレームワーク |
| `pytest-asyncio` | 非同期テストサポート |
| `httpx` | テスト用HTTPクライアント |

---

## ディレクトリ構成

```text
api/
├── alembic/                # データベースマイグレーションファイル群
│   └── versions/           # 各マイグレーションスクリプト
├── src/                    # アプリケーションのソースコード
│   ├── core/               # 認証・セキュリティ関連
│   │   ├── security.py     # パスワードハッシュ化・JWTトークン生成
│   │   └── deps.py         # JWTトークンからuser_idを取り出す依存関数
│   ├── cruds/              # データベース操作（CRUD処理）
│   │   ├── article.py      # 記事のCRUD
│   │   ├── question.py     # 質問のCRUD
│   │   ├── auth.py         # 認証用のユーザー検索
│   │   └── user.py         # ユーザーのCRUD
│   ├── models/             # テーブル定義（SQLAlchemyモデル）
│   │   ├── article.py      # Article, ArticleComment モデル
│   │   ├── question.py     # Question, QuestionComment モデル
│   │   ├── user.py         # User モデル
│   │   └── like.py         # Like モデル
│   ├── routers/            # APIエンドポイントのルーティング
│   │   ├── articles.py     # /articles エンドポイント
│   │   ├── question.py     # /questions エンドポイント
│   │   └── auth.py         # /auth/login, /auth/signup エンドポイント
│   ├── schemas/            # データ型の定義（Pydanticモデル）
│   │   ├── article.py      # ArticleCreate, ArticleResponse
│   │   ├── question.py     # QuestionCreate, QuestionResponse
│   │   ├── user.py         # UserCreate, UserResponse
│   │   └── auth.py         # LoginRequest
│   ├── database.py         # データベース接続設定
│   └── main.py             # アプリケーションのエントリポイント
├── docker-compose.yml      # Dockerコンテナの構成設定
├── Dockerfile              # バックエンド用Dockerイメージの構築手順
├── alembic.ini             # Alembicの設定ファイル
├── requirements.txt        # 必要なPythonパッケージ一覧
└── requirements-dev.txt    # 開発用追加パッケージ
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
2. 環境変数ファイルを作成します（初回のみ）。
   ```bash
   cp .env.example .env
   ```
3. Docker Composeを使ってバックグラウンドで起動します。
   ```bash
   docker compose up -d --build
   ```
4. データベースのマイグレーションを実行します。
   ```bash
   docker exec baymux-api alembic upgrade head
   ```
5. コンテナを停止したい場合は以下のコマンドを実行します。
   ```bash
   docker compose down
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

---

## 認証フロー

1. **ユーザー登録**: `POST /auth/signup` でユーザー名とパスワードを送信（パスワードはbcryptでハッシュ化して保存）
2. **ログイン**: `POST /auth/login` でユーザー名とパスワードを送信 → JWTトークンが返却される
3. **認証が必要なAPI**: `Authorization: Bearer <token>` ヘッダーを付けてリクエストを送信
4. **トークン検証**: `core/deps.py` の `get_current_user_id` がトークンを検証し、`user_id` を取り出してAPI関数に渡す
