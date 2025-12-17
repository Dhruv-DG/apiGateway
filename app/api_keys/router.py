from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.dependency import get_current_user
from app.db.session import SessionLocal
from app.api_keys.service import create_api_key

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def create_key(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    key = create_api_key(db, user.id)
    return {"api_key": key}
