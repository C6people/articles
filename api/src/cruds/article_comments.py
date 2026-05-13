from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.article import ArticleComment
import uuid
async def get_comments_by_article_id(       # 記事IDからコメント一覧を取得する関数
    db: AsyncSession,
    article_id: uuid.UUID
):

    # SQL実行
    result = await db.execute(
        # ArticleCommentテーブルからデータを取得
        select(ArticleComment)
        # 場所は記事IDが一致するもの
        .where(ArticleComment.article_id == article_id)
    )
    # 結果を配列で返す
    return result.scalars().all()