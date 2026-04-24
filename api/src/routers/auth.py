from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
import src.schemas.auth as auth_schema
import src.cruds.auth as user_crud
from src.core.security import verify_password, create_access_token

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

    # 4. JWTトークンの生成
    # トークンの中身(Payload)にユーザー名とIDを入れます。
    # 💡注意: user.idはUUID型なので、必ず str() で文字列に変換してから入れます！
    access_token = create_access_token(
        data={"sub": user.name, "user_id": str(user.id)}
    )

    # 5. レスポンスの返却
    # IssueのAPI仕様通り、{"token": "生成されたトークン文字列"} の形で返す
    return {"token": access_token}