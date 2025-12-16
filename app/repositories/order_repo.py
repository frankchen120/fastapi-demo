from sqlalchemy.orm import Session
from app.models.order import OrderModel
from app.models.order_item import OrderItemModel


def get_orders_by_user(db: Session, user_id: int):
    return (
        db.query(OrderModel)
        .filter(OrderModel.user_id == user_id)
        .all()
    )
    
def get_order_by_id(db: Session, order_id: int):
    #return db.query(OrderModel).filter(OrderModel.id == order_id).first()
    return (
        db.query(OrderModel)
        .filter(OrderModel.id == order_id)
        .first()
    )

def create_order(db: Session, user_id: int) -> OrderModel:
    order = OrderModel(user_id=user_id)
    db.add(order)
    db.flush()
    return order

def add_order_items(db: Session, order_id: int, items: list[dict]) -> None:
    for it in items:
        db.add(OrderItemModel(
            order_id=order_id,
            product_name=it["product_name"],
            unit_price=it["unit_price"],
            quantity=it["quantity"]
        ))
        