from typing import List
from sqlalchemy.orm import Session
from app.schemas.discount import Discount, DiscountResponse, DiscountUpdate
from app.repositories import discount_repo

def _calc_final_price(price: float, discount:float) -> float:
    return price * (1 - discount)

def create_discount(db: Session, data: Discount):
    final_price = _calc_final_price(data.price, data.discount)
    return discount_repo.create(
        db, 
        data.name, 
        data.price,
        data.discount,
        final_price)

def list_discounts(db: Session):
    return discount_repo.list_all(db)

def get_discount(db: Session, discount_id: int):
    return discount_repo.get(db, discount_id)

def update_discount(db: Session, discount_id: int, data: DiscountUpdate):
    obj = discount_repo.get(db, discount_id)
    if not obj:
        return None
    
    if(data.name is not None):
        obj.name = data.name
    if(data.price is not None):
        obj.price = data.price
    if(data.discount is not None):    
        obj.discount = data.discount

    obj.final_price = _calc_final_price(obj.price, obj.discount)        
    
    return discount_repo.update(db, obj)

def delete_discount(db: Session, discount_id: int):
    obj = discount_repo.get(db, discount_id)
    if not obj:
        return None
    discount_repo.delete(db, obj)
    return True

