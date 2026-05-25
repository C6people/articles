from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from src.database import get_db
import src.schemas.question as question_schema
import src.cruds.question as question_crud
from src.core.deps import get_current_user_id, get_current_user_id_optional
from src.cruds.like import check_is_liked, get_user_liked_ids

router = APIRouter()

@router.get("/questions", response_model=List[question_schema.QuestionResponse])
async def read_questions(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db),
    current_user_id: Optional[UUID] = Depends(get_current_user_id_optional)
):
    """
    質問一覧を取得します。
    新しい順（降順）で返却します。
    """
    questions = await question_crud.get_questions(db, skip=skip, limit=limit)
    if current_user_id:
        liked_ids = await get_user_liked_ids(db, current_user_id, "question", [q.id for q in questions])
        for question in questions:
            question.is_liked = question.id in liked_ids
    else:
        for question in questions:
            question.is_liked = False
    return questions

@router.get("/questions/{question_id}", response_model=question_schema.QuestionResponse)
async def read_question(
    question_id: UUID, 
    db: AsyncSession = Depends(get_db),
    current_user_id: Optional[UUID] = Depends(get_current_user_id_optional)
):
    """
    指定されたIDの質問詳細を取得します。
    """
    question = await question_crud.get_question(db, question_id=question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="質問が見つかりません")
    
    if current_user_id:
        question.is_liked = await check_is_liked(db, current_user_id, "question", question_id)
    else:
        question.is_liked = False
    return question

@router.post("/questions", response_model=question_schema.QuestionResponse, status_code=201)
async def create_question(question_in: question_schema.QuestionCreate, 
                          db: AsyncSession = Depends(get_db),
                          user_id: UUID = Depends(get_current_user_id)):
    """
    新しい質問を作成します。
    """
    question = await question_crud.create_question(db=db, question_in=question_in, user_id=user_id)
    question.is_liked = False
    return question

