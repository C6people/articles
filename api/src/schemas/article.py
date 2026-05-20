from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class ArticleCreate(BaseModel):
    title: str
    body: str
    category: str

class ArticleResponse(BaseModel):
    id: UUID
    user_id: UUID
    user_name: str | None = Field(default=None, alias="user_name")
    title: str
    category: str
    body: str
    likes_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True
