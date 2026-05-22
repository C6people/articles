from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.database import get_db
from src.core.deps import get_current_user_id
from src.core.security import (verify_password, get_password_hash)
import src.schemas.auth as auth_schema
import src.cruds.auth_password as auth_password_crud
import src.cruds.user as user_crud


router = APIRouter()


# パスワード変更API
@router.patch("/password")
async def change_password(

    # request body
    request: auth_schema.PasswordChangeRequest,

    # DB接続
    db: AsyncSession = Depends(get_db),

    # JWTから user_id取得
    current_user_id: UUID = Depends(get_current_user_id)

):

    # user_idからユーザー取得
    current_user = await user_crud.get_user_by_id(
        db,
        current_user_id
    )

    # ユーザー存在確認
    if current_user is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ユーザーが存在しません"
        )

    # 現在パスワード確認
    is_valid = verify_password(

        request.current_password,

        current_user.password_hash
    )

    # パスワード不一致
    if not is_valid:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="現在のパスワードが正しくありません"
        )

    # 新パスワードをhash化
    hashed_password = get_password_hash(
        request.new_password
    )

    # DB更新
    await auth_password_crud.update_password(

        db,

        current_user,

        hashed_password
    )

    return {
        "message": "パスワード変更が完了しました"
    }