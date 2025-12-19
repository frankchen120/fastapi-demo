from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.core.exceptions import UnauthorizedError
from app.core.jwt import ALGORITHM, decode_token
from app.db.database import SessionLocal
from app.models.enums import UserRole
from app.repositories.user_repo import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

#bearer_scheme = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def get_current_user(
    token: str = Depends(oauth2_scheme),    
    db: Session = Depends(get_db)
):
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedError("invalid token")
    except Exception:
        raise UnauthorizedError("invalid token")
        
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