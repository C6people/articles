"""いいねモデル"""

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from src.database import Base


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    target_type = Column(String, nullable=False, comment="'article', 'article_comment', 'question', 'question_comment'")
    target_id = Column(Integer, nullable=False)

    # 同じユーザーが同じ対象に2回いいねできないようにする
    __table_args__ = (
        UniqueConstraint("user_id", "target_type", "target_id", name="uq_likes_user_target"),
    )
