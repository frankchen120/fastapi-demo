from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dependencies.auth import get_current_user, require_role
from app.services.order_service import get_user_orders, get_order_items, place_order
from app.schemas.order import OrderCreateRequest, OrderCreateResponse, OrderResponse, OrderItemResponse
from app.db.database import SessionLocal
from app.models.enums import UserRole

router = APIRouter(prefix="/orders", tags=["Orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.get("/user/{user_id}", response_model=List[OrderResponse])
def list_user_orders(user_id: int, db: Session = Depends(get_db)):
    orders = get_user_orders(db, user_id)
    return orders

@router.get("/{order_id}/items", response_model=List[OrderItemResponse])
def list_order_items(order_id: int, db: Session = Depends(get_db)):
    items = get_order_items(db, order_id)
    if items is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return items

@router.get("/me/orders")
def my_orders(
    current_user=Depends(get_current_user),
    #current_user=Depends(require_role(UserRole.user)),
    db: Session = Depends(get_db)
):
    orders = get_user_orders(db, current_user.id)
    return orders

@router.post("/me", response_model=OrderCreateResponse)
def create_my_order(
    data: OrderCreateRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if len(data.items) == 0:
        raise HTTPException(status_code=400, detail="items can't be empty")
    
    order_id = place_order(db, current_user.id, [it.model_dump() for it in data.items])
    return {"order_id": order_id, "items_count": len(data.items)}

    