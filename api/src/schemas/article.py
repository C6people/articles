from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class ArticleCreate(BaseModel):
    title: str
    body: str
    category: str

class ArticleResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    body: str
    created_at: datetime
    category: str

    class Config:
        from_attributes = True
