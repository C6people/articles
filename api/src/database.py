import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Docker環境変数からDATABASE_URLを取得
# デフォルト値はローカル開発用を想定していますが、基本は環境変数から読み込みます
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://articles_user:articles_password@localhost:5432/articles_db"
)

# 非同期エンジンの作成
engine = create_async_engine(
    DATABASE_URL,
    echo=True, # 開発中はSQLクエリを出力（本番ではFalseに）
)

# 非同期セッションファクトリ
AsyncSessionLocal = async_sessionmaker(
    engine, 
    expire_on_commit=False
)

# モデルのベースクラス
Base = declarative_base()

# DBセッションを取得するための依存関数(Dependency Injection)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
