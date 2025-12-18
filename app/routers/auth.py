from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedError
from app.schemas.auth import LoginRequest, TokenResponse
from app.repositories.user_repo import get_user_by_email
from app.core.password import verify_password  
from app.core.security import create_access_token
from app.db.database import SessionLocal

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session=Depends(get_db)):
    user = get_user_by_email(db, data.email)
    
    if not user:
        raise UnauthorizedError("Invalid credentials")
    
    if not verify_password(data.password, user.password_hash):
        raise UnauthorizedError("Invalid credentials")
        
    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, token_type="bearer")

    