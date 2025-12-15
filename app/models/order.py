from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class OrderModel(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    crated_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("UserModel", back_populates="orders")
    items = relationship("OrderItemModel", back_populates="order")
    
    