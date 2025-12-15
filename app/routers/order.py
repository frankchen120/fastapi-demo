from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.services.order_service import get_user_orders, get_order_items
from app.schemas.order import OrderResponse, OrderItemResponse
from app.db.database import SessionLocal

router = APIRouter(prefix="/orders", tags=["Orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.get("user/{user_id}", response_model=List[OrderResponse])
def list_user_orders(user_id: int, db: Session = Depends(get_db)):
    orders = get_user_orders(db, user_id)
    return orders

@router.get("/{order_id}/items", response_model=List[OrderItemResponse])
def list_order_items(order_id: int, db: Session = Depends(get_db)):
    items = get_order_items(db, order_id)
    if items is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return items
