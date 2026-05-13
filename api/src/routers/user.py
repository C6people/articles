from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.database import get_db
from src.core.deps import get_current_user_id

import src.schemas.user as user_schema
import src.cruds.user as user_crud

router = APIRouter()


@router.get(
    "/users/me",
    response_model=user_schema.MyProfileResponse
)
async def get_my_profile(
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    user = await user_crud.get_user_by_id(
        db=db,
        user_id=user_id
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="ユーザーが見つかりません"
        )

    return user

@router.put(
    "/users/me",
    response_model=user_schema.MyProfileResponse
)
async def update_my_profile(
    profile_in: user_schema.MyProfileUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    user = await user_crud.get_user_by_id(
        db=db,
        user_id=user_id
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="ユーザーが見つかりません"
        )

    updated_user = await user_crud.update_my_profile(
        db=db,
        user=user,
        profile_in=profile_in
    )

    return updated_user