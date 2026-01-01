from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependency import get_current_user
from app.api_keys.dependency import get_user_from_api_key

router = APIRouter()

@router.get("/data")
def protected_data(
    user = Depends(get_current_user),
    api_user_id = Depends(get_user_from_api_key)
):
    if user:
        return {"auth": "jwt", "user_id": user.id}

    if api_user_id:
        return {"auth": "api_key", "user_id": api_user_id}

    raise HTTPException(status_code=401, detail="Not authenticated")
