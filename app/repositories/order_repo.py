from sqlalchemy.orm import Session
from app.models.order import OrderModel


def get_orders_by_user(db: Session, user_id: int):
    return (
        db.query(OrderModel)
        .filter(OrderModel.user_id == user_id)
        .all()
    )
    