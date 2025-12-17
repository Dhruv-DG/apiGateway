from fastapi import APIRouter

router = APIRouter()

@router.get("/usage")
def usage():
    return {"usage": "analytics data"}
