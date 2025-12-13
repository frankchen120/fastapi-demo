from fastapi import APIRouter, Depends
from fastapi import status, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.schemas.discount import Discount, DiscountResponse, DiscountUpdate
from app.services.discount_service import (
    create_discount, list_discounts, get_discount, update_discount, delete_discount
)
from app.db.database import SessionLocal

router = APIRouter(prefix="/discount", tags=["Discount"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=DiscountResponse, status_code=status.HTTP_201_CREATED)
def create(discount: Discount, db: Session = Depends(get_db)):
    obj = create_discount(db, discount)
    return {"id": obj.id, "name": obj.name, "final_price": obj.final_price}

@router.get("/", response_model=List[DiscountResponse])
def list_all(db: Session = Depends(get_db)):
    rows = list_discounts(db)
    return [{"id": r.id, "name": r.name, "final_price": r.final_price} for r in rows]

@router.get("/{discount_id}", response_model=DiscountResponse)
def get_one(discount_id: int, db: Session = Depends(get_db)):
    obj = get_discount(db, discount_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Discount not found")
    return {"id": obj.id, "name": obj.name, "final_price": obj.final_price}

@router.put("/{discount_id}", response_model=DiscountResponse)
def update_one(discount_id: int, data: DiscountUpdate, db: Session = Depends(get_db)):
    obj = update_discount(db, discount_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Discount not found")
    return {"id": obj.id, "name": obj.name, "final_price": obj.final_price}

@router.delete("/{discount_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one(discount_id: int, db: Session = Depends(get_db)):
    ok = delete_discount(db, discount_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Discount not found")
    return None

