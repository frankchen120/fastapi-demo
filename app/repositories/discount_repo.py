from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.discount import DiscountModel
from app.schemas.discount import DiscountResponse
    
def create(db: Session, name: str, final_price: float) -> DiscountModel:
    obj = DiscountModel(name=name, final_price=final_price)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get(db: Session, discount_id: int) -> Optional[DiscountModel]:
    return db.query(DiscountModel).filter(DiscountModel.id == discount_id).first()

def list_all(db: Session) -> List[DiscountModel]:
    return db.query(DiscountModel).order_by(DiscountModel.id.desc()).all()

def update(db: Session, obj: DiscountModel, name: str, final_price: float) -> DiscountModel:
    obj.name = name
    obj.final_price = final_price
    db.commit()
    db.refresh(obj)
    return obj

def delete(db: Session, obj: DiscountModel) -> None:
    db.delete(obj)
    db.commit()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    