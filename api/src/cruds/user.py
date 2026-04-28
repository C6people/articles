from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.user import User
import src.schemas.user as user_schema
from src.utils.security import get_password_hash

async def get_user_by_name(db: AsyncSession, name: str) -> User | None:
    """名前（学籍番号など）でユーザーを検索する"""
    result = await db.execute(select(User).where(User.name == name))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_in: user_schema.UserCreate) -> User:
    """新しいユーザーを作成する"""
    # パスワードをハッシュ化
    hashed_password = get_password_hash(user_in.password)
    
    new_user = User(
        name=user_in.name,
        password_hash=hashed_password,
        role="student"  # デフォルトは生徒
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user
