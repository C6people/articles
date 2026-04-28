from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
import src.schemas.user as user_schema
import src.cruds.user as user_crud

router = APIRouter()

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
