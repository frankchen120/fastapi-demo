import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.exceptions import BadRequestError, ForbiddenError
from app.dependencies.auth import get_current_user, require_role
from app.repositories.order_repo import get_order_by_id
from app.services.order_service import get_user_orders, get_order_items, place_order
from app.schemas.order import OrderCreateRequest, OrderCreateResponse, OrderResponse, OrderItemResponse
from app.db.database import get_db
from app.models.enums import UserRole

logger = logging.getLogger("api")

router = APIRouter(prefix="/orders", tags=["Orders"])

# ---------------
# Admin endpoints
# ---------------
@router.get("/user/{user_id}", response_model=List[OrderResponse])
def list_user_orders(user_id: int, 
                     _admin = Depends(require_role(UserRole.admin)),
                     db: Session = Depends(get_db)
):
    orders = get_user_orders(db, user_id)
    return orders


# ---------------
# User endpoints
# ---------------
@router.get("/me")
def my_orders(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    orders = get_user_orders(db, current_user.id)
    return orders

@router.post("/me", response_model=OrderCreateResponse)
def create_my_order(
    data: OrderCreateRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if len(data.items) == 0:
        raise BadRequestError("items cannot be empty")
    
    order_id = place_order(db, current_user.id, [it.model_dump() for it in data.items])
    return {"order_id": order_id, "items_count": len(data.items)}

    
@router.get("/{order_id}/items", response_model=List[OrderItemResponse])
def list_order_items(order_id: int,
                     current_user = Depends(get_current_user),
                     db: Session = Depends(get_db)
):
    order = get_order_by_id(db, order_id)
    if not order or order.user_id != current_user.id:
        raise ForbiddenError("No permission")
    
    items = get_order_items(db, order_id)
    return items