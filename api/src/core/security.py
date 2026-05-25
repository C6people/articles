# api/src/core/security.py
from passlib.context import CryptContext
import jwt  # PyJWT
from datetime import datetime, timedelta  # 有効期限の設定用

# bcryptアルゴリズムを使用する設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# JWTの設定（本来は .env などの環境変数で管理しますが、今回は直接記述します）
SECRET_KEY = "your-super-secret-key-for-pbl12" # トークン暗号化の鍵（好きな文字列でOK）
ALGORITHM = "HS256"                            # 暗号化アルゴリズム
ACCESS_TOKEN_EXPIRE_MINUTES = 60               # トークンの有効期限（例: 60分）

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """入力されたパスワードとDBのハッシュを照合する"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """データ（ユーザー情報）を受け取り、JWTトークンを生成する"""
    to_encode = data.copy()
    
    # 現在時刻に有効期限（60分）を足して 'exp'（expiration）として追加
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # jwt.encode を使ってトークンを作成
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_password_hash(password: str) -> str:
    """
    パスワードをハッシュ化して返す
    """
    return pwd_context.hash(password)