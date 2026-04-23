"""ユーザーモデル"""

from sqlalchemy import Column, Integer, String
from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, comment="ユーザー名（ログイン用）")
    role = Column(String, nullable=False, comment="'student' または 'teacher'")
    password_hash = Column(String, nullable=False, comment="ハッシュ化されたパスワード")
