# SQLAlchemyのselectを使うためimport
from sqlalchemy import select

# 非同期DB接続用
from sqlalchemy.ext.asyncio import AsyncSession

# ArticleCommentsモデルのimport
from src.models.article_comments import ArticleComment


# 記事IDからコメント一覧を取得する関数
async def get_comments_by_article_id(

    # DBの接続情報
    db: AsyncSession,

    # URLから受け取る記事ID
    article_id: int
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