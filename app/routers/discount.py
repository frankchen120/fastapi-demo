from fastapi import APIRouter, Depends
from fastapi import status, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.schemas.discount import Discount, DiscountResponse
from app.services.discount_service import create_discount, list_discounts
from app.db.database import SessionLocal

router = APIRouter(prefix="/discount", tags=["Discount"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/", 
    response_model=DiscountResponse,
    status_code=status.HTTP_201_CREATED
    )
def create(discount: Discount, db: Session = Depends(get_db)):
    try:
        return create_discount(db, discount)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        

@router.get("/", response_model=List[DiscountResponse])
def list_all(db: Session = Depends(get_db)):
    return list_discounts(db)
