from pydantic import BaseModel
from uuid import UUID

class UserCreate(BaseModel):
    name: str
    password: str

class UserResponse(BaseModel):
    id: UUID
    name: str
    role: str

    class Config:
        from_attributes = True

class MyProfileResponse(BaseModel):
    name: str
    bio: str | None

    class Config:
        from_attributes = True

class MyProfileUpdate(BaseModel):
    bio: str | None