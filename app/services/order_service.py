from sqlalchemy.orm import Session
from app.repositories import order_repo


def get_user_orders(db: Session, user_id: int):
    return order_repo.get_orders_by_user(db, user_id)

def get_order_items(db: Session, order_id: int):
    order = order_repo.get_order_by_id(db, order_id)
    if not order:
        return None
    return order.items
