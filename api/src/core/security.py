# api/src/core/security.py
from passlib.context import CryptContext

# bcryptアルゴリズムを使用する設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """入力されたパスワードとDBのハッシュを照合する"""
    return pwd_context.verify(plain_password, hashed_password)