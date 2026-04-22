from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base

app = FastAPI(
    title="Articles API",
    description="API for the Articles application",
    version="1.0.0",
)

# CORSの設定 (フロントエンドとの通信用)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開発環境用。本番ではフロントエンドのドメインを指定してください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    # 本番環境ではマイグレーションツール(alembic等)を使用しますが、
    # 開発用として起動時にテーブル作成を行うことも可能です(今回はmigrateツールがあるのでコメントアウト)
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    pass

@app.get("/")
async def read_root():
    return {"message": "Welcome to Articles API"}

@app.get("/ping")
async def ping():
    return {"status": "ok"}
