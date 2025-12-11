from fastapi import APIRouter
from app.schemas.discount import Discount, DiscountResponse

router = APIRouter(prefix="/discount", tags=["Discount"])

@router.post("/", response_model=DiscountResponse)

def create_discount(discount: Discount):
    final_price = discount.price * (1 - discount.discount)
    return DiscountResponse(
        name= discount.name,
        final_price= final_price
    )
    
