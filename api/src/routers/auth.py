from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
import src.schemas.auth as auth_schema
import src.cruds.auth as auth_crud
from src.core.security import verify_password, create_access_token
import src.schemas.user as user_schema
import src.cruds.user as user_crud

router = APIRouter()

@router.post("/login")
async def login(
    request: auth_schema.LoginRequest, 
    db: AsyncSession = Depends(get_db)
):
    # 2. ユーザーの検索
    user = await auth_crud.get_user_by_name(db, name=request.name)
    
    # ユーザーが見つからない,またはパスワードが一致しない場合は 401 エラー
    if user is None or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザー名またはパスワードが正しくありません"
        )

    # 4. JWTトークンの生成
    # トークンの中身(Payload)にユーザー名とIDを入れます。
    access_token = create_access_token(
        data={"sub": user.name, "user_id": str(user.id)}
    )

    # 5. レスポンスの返却
    # IssueのAPI仕様通り、{"token": "生成されたトークン文字列"} の形で返す
    return {"token": access_token}


@router.post("/signup", response_model=user_schema.UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_in: user_schema.UserCreate, db: AsyncSession = Depends(get_db)):
    """
    ユーザーを新規登録します。
    """
    # 既に同じ学籍番号のユーザーが存在するかチェック
    user = await user_crud.get_user_by_name(db, name=user_in.name)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="この学籍番号（またはユーザー名）は既に登録されています。"
        )
    
    # 新規ユーザー作成
    created_user = await user_crud.create_user(db, user_in=user_in)
    return created_user
