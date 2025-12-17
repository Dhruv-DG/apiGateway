from fastapi import APIRouter, Depends
from app.auth.dependency import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/data")
def protected_data(user: User = Depends(get_current_user)):
    return {"message": f"Hello {user.email}"}
