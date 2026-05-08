"""記事関連モデル"""

import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, UUID
from sqlalchemy.sql import func
from src.database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    category = Column(String, nullable=False, default="その他")  # カテゴリを追加
    created_at = Column(DateTime, nullable=False, server_default=func.now())

class ArticleComment(Base):
    __tablename__ = "article_comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(UUID(as_uuid=True), ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("article_comments.id", ondelete="CASCADE"), nullable=True, comment="返信先コメントID（NULLなら記事への直接コメント）")
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
