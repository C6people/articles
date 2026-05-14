from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db

import src.schemas.article as article_schema
import src.cruds.article as article_crud

router = APIRouter()

@router.get(
    "/users/{user_id}/articles",
    response_model=list[article_schema.ArticleResponse]
)
async def get_user_articles(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    articles = await article_crud.get_articles_by_user_id(
        db,
        user_id
    )

    return articles