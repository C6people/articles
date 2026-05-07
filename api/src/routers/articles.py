from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from src.database import get_db
import src.schemas.article as article_schema
import src.cruds.article as article_crud
from src.core.deps import get_current_user_id

router = APIRouter()

@router.get("/articles", response_model=List[article_schema.ArticleResponse])
async def read_articles(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    記事一覧を取得します。
    新しい順（降順）で返却します。
    """
    articles = await article_crud.get_articles(db, skip=skip, limit=limit)
    return articles

@router.get("/articles/{article_id}", response_model=article_schema.ArticleResponse)
async def read_article(article_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    指定されたIDの記事詳細を取得します。
    """
    article = await article_crud.get_article(db, article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="記事が見つかりません")
    return article

@router.post("/articles", response_model=article_schema.ArticleResponse, status_code=201)
async def create_article(article_in: article_schema.ArticleCreate,
                         db: AsyncSession = Depends(get_db),
                         user_id: UUID = Depends(get_current_user_id)):
    """
    新しい記事を作成します。
    """
    return await article_crud.create_article(db=db, article_in=article_in, user_id=user_id)
