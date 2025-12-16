
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.order import OrderModel
from app.models.order_item import OrderItemModel
from app.models.user import UserModel

def get_user_total_spent(db: Session, user_id: int):
    return (
        db.query(
            func.sum(OrderItemModel.unit_price * OrderItemModel.quantity).label("total_spent")
        )
        .join(OrderModel, OrderModel.id == OrderItemModel.order_id)
        .filter(OrderModel.user_id == user_id)
        .scalar()
    ) 
    
#消費金額最高的前 5 名使用者
"""
SELECT
  u.id AS user_id,
  SUM(i.unit_price * i.quantity) AS total_spent
FROM users u
JOIN orders o ON o.user_id = u.id
JOIN order_items i ON i.order_id = o.id
GROUP BY u.id
ORDER BY total_spent DESC
LIMIT 5;
"""
def get_top_users_by_spending(db: Session, limit: int = 5):
    return (
        db.query(
            UserModel.id.label("user_id"),
            func.sum(OrderItemModel.unit_price * OrderItemModel.quantity).label("total_spent")
        )
        .join(OrderModel, OrderModel.user_id == UserModel.id)
        .join(OrderItemModel, OrderItemModel.order_id == OrderModel.id)
        .group_by(UserModel.id)
        .order_by(func.sum(OrderItemModel.unit_price * OrderItemModel.quantity).desc())
        #.order_by("total_spent DESC")
        .limit(limit)
        .all()
    )

