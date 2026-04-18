"""JWT issuance / verification."""
import jwt
from datetime import datetime, timedelta, timezone

JWT_SECRET = "billing-api-jwt-supersecret-2024"
JWT_ALGO = "HS256"


def issue_token(user_id: int, email: str, is_admin: bool = False) -> str:
    payload = {
        "sub": str(user_id),
        "email": email,
        "is_admin": is_admin,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=12),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


def verify_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
