from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List
from datetime import datetime

from src.database import get_db
from src.models.question import Question

router = APIRouter()

# --- Pydantic Schemas ---
class QuestionCreate(BaseModel):
    title: str
    body: str
    # TODO: ログイン機能実装後は削除し、トークンから取得するように変更する
    user_id: int

class QuestionResponse(BaseModel):
    id: int
    user_id: int
    title: str
    body: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- API Endpoints ---

@router.get("/", response_model=List[QuestionResponse])
async def read_questions(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    質問一覧を取得します。
    新しい順（降順）で返却します。
    """
    result = await db.execute(
        select(Question).order_by(Question.created_at.desc()).offset(skip).limit(limit)
    )
    questions = result.scalars().all()
    return questions

@router.get("/{question_id}", response_model=QuestionResponse)
async def read_question(question_id: int, db: AsyncSession = Depends(get_db)):
    """
    指定されたIDの質問詳細を取得します。
    """
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    
    if question is None:
        raise HTTPException(status_code=404, detail="質問が見つかりません")
    
    return question

@router.post("/", response_model=QuestionResponse, status_code=201)
async def create_question(question_in: QuestionCreate, db: AsyncSession = Depends(get_db)):
    """
    新しい質問を作成します。
    ※現在は暫定的にリクエストボディから user_id を受け取ります。
    """
    new_question = Question(
        title=question_in.title,
        body=question_in.body,
        user_id=question_in.user_id
    )
    db.add(new_question)
    await db.commit()
    await db.refresh(new_question)
    
    return new_question
