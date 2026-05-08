from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from uuid import UUID

from src.models.question import Question
import src.schemas.question as question_schema

async def get_questions(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Question]:
    result = await db.execute(
        select(Question).order_by(Question.created_at.desc()).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def get_question(db: AsyncSession, question_id: UUID) -> Question | None:
    result = await db.execute(select(Question).where(Question.id == question_id))
    return result.scalar_one_or_none()

async def create_question(db: AsyncSession, question_in: question_schema.QuestionCreate, user_id: UUID) -> Question:
    new_question = Question(
        title=question_in.title,
        body=question_in.body,
        user_id=user_id
    )
    db.add(new_question)
    await db.commit()
    await db.refresh(new_question)
    return new_question
