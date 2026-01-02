from fastapi import FastAPI
from app.middleware.rate_limit_middleware import rate_limit_middleware
from app.auth.router import router as auth_router
from app.analytics.router import router as analytics_router
from app.routes.protected import router as protected_router
from app.api_keys.router import router as api_key_router
from app.admin.router import router as admin_router
from fastapi.staticfiles import StaticFiles 

app = FastAPI(title="Developer API Gateway")

app.middleware("http")(rate_limit_middleware)

app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
app.include_router(protected_router, prefix="/protected", tags=["Protected"])
app.include_router(api_key_router, prefix="/keys", tags=["API Keys"])

app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

@app.get("/")
def health():
    return {"status": "running"}
