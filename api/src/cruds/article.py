from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from uuid import UUID

from src.models.article import Article
import src.schemas.article as article_schema

async def get_articles(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Article]:
    result = await db.execute(
        select(Article).options(selectinload(Article.user)).order_by(Article.created_at.desc()).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def get_article(db: AsyncSession, article_id: UUID) -> Article | None:
    result = await db.execute(
        select(Article).options(selectinload(Article.user)).where(Article.id == article_id)
    )
    return result.scalar_one_or_none()

async def create_article(db: AsyncSession, article_in: article_schema.ArticleCreate, user_id: UUID) -> Article:
    new_article = Article(
        title=article_in.title,
        body=article_in.body,
        category=article_in.category,
        user_id=user_id
    )
    db.add(new_article)
    await db.commit()
    await db.refresh(new_article)
    # Eagerly load the user so it can be returned safely
    result = await db.execute(select(Article).options(selectinload(Article.user)).where(Article.id == new_article.id))
    return result.scalar_one()

# user_idから記事を取得
async def get_articles_by_user_id(
    db: AsyncSession,
    user_id: UUID
):
    result = await db.execute(
        select(Article)
        .options(selectinload(Article.user))
        .where(Article.user_id == user_id)
        .order_by(Article.created_at.desc())
    )

    return result.scalars().all()