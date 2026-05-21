from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.database import get_db
from src.core.deps import get_current_user_id
import src.cruds.like as like_crud
from src.schemas.like import LikeResponse, LikedContentsResponse

router = APIRouter()

@router.post("/articles/{article_id}/likes", response_model=LikeResponse)
async def like_article(
    article_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    likes_count = await like_crud.create_like(db, "article", article_id, user_id)
    return LikeResponse(message="記事にいいねしました", likes_count=likes_count)


@router.post("/questions/{question_id}/likes", response_model=LikeResponse)
async def like_question(
    question_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    likes_count = await like_crud.create_like(db, "question", question_id, user_id)
    return LikeResponse(message="質問にいいねしました", likes_count=likes_count)


@router.post("/article-comments/{comment_id}/likes", response_model=LikeResponse)
async def like_article_comment(
    comment_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    likes_count = await like_crud.create_like(db, "article_comment", comment_id, user_id)
    return LikeResponse(message="記事のコメントにいいねしました", likes_count=likes_count)


@router.post("/question-comments/{comment_id}/likes", response_model=LikeResponse)
async def like_question_comment(
    comment_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    likes_count = await like_crud.create_like(db, "question_comment", comment_id, user_id)
    return LikeResponse(message="質問のコメントにいいねしました", likes_count=likes_count)

@router.get(
    "/users/me/likes",
    response_model=LikedContentsResponse
)
async def get_my_likes(
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    articles = await like_crud.get_liked_articles(
        db,
        user_id
    )

    questions = await like_crud.get_liked_questions(
        db,
        user_id
    )

    return {
        "articles": articles,
        "questions": questions
    }