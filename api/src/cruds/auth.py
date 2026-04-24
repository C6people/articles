from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.user import User # 定義済みのUserモデル

async def get_user_by_name(db: AsyncSession, name: str):
    # SELECT * FROM users WHERE name = :name
    result = await db.execute(select(User).filter(User.name == name))
    return result.scalars().first()