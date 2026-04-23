"""質問関連モデル"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from src.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class QuestionComment(Base):
    __tablename__ = "question_comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(Integer, ForeignKey("question_comments.id", ondelete="CASCADE"), nullable=True, comment="返信先コメントID（NULLなら質問への直接コメント）")
    body = Column(Text, nullable=False)
    is_answer = Column(Boolean, nullable=False, default=False, comment="true: 回答 / false: コメント")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
