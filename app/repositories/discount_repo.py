from typing import List
from sqlalchemy.orm import Session
from app.models.discount import DiscountModel
from app.schemas.discount import DiscountResponse


def save_discount(db: Session, discount: DiscountResponse) -> DiscountResponse:
    db_obj = DiscountModel(
        name=discount.name,
        final_price=discount.final_price
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    
    return discount

def get_all_discounts(db: Session) -> List[DiscountResponse]:
    records = db.query(DiscountModel).all()
    return [
        DiscountResponse(name=r.name, final_price=r.final_price)
        for r in records
    ]