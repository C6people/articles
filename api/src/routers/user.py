from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.database import get_db
from src.core.deps import get_current_user_id
from src.models.user import User
import src.schemas.user as user_schema
import src.cruds.user as user_crud
import src.schemas.article as article_schema
import src.cruds.article as article_crud
import src.schemas.question as question_schema
import src.cruds.question as question_crud


router = APIRouter()


@router.get(
    "/users/me",
    response_model=user_schema.MyProfileResponse
)
async def get_my_profile(
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    user = await user_crud.get_user_by_id(
        db=db,
        user_id=user_id
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="ユーザーが見つかりません"
        )

    return user

@router.put(
    "/users/me",
    response_model=user_schema.MyProfileResponse
)
async def update_my_profile(
    profile_in: user_schema.MyProfileUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    user = await user_crud.get_user_by_id(
        db=db,
        user_id=user_id
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="ユーザーが見つかりません"
        )

    updated_user = await user_crud.update_my_profile(
        db=db,
        user=user,
        profile_in=profile_in
    )

    return updated_user

@router.get(
    "/users/{user_id}",
    response_model=user_schema.MyProfileResponse
)
async def get_user_profile(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    user = await user_crud.get_user_by_id(
        db=db,
        user_id=user_id
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="ユーザーが見つかりません"
        )

    return user

# user_idから記事を取得
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

# user_idから質問を取得
@router.get(
    "/users/{user_id}/questions",
    response_model=list[question_schema.QuestionResponse]
)
async def get_user_questions(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    questions = await question_crud.get_questions_by_user_id(
        db,
        user_id
    )

    return questions


# user_idからユーザー情報取得
async def get_user_by_id(

    db: AsyncSession,

    user_id: UUID

):

    result = await db.execute(  # ユーザー情報を取得
        select(User).where(
            User.id == user_id
        )
    )

    return result.scalar_one_or_none()  # user_idに該当するユーザーがいない場合はNoneを返す