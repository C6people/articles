from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User


# パスワード変更
async def update_password(

    db: AsyncSession,

    user: User,

    hashed_password: str
):

    # パスワード更新
    user.password_hash = hashed_password

    # DB保存
    await db.commit()

    # 最新化
    await db.refresh(user)

    return user
    