from sqlalchemy.orm import Session
from app.models.usage_log import UsageLog

def log_request(
    db: Session,
    identifier: str,
    path: str,
    method: str,
    status_code: int
):
    try:
        log = UsageLog(
            identifier=identifier,
            path=path,
            method=method,
            status_code=status_code
        )
        db.add(log)
        db.commit()
    except Exception:
        db.rollback()   # NEVER break request flow
