from fastapi import APIRouter
from app.schemas.discount import Discount, DiscountResponse
from app.services.discount_service import calculate_discount

router = APIRouter(prefix="/discount", tags=["Discount"])

@router.post("/", response_model=DiscountResponse)
def create_discount(discount: Discount):
    return calculate_discount(discount)
