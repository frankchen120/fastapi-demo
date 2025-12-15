from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.repo_service import get_user_spending
from app.db.database import SessionLocal

router = APIRouter(prefix="/reports", tags=["Reports"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.get("/user/{user_id}/total-spent")
def user_spending_report(user_id: int, db: Session = Depends(get_db)):
    total_spent = get_user_spending(db, user_id)
    return {"user_id": user_id, "total_spent": total_spent} 

