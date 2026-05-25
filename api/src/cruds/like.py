from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, case
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

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


async def get_liked_articles(
    db: AsyncSession,
    user_id: UUID
):
    # ユーザーがいいねした article のID取得
    result = await db.execute(
        select(Like.target_id)
        .where(
            Like.user_id == user_id,
            Like.target_type == "article"
        )
    )

    article_ids = result.scalars().all()

    if not article_ids:
        return []

    # 記事取得（既存構成に寄せる）
    result = await db.execute(
        select(Article)
        .options(selectinload(Article.user))
        .where(Article.id.in_(article_ids))
        .order_by(Article.created_at.desc())
    )

    return result.scalars().all()


async def get_liked_questions(
    db: AsyncSession,
    user_id: UUID
):
    result = await db.execute(
        select(Like.target_id)
        .where(
            Like.user_id == user_id,
            Like.target_type == "question"
        )
    )

    question_ids = result.scalars().all()

    if not question_ids:
        return []

    result = await db.execute(
        select(Question)
        .options(selectinload(Question.user))
        .where(Question.id.in_(question_ids))
        .order_by(Question.created_at.desc())
    )

    return result.scalars().all()


async def delete_like(db: AsyncSession, target_type: str, target_id: UUID, user_id: UUID) -> int:
    """指定した対象へのいいねを削除し、対象のlikes_countをデクリメントする"""
    
    # 対象のモデルを取得
    model = TARGET_MODELS.get(target_type)
    if not model:
        raise HTTPException(status_code=400, detail="不正なtarget_typeです")
        
    # 1. いいねレコードの存在確認
    stmt_select = select(Like).where(
        Like.user_id == user_id,
        Like.target_type == target_type,
        Like.target_id == target_id
    )
    result = await db.execute(stmt_select)
    like_record = result.scalar_one_or_none()
    
    if not like_record:
        raise HTTPException(status_code=400, detail="いいねしていません")
        
    # 2. 対象のlikes_countを-1（0未満にはならないよう制御）
    stmt_update = (
        update(model)
        .where(model.id == target_id)
        .values(likes_count=case((model.likes_count > 0, model.likes_count - 1), else_=0))
        .returning(model.likes_count)
    )
    update_result = await db.execute(stmt_update)
    updated_likes_count = update_result.scalar()
    
    if updated_likes_count is None:
        raise HTTPException(status_code=404, detail="対象が見つかりません")
        
    # 3. いいねレコードを削除
    await db.delete(like_record)
    await db.commit()
    return updated_likes_count


async def check_is_liked(db: AsyncSession, user_id: UUID, target_type: str, target_id: UUID) -> bool:
    """ユーザーが対象をいいねしているか判定する"""
    stmt = select(Like).where(
        Like.user_id == user_id,
        Like.target_type == target_type,
        Like.target_id == target_id
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none() is not None


async def get_user_liked_ids(db: AsyncSession, user_id: UUID, target_type: str, target_ids: list[UUID]) -> set[UUID]:
    """対象のIDリストのうち、ユーザーがいいねしているIDの集合を返す"""
    if not target_ids:
        return set()
    stmt = select(Like.target_id).where(
        Like.user_id == user_id,
        Like.target_type == target_type,
        Like.target_id.in_(target_ids)
    )
    result = await db.execute(stmt)
    return set(result.scalars().all())