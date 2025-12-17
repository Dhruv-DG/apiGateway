from fastapi import APIRouter

router = APIRouter()

@router.get("/data")
def protected_data():
    return {"data": "This is protected"}
