from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class QuestionCreate(BaseModel):
    title: str
    body: str

class QuestionResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    body: str
    created_at: datetime

    class Config:
        from_attributes = True
