"""ユーザーモデル"""

import uuid
from sqlalchemy import Column, String, UUID, Integer
from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True, comment="ユーザー名（ログイン用）")
    role = Column(String, nullable=False, comment="'student' または 'teacher'")
    password_hash = Column(String, nullable=False, comment="ハッシュ化されたパスワード")
    # ユーザー情報追加
    grade = Column(Integer, nullable=True, comment="学年（1〜4）")
    department = Column(String, nullable=True, comment="学科")
    course = Column(String, nullable=True, comment="コース")
    bio = Column(String, nullable=True, comment="自己紹介")