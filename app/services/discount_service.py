from typing import List
from sqlalchemy.orm import Session
from app.schemas.discount import Discount, DiscountResponse
from app.repositories.discount_repo import save_discount, get_all_discounts


def create_discount(db:Session, data: Discount) -> DiscountResponse:
    if(data.discount < 0 or data.discount > 1):
        raise ValueError("discount must between 0 and 1")
    
    final_price = data.price * (1 - data.discount)
    
    discount = DiscountResponse(
        name= data.name,
        final_price= final_price
    )
    
    return save_discount(db, discount)

def list_discounts(db: Session) -> List[DiscountResponse]:
    return get_all_discounts(db)


        