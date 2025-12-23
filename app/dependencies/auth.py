import logging
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.core.exceptions import UnauthorizedError
from app.core.jwt import ALGORITHM, decode_token
from app.db.database import get_db
from app.models.enums import UserRole
from app.repositories.user_repo import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

#bearer_scheme = HTTPBearer()

logger = logging.getLogger("api")



def get_token(token: str = Depends(oauth2_scheme)) -> str:
    logger.info(f"[auth] extracted token prefix={token[:10] if token else None}")
    return token

def get_current_user(
    token: str = Depends(get_token),    
    db: Session = Depends(get_db)
):
    logger.info(f"[auth] token present={bool(token)} prefix={token[:10] if token else None}")
    
    try:
        payload = decode_token(token)
        logger.info(f"[auth] decoded payload keys={list(payload.keys())}")
        
        user_id = payload.get("sub")
        
        if not user_id:
            raise UnauthorizedError("invalid token")
    except Exception as e:
        logger.exception(f"[auth] decode failed: {e}")
        raise UnauthorizedError("invalid token")
        
    logger.info(f"[auth] user-id={user_id}")
        
    user = get_user_by_id(db, int(user_id))
    if not user:
        raise UnauthorizedError("user not found")
        
    return user

def require_role(required_role: UserRole):
    def role_checker(
        current_user = Depends(get_current_user)
    ):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )
        return current_user
    return role_checker