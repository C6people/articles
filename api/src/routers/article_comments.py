from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.cruds.article_comments import get_comments_by_article_id
from src.schemas.article_comments import ArticleCommentResponse
from src.schemas.article_comments import CommentCreate

from src.cruds.article_comments import (
    get_comments_by_article_id,
    create_comment
)
from uuid import UUID
router = APIRouter()

# GET API作成
@router.get(
    # API URL
    "/articles/{article_id}/comments",
    response_model=list[ArticleCommentResponse]
)

# コメント取得API
async def get_comments(
    # URLのarticle_idを受け取る
    article_id: UUID,
    # DB接続取得
    db: AsyncSession = Depends(get_db)
):

    # CRUDを呼び出して結果返却
    return await get_comments_by_article_id(
        db,
        article_id
    )

# POST　API作成
@router.post(
    "/",

    response_model=ArticleCommentResponse
)
async def post_comment(

    # request body
    request: CommentCreate,

    # DB
    db: AsyncSession = Depends(get_db)
):

    # 仮user_id
    # 後でJWTから取得
    user_id = 1

    comment = await create_comment(
        db=db,

        article_id=request.article_id,

        user_id=user_id,

        body=request.body
    )

    return comment