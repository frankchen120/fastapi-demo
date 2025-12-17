from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.enums import UserRole

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(SAEnum(UserRole), default=UserRole.user)
    
    orders = relationship("OrderModel", back_populates="user")
    
    