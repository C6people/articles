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
    created_at: datetime  # 作成日時

class CommentCreate(BaseModel): # コメント投稿用のスキーマ

    article_id: UUID   # コメントを投稿する記事のID
    body: str          # コメントの内容

