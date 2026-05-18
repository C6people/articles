"""質問コメントCRUD"""

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.question import QuestionComment
from uuid import UUID


async def get_comments_by_question_id(
    db: AsyncSession,
    question_id: UUID
):
    """質問IDからコメント一覧を取得"""
    result = await db.execute(
        select(QuestionComment)
        .where(QuestionComment.question_id == question_id)
    )
    return result.scalars().all()


async def create_comment(
    db: AsyncSession,
    question_id: UUID,
    user_id: UUID,
    body: str,
    parent_id: UUID | None = None,
    is_answer: bool = False,
):
    """質問へのコメントを作成"""
    comment = QuestionComment(
        question_id=question_id,
        user_id=user_id,
        parent_id=parent_id,
        body=body,
        is_answer=is_answer,
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def set_best_answer(
    db: AsyncSession,
    question_id: UUID,
    comment_id: UUID,
):
    """ベストアンサーを設定（既存のベストアンサーを解除してから設定）"""
    # 既存のベストアンサーを全て解除
    await db.execute(
        update(QuestionComment)
        .where(QuestionComment.question_id == question_id)
        .where(QuestionComment.is_best == True)
        .values(is_best=False)
    )
    # 新しいベストアンサーを設定
    await db.execute(
        update(QuestionComment)
        .where(QuestionComment.id == comment_id)
        .values(is_best=True)
    )
    await db.commit()

    # 更新後のコメントを返す
    result = await db.execute(
        select(QuestionComment)
        .where(QuestionComment.id == comment_id)
    )
    return result.scalar_one_or_none()
