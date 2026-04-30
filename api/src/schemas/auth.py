from pydantic import BaseModel

class LoginRequest(BaseModel):
    name: str       # ログイン用のユーザー名
    password: str   # 生のパスワード