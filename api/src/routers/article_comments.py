from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from src.database import get_db
from src.core.deps import get_current_user_id, get_current_user_id_optional
from src.cruds.article_comments import get_comments_by_article_id, create_comment
from src.cruds.like import check_is_liked, get_user_liked_ids
from src.schemas.article_comments import ArticleCommentResponse, CommentCreate

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
    db: AsyncSession = Depends(get_db),
    current_user_id: Optional[UUID] = Depends(get_current_user_id_optional)
):
    # CRUDを呼び出して結果返却
    comments = await get_comments_by_article_id(
        db,
        article_id
    )
    if current_user_id:
        liked_ids = await get_user_liked_ids(db, current_user_id, "article_comment", [c.id for c in comments])
        for comment in comments:
            comment.is_liked = comment.id in liked_ids
    else:
        for comment in comments:
            comment.is_liked = False
    return comments

# POST　API作成
@router.post(
    "/articles/{article_id}/comments",
    response_model=ArticleCommentResponse
)
async def post_comment(
    article_id: UUID,
    request: CommentCreate,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id) # ログインユーザーのIDを取得
):
    # modelの生成
    comment = await create_comment(
        db=db,
        article_id=article_id,       # URLから取得したものを使う
        user_id=user_id,
        body=request.body,
        parent_id=request.parent_id  # 追加
    )
    comment.is_liked = False
    return comment