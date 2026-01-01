from fastapi import Request
from fastapi.responses import JSONResponse
from app.rate_limiter.limiter import is_allowed
from app.analytics.logger import log_request
from app.db.session import SessionLocal

async def rate_limit_middleware(request: Request, call_next):
    identifier = None

    api_key = request.headers.get("X-API-Key")
    if api_key:
        identifier = f"apikey:{api_key}"
    elif hasattr(request.state, "user"):
        identifier = f"user:{request.state.user.id}"
    else:
        identifier = f"ip:{request.client.host}"

    if not is_allowed(identifier):
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
