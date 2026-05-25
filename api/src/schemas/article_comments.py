from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class ArticleCommentCreate(BaseModel):  # コメント作成用のスキーマ
    article_id: UUID    # 記事のID
    user_id: UUID        # ユーザーのID
    parent_id: UUID | None = None  # 親コメントのID
    body: str            # コメントの内容

class ArticleCommentResponse(BaseModel):
    id: UUID              # コメントのID
    article_id: UUID      # 記事のID
    user_id: UUID         # ユーザーのID
    parent_id: UUID | None = None  # 親コメントのID
    body: str             # コメントの内容
    likes_count: int = 0  # いいね数
    is_liked: bool = False # いいね済みフラグ
    created_at: datetime  # 作成日時
    user_name: str | None = None  # ユーザー名

    class Config:
        from_attributes = True

class CommentCreate(BaseModel): # コメント投稿用のスキーマ
    parent_id: UUID | None = None   # 親コメントのID（返信の場合）
    body: str                       # コメントの内容

