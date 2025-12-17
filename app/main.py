from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.analytics.router import router as analytics_router
from app.routes.protected import router as protected_router

app = FastAPI(title="Developer API Gateway")

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
app.include_router(protected_router, prefix="/protected", tags=["Protected"])

@app.get("/")
def health():
    return {"status": "running"}
