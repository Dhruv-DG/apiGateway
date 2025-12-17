from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Integer, default=1)
