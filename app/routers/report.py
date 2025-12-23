from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.repo_service import get_user_spending, get_spending_ranking
from app.db.database import get_db

router = APIRouter(prefix="/reports", tags=["Reports"])

        
@router.get("/user/{user_id}/total-spent")
def user_spending_report(user_id: int, db: Session = Depends(get_db)):
    total_spent = get_user_spending(db, user_id)
    return {"user_id": user_id, "total_spent": total_spent} 


@router.get("/users/ranking")
def user_spending_ranking(limit: int = 5, db: Session = Depends(get_db)):
    ranking = get_spending_ranking(db, limit)
    return ranking
