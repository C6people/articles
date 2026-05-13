from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.cruds.article_comments import get_comments_by_article_id
from src.schemas.article_comments import ArticleCommentResponse
router = APIRouter()
from uuid import UUID

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