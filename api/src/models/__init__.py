# すべてのモデルをここでimportする
# Alembicがテーブルを自動検出するために必要です
from src.models.user import User  # noqa: F401
from src.models.article import Article, ArticleComment  # noqa: F401
from src.models.question import Question, QuestionComment  # noqa: F401
from src.models.like import Like  # noqa: F401
