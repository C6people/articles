from pydantic import BaseModel
from datetime import datetime

class QuestionCreate(BaseModel):
    title: str
    body: str
    # TODO: ログイン機能実装後は削除し、トークンから取得するように変更する
    user_id: int

class QuestionResponse(BaseModel):
    id: int
    user_id: int
    title: str
    body: str
    created_at: datetime

    class Config:
        from_attributes = True
