from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import ConflictError
from app.core.password import hash_password
from app.repositories import user_repo

def register_user(db: Session, email: str, password: str):
    if user_repo.get_user_by_email(db, email):
        raise ConflictError("email already exists")
    
    password_hash = hash_password(password)
    try:
        user = user_repo.create_user(db, email, password_hash)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise ConflictError("email already exists")
    except:
        db.rollback()
        raise
