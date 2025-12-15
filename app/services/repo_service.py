from sqlalchemy.orm import Session
from app.repositories.report_repo import get_user_total_spent

def get_user_spending(db: Session, user_id: int):
    total = get_user_total_spent(db, user_id)
    return total or 0
