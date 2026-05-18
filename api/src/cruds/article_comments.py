from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.models.article import ArticleComment
from uuid import UUID

async def get_comments_by_article_id(       # 記事IDからコメント一覧を取得する関数
    db: AsyncSession,
    article_id: UUID
):

    # SQL実行
    result = await db.execute(
        # ArticleCommentテーブルからデータを取得
        select(ArticleComment)
        .options(selectinload(ArticleComment.user))
        # 場所は記事IDが一致するもの
        .where(ArticleComment.article_id == article_id)
    )
    # 結果を配列で返す
    return result.scalars().all()

async def create_comment(   # コメント作成
    db: AsyncSession,
    article_id: UUID,
    user_id:    UUID,
    body:       str,
    parent_id:  UUID | None = None,
):

    # model生成
    comment = ArticleComment(
        article_id=article_id,
        user_id=user_id,
        parent_id=parent_id,
        body=body
    )

    # DB追加
    db.add(comment)

    # 保存
    await db.commit()

    # userをeager loadして返す
    result = await db.execute(
        select(ArticleComment)
        .options(selectinload(ArticleComment.user))
        .where(ArticleComment.id == comment.id)
    )
    return result.scalar_one()