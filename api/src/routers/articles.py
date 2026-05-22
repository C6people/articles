from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from src.database import get_db
import src.schemas.article as article_schema
import src.cruds.article as article_crud
from src.core.deps import get_current_user_id, get_current_user_id_optional
from src.cruds.like import check_is_liked, get_user_liked_ids

router = APIRouter()

@router.get("/articles", response_model=List[article_schema.ArticleResponse])
async def read_articles(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db),
    current_user_id: Optional[UUID] = Depends(get_current_user_id_optional)
):
    """
    記事一覧を取得します。
    新しい順（降順）で返却します。
    """
    articles = await article_crud.get_articles(db, skip=skip, limit=limit)
    if current_user_id:
        liked_ids = await get_user_liked_ids(db, current_user_id, "article", [a.id for a in articles])
        for article in articles:
            article.is_liked = article.id in liked_ids
    else:
        for article in articles:
            article.is_liked = False
    return articles

@router.get("/articles/{article_id}", response_model=article_schema.ArticleResponse)
async def read_article(
    article_id: UUID, 
    db: AsyncSession = Depends(get_db),
    current_user_id: Optional[UUID] = Depends(get_current_user_id_optional)
):
    """
    指定されたIDの記事詳細を取得します。
    """
    article = await article_crud.get_article(db, article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="記事が見つかりません")
    
    if current_user_id:
        article.is_liked = await check_is_liked(db, current_user_id, "article", article_id)
    else:
        article.is_liked = False
    return article

@router.post("/articles", response_model=article_schema.ArticleResponse, status_code=201)
async def create_article(article_in: article_schema.ArticleCreate,
                         db: AsyncSession = Depends(get_db),
                         user_id: UUID = Depends(get_current_user_id)):
    """
    新しい記事を作成します。
    """
    article = await article_crud.create_article(db=db, article_in=article_in, user_id=user_id)
    article.is_liked = False
    return article

