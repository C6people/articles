from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from src.database import Base


class ArticleComment(Base):

    # 既存テーブル
    __tablename__ = "article_comments"

    # カラム対応
    id = Column(Integer, primary_key=True)

    article_id = Column(
        Integer,
        ForeignKey("articles.id")
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    parent_id = Column(
        Integer,
        nullable=True
    )

    body = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    