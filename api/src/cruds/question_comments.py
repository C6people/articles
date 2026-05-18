"""質問コメントCRUD"""

from sqlalchemy import select
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
