from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class ArticleCommentCreate(BaseModel):
    parent_id: UUID | None = None  # 親コメントのID
    body: str            # コメントの内容

class ArticleCommentResponse(BaseModel):
    id: UUID              # コメントのID
    parent_id: UUID | None = None  # 親コメントのID
    body: str             # コメントの内容
    created_at: datetime  # 作成日時

    class Config:  # ORMモデルからの変換するための設定
        from_attributes = True