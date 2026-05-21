from pydantic import BaseModel

class LoginRequest(BaseModel):
    name: str       # ログイン用のユーザー名
    password: str   # 生のパスワード

# パスワード変更用
class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str