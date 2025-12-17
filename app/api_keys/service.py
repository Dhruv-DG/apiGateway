from sqlalchemy.orm import Session
from app.models.api_key import APIKey
from app.utils.api_key import generate_api_key

def create_api_key(db: Session, user_id: int):
    key = generate_api_key()
    api_key = APIKey(key=key, user_id=user_id)
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return key

def get_api_key(db: Session, key: str):
    return db.query(APIKey).filter(APIKey.key == key, APIKey.is_active == 1).first()
