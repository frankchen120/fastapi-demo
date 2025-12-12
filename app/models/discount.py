from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base

class DiscountModel(Base):
    __tablename__ = "discounts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    final_price = Column(Float, nullable=False)
    
    