"""質問コメント用スキーマ"""

from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class QuestionCommentResponse(BaseModel):
    """質問コメントのレスポンス"""
    id: UUID
    question_id: UUID
    user_id: UUID
    parent_id: UUID | None = None
    body: str
    is_answer: bool
    is_best: bool
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionCommentCreate(BaseModel):
    """質問コメントの投稿用"""
    parent_id: UUID | None = None   # 親コメントのID（返信の場合）
    body: str                       # コメントの内容
    is_answer: bool = False         # 回答フラグ（デフォルトはコメント）
