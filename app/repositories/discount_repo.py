from typing import List
from app.schemas.discount import DiscountResponse

# In-memory DB
_discount_db: List[DiscountResponse] = []

def save_discount(discount: DiscountResponse) -> DiscountResponse:
    _discount_db.append(discount)
    return discount

def get_all_discounts() -> List[DiscountResponse]:
    return _discount_db
