
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.settings import settings

ALGORITHM = "HS256"

def create_access_token(sub: str, expire_minutes: int = 30) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": sub,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expire_minutes)).timestamp())
    }
    encoded_jwt = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=ALGORITHM)
