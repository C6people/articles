from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
import src.schemas.auth as auth_schema
import src.cruds.auth as user_crud
from src.core.security import verify_password  # 作成したハッシュ照合の関数をインポート

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(
    request: auth_schema.LoginRequest, 
    db: AsyncSession = Depends(get_db)
):
    # 2. ユーザーの検索
    user = await user_crud.get_user_by_name(db, name=request.name)
    
    # ユーザーが見つからない,またはパスワードが一致しない場合は 401 エラー
    if user is None or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザー名またはパスワードが正しくありません"
        )

    # ユーザーが見つかった場合、この後のパスワード検証で user.password_hash を使い、
    # JWT生成で user.id (UUID) を使用します。
    return {
        "message": "User found",
        "user_id": str(user.id) # 型定義に基づいたUUID
    }