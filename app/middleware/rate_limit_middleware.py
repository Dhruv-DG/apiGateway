from fastapi import Request
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from app.rate_limiter.limiter import is_allowed
from app.analytics.logger import log_request
from app.db.session import SessionLocal
from app.core.config import settings

ALGORITHM = "HS256"

def extract_user_from_jwt(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return None, None

    token = auth.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub"), payload.get("role", "free")
    except JWTError:
        return None, None


async def rate_limit_middleware(request: Request, call_next):
    identifier = None
    # DEFAULTS (IMPORTANT)
    request.state.user_role = "free"

    api_key = request.headers.get("X-API-Key")
    user_id, role = extract_user_from_jwt(request)

    if api_key:
        identifier = f"apikey:{api_key}"
        request.state.user_role = "free"   # API keys use free limits for now

    elif user_id:
        identifier = f"user:{user_id}"
        request.state.user_role = role or "free"

    else:
        identifier = f"ip:{request.client.host}"
        request.state.user_role = "free"

    if not is_allowed(identifier, request.url.path, request.state.user_role):
        db = SessionLocal()
        log_request(
            db=db,
            identifier=identifier,
            path=request.url.path,
            method=request.method,
            status_code=429
        )
        db.close()

        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"}
        )

    response = await call_next(request)

    db = SessionLocal()
    log_request(
        db=db,
        identifier=identifier,
        path=request.url.path,
        method=request.method,
        status_code=response.status_code
    )
    db.close()

    return response
