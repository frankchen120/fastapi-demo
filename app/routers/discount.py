from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from app.schemas.discount import Discount, DiscountResponse
from app.services.discount_service import calculate_discount, list_discounts
from app.db.database import SessionLocal

router = APIRouter(prefix="/discount", tags=["Discount"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=DiscountResponse)
def create_discount(discount: Discount, db: Session = Depends(get_db)):
    return calculate_discount(db, discount)

@router.get("/", response_model=List[DiscountResponse])
def list_all(db: Session = Depends(get_db)):
    return list_discounts(db)
