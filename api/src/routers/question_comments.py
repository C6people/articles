"""質問コメントルーター"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.database import get_db
from src.core.deps import get_current_user_id
import src.cruds.question_comments as qc_crud
import src.cruds.question as question_crud
import src.schemas.question_comments as qc_schema

router = APIRouter()


@router.get(
    "/questions/{question_id}/comments",
    response_model=list[qc_schema.QuestionCommentResponse],
)
async def get_comments(
    question_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """質問に対するコメント一覧を取得"""
    return await qc_crud.get_comments_by_question_id(db, question_id)


@router.post(
    "/questions/{question_id}/comments",
    response_model=qc_schema.QuestionCommentResponse,
)
async def post_comment(
    question_id: UUID,
    request: qc_schema.QuestionCommentCreate,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id),
):
    """質問にコメントを投稿"""
    return await qc_crud.create_comment(
        db=db,
        question_id=question_id,
        user_id=user_id,
        body=request.body,
        parent_id=request.parent_id,
        is_answer=request.is_answer,
    )


@router.patch(
    "/questions/{question_id}/comments/{comment_id}/best",
    response_model=qc_schema.QuestionCommentResponse,
)
async def toggle_best_answer(
    question_id: UUID,
    comment_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id),
):
    """ベストアンサーを設定（質問の投稿者のみ）"""
    # 質問の投稿者かチェック
    question = await question_crud.get_question(db, question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="質問が見つかりません")
    if question.user_id != user_id:
        raise HTTPException(status_code=403, detail="ベストアンサーは質問の投稿者のみ設定できます")

    result = await qc_crud.set_best_answer(db, question_id, comment_id)
    if result is None:
        raise HTTPException(status_code=404, detail="コメントが見つかりません")
    return result
