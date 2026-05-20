from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.models.like import Like
from src.models.article import Article, ArticleComment
from src.models.question import Question, QuestionComment

# target_type に対応するモデルのマッピング
TARGET_MODELS = {
    "article": Article,
    "article_comment": ArticleComment,
    "question": Question,
    "question_comment": QuestionComment
}

async def create_like(db: AsyncSession, target_type: str, target_id: UUID, user_id: UUID) -> int:
    """指定した対象へのいいねを作成し、対象のlikes_countをインクリメントする"""
    
    # 対象のモデルを取得
    model = TARGET_MODELS.get(target_type)
    if not model:
        raise HTTPException(status_code=400, detail="不正なtarget_typeです")
        
    # 1. 対象のlikes_countを+1 (同時に存在確認)
    stmt = (
        update(model)
        .where(model.id == target_id)
        .values(likes_count=model.likes_count + 1)
        .returning(model.likes_count)
    )
    
    try:
        # 先にカウント更新を試みる
        result = await db.execute(stmt)
        updated_likes_count = result.scalar()
        
        if updated_likes_count is None:
            # 対象が存在しない場合
            raise HTTPException(status_code=404, detail="対象が見つかりません")
            
        # 2. いいねレコード作成
        new_like = Like(
            user_id=user_id,
            target_type=target_type,
            target_id=target_id
        )
        db.add(new_like)
        
        await db.commit()
        return updated_likes_count
        
    except IntegrityError:
        await db.rollback()
        # UniqueConstraint違反(すでにいいね済み)など
        raise HTTPException(status_code=400, detail="すでにいいねしています")
