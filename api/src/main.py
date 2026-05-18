from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import articles, question, auth, user
from src.routers import article_comments
from src.routers import question_comments

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

# ルーターの登録
app.include_router(articles.router, tags=["articles"])
app.include_router(question.router, tags=["questions"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, tags=["users"])
app.include_router(article_comments.router, tags=["article_comments"])
app.include_router(question_comments.router, tags=["question_comments"])


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

