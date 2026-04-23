"""いいねモデル"""

import uuid
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint, UUID
from src.database import Base


class Like(Base):
    __tablename__ = "likes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    target_type = Column(String, nullable=False, comment="'article', 'article_comment', 'question', 'question_comment'")
    target_id = Column(UUID(as_uuid=True), nullable=False)

    # 同じユーザーが同じ対象に2回いいねできないようにする
    __table_args__ = (
        UniqueConstraint("user_id", "target_type", "target_id", name="uq_likes_user_target"),
    )
