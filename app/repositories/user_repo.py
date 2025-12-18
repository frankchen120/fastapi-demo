from sqlalchemy.orm import Session
from app.models.enums import UserRole
from app.models.user import UserModel

def get_user_by_id(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()
  
def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()
  
def create_user(db: Session, email: str, password_hash: str):
    user = UserModel(
        email = email,
        password_hash = password_hash,
    )
    
    db.add(user)
    db.flush() # 取得 user.id
    return user