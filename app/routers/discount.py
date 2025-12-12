from fastapi import APIRouter
from typing import List
from app.schemas.discount import Discount, DiscountResponse
from app.services.discount_service import calculate_discount, list_discounts

router = APIRouter(prefix="/discount", tags=["Discount"])

@router.post("/", response_model=DiscountResponse)
def create_discount(discount: Discount):
    return calculate_discount(discount)

@router.get("/", response_model=List[DiscountResponse])
def list_all():
    return list_discounts()
