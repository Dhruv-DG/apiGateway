from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base

class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, index=True)   # user:<id> / apikey:<key> / ip:<ip>
    path = Column(String)
    method = Column(String)
    status_code = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
