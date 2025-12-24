from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import ConflictError, NotFoundError
from app.repositories import order_repo, user_repo
from app.repositories.order_repo import create_order, add_order_items

def get_user_orders(db: Session, user_id: int):
    user = user_repo.get_user_by_id(db, user_id)
    if not user:
        raise NotFoundError(f"user_id={user_id}")
    
    return order_repo.get_orders_by_user(db, user_id)

def get_order_items(db: Session, order_id: int):
    order = order_repo.get_order_by_id(db, order_id)
    if not order:
        raise NotFoundError(f"order_id={order_id}")
    return order.items
   
def get_order_by_id(db: Session, order_id: int):
    order = order_repo.get_order_by_id(db, order_id)
    return order

def place_order(db: Session, user_id: int, items: list[dict]) -> int:
    try:
        order = create_order(db, user_id)
        add_order_items(db, order.id, items)
        
        db.commit()
        db.refresh(order)
        return order.id
    
    except IntegrityError as e:
        db.rollback()
        raise ConflictError("DB constraint violated") 

    except Exception:
        db.rollback()
        raise
 