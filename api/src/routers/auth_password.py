from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.deps import get_current_user
from src.core.security import (verify_password,get_password_hash)
import src.schemas.auth as auth_schema
import src.cruds.auth_password as auth_password_crud


router = APIRouter()


# パスワード変更API
@router.patch("/password")
async def change_password(

    # request body
    request: auth_schema.PasswordChangeRequest,

    # DB接続
    db: AsyncSession = Depends(get_db),

    # JWTログインユーザー取得
    current_user: User = Depends(get_current_user)
):

    is_valid = verify_password(  # 現在PWを確認

        request.current_password,
        current_user.password_hash
    )

    if not is_valid:    #現在PW違う時はエラー表示


        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="現在のパスワードが正しくありません"
        )

    # 新PW hash化
    hashed_password = get_password_hash(
        request.new_password
    )

    await auth_password_crud.update_password(       # パスワード更新
        db,
        current_user,
        hashed_password
    )

    return {"message": "パスワードが変更されました"}    # 成功メッセを返す