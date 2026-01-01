from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import SessionLocal
from app.models.usage_log import UsageLog

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/summary")
def usage_summary(db: Session = Depends(get_db)):
    total = db.query(UsageLog).count()
    blocked = db.query(UsageLog).filter(
        UsageLog.status_code == 429
    ).count()
    return {
        "total_requests": total,
        "blocked_requests": blocked
    }

@router.get("/usage")
def get_usage(db: Session = Depends(get_db)):
    return db.query(UsageLog).order_by(UsageLog.timestamp.desc()).limit(50).all()

@router.get("/chart/requests-per-endpoint")
def requests_per_endpoint(db: Session = Depends(get_db)):
    rows = (
        db.query(UsageLog.path, func.count())
        .group_by(UsageLog.path)
        .all()
    )
    return [{"path": r[0], "count": r[1]} for r in rows]

@router.get("/chart/status-codes")
def status_code_distribution(db: Session = Depends(get_db)):
    rows = (
        db.query(UsageLog.status_code, func.count())
        .group_by(UsageLog.status_code)
        .all()
    )
    return [{"status": r[0], "count": r[1]} for r in rows]
