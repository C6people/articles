"""質問関連モデル"""

import uuid
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    
    user = relationship("User")

    @property
    def user_name(self):
        return self.user.name if self.user else None


class QuestionComment(Base):
    __tablename__ = "question_comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("question_comments.id", ondelete="CASCADE"), nullable=True, comment="返信先コメントID（NULLなら質問への直接コメント）")
    body = Column(Text, nullable=False)
    is_answer = Column(Boolean, nullable=False, default=False, comment="true: 回答 / false: コメント")
    is_best = Column(Boolean, nullable=False, default=False, comment="true: ベストアンサー")
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    user = relationship("User")

    @property
    def user_name(self):
        return self.user.name if self.user else None
