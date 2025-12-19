import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedError
from app.dependencies.auth import get_current_user
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.services.auth_service import register_user
 
from app.repositories.user_repo import get_user_by_email
from app.core.password import verify_password  
from app.core.jwt import create_access_token
from app.db.database import SessionLocal

logger = logging.getLogger("api")

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/register")
def register(data: RegisterRequest, db: Session=Depends(get_db)):
    user = register_user(db, data.email, data.password)
    return {"id": user.id, "email": user.email }
        
@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    email = form_data.username
    password = form_data.password
    
    logger.info(f"user [{email}] tries to login")
    
    user = get_user_by_email(db, email)
    
    if not user:
        raise UnauthorizedError("Invalid credentials")
    
    if not verify_password(password, user.password_hash):
        raise UnauthorizedError("Invalid credentials")
        
    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token, token_type="bearer")

@router.get("/me")
def me(current_user = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}
