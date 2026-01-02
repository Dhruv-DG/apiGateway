from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.auth.dependency import get_current_user
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    new_role: str,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user)
):
    if not admin or admin.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = new_role
    db.commit()

    return {"message": f"User role updated to {new_role}"}
