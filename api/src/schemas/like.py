from pydantic import BaseModel
from typing import List

from src.schemas.article import ArticleResponse
from src.schemas.question import QuestionResponse

class LikeResponse(BaseModel):
    message: str
    likes_count: int

class LikedContentsResponse(BaseModel):
    articles: List[ArticleResponse]
    questions: List[QuestionResponse]