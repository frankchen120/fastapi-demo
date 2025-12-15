
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.order import OrderModel
from app.models.order_item import OrderItemModel

def get_user_total_spent(db: Session, user_id: int):
    return (
        db.query(
            func.sum(OrderItemModel.unit_price * OrderItemModel.quantity).label("total_spent")
        )
        .join(OrderModel, OrderModel.id == OrderItemModel.order_id)
        .filter(OrderModel.user_id == user_id)
        .scalar()
    ) 