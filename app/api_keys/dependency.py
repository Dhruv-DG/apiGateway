from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.api_keys.service import get_api_key

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_from_api_key(
    x_api_key: str = Header(None),
    db: Session = Depends(get_db)
):
    if not x_api_key:
        return None

    api_key = get_api_key(db, x_api_key)
    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return api_key.user_id
