from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from uuid import UUID
from typing import Optional

# Bearer token を受け取る設定
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


# JWT設定
SECRET_KEY = SECRET_KEY = "your-super-secret-key-for-pbl12"
ALGORITHM = "HS256"


async def get_current_user_id(
    token: str = Depends(oauth2_scheme)
):
    """
    AuthorizationヘッダーからJWTを取得し、
    user_idを取り出して返す
    """

    try:
        # JWTを復号
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # payloadからuser_id取得
        user_id = payload.get("user_id")

        # user_idが無い場合
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="user_idが存在しません"
            )

        # UUID型へ変換して返却
        return UUID(user_id)

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="トークンが不正です"
        )

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="認証エラー"
        )


async def get_current_user_id_optional(
    token: Optional[str] = Depends(oauth2_scheme_optional)
) -> Optional[UUID]:
    """
    AuthorizationヘッダーからJWTを取得し、
    user_idを取り出して返す。未ログイン時はNoneを返す。
    """
    if not token:
        return None

    try:
        # JWTを復号
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # payloadからuser_id取得
        user_id = payload.get("user_id")

        if user_id is None:
            return None

        # UUID型へ変換して返却
        return UUID(user_id)

    except Exception:
        # 期限切れトークンや不正トークンの場合も認証情報無しとして扱う
        return None