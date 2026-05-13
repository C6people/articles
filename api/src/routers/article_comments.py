# APIルーター機能
from fastapi import APIRouter, Depends

# 非同期DB接続
from sqlalchemy.ext.asyncio import AsyncSession

# DB接続関数
from src.database import get_db

# CRUD関数
from src.cruds.article_comments import get_comments_by_article_id

# レスポンスSchema
from src.schemas.article_comments import ArticleCommentResponse


# ルーター作成
router = APIRouter()


# GET API作成
@router.get(

    # API URL
    "/articles/{article_id}/comments",

    # レスポンス型指定
    response_model=list[ArticleCommentResponse]
)

# コメント取得API
async def get_comments(

    # URLのarticle_idを受け取る
    article_id: int,

    # DB接続取得
    db: AsyncSession = Depends(get_db)
):

    # CRUDを呼び出して結果返却
    return await get_comments_by_article_id(
        db,
        article_id
    )