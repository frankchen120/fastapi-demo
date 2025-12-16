from sqlalchemy.orm import Session
from app.repositories.report_repo import get_top_users_by_spending, get_user_total_spent

def get_user_spending(db: Session, user_id: int):
    total = get_user_total_spent(db, user_id)
    return total or 0

def get_spending_ranking(db: Session, limit: int = 5):
    rows = get_top_users_by_spending(db, limit)
    return [
        {"userid": r.user_id, "total_spent": r.total_spent}
        for r in rows
    ]
    