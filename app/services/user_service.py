from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError
from app.core.password import hash_password
from app.repositories import user_repo

def create_user(db: Session, email: str, password: str):
    if user_repo.get_user_by_email(db, email):
        raise ConflictError("email already exists")
    
    password_hash = hash_password(password)
    return user_repo.create_user(db, email, password_hash)

