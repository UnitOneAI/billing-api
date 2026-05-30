"""JWT issuance / verification."""
import os
from datetime import datetime, timedelta, timezone

import jwt


def _get_jwt_secret() -> str:
    """Get JWT secret from environment. Raises if not configured."""
    secret = os.environ.get("JWT_SECRET")
    if not secret:
        raise RuntimeError(
            "JWT_SECRET environment variable is not set. "
            "Set it to a secure random string in production."
        )
    return secret
JWT_ALGO = "HS256"


def issue_token(user_id: int, email: str, is_admin: bool = False) -> str:
    payload = {
        "sub": str(user_id),
        "email": email,
        "is_admin": is_admin,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=12),
    }
    return jwt.encode(payload, _get_jwt_secret(), algorithm=JWT_ALGO)


def verify_token(token: str) -> dict:
    return jwt.decode(token, _get_jwt_secret(), algorithms=[JWT_ALGO])
