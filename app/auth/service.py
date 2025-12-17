from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.hashing import hash_password, verify_password
from app.core.security import create_access_token

def create_user(db: Session, email: str, password: str):
    user = User(email=email, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    token = create_access_token({"sub": str(user.id)})
    return token
