from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List
from datetime import datetime

from src.database import get_db
from src.models.article import Article

router = APIRouter()

# --- Pydantic Schemas ---
class ArticleCreate(BaseModel):
    title: str
    body: str
    # TODO: ログイン機能実装後は削除し、トークンから取得するように変更する
    user_id: int

class ArticleResponse(BaseModel):
    id: int
    user_id: int
    title: str
    body: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- API Endpoints ---

@router.get("/", response_model=List[ArticleResponse])
async def read_articles(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    記事一覧を取得します。
    新しい順（降順）で返却します。
    """
    result = await db.execute(
        select(Article).order_by(Article.created_at.desc()).offset(skip).limit(limit)
    )
    articles = result.scalars().all()
    return articles

@router.get("/{article_id}", response_model=ArticleResponse)
async def read_article(article_id: int, db: AsyncSession = Depends(get_db)):
    """
    指定されたIDの記事詳細を取得します。
    """
    result = await db.execute(select(Article).where(Article.id == article_id))
    article = result.scalar_one_or_none()
    
    if article is None:
        raise HTTPException(status_code=404, detail="記事が見つかりません")
    
    return article

@router.post("/", response_model=ArticleResponse, status_code=201)
async def create_article(article_in: ArticleCreate, db: AsyncSession = Depends(get_db)):
    """
    新しい記事を作成します。
    ※現在は暫定的にリクエストボディから user_id を受け取ります。
    """
    new_article = Article(
        title=article_in.title,
        body=article_in.body,
        user_id=article_in.user_id
    )
    db.add(new_article)
    await db.commit()
    await db.refresh(new_article)
    
    return new_article
