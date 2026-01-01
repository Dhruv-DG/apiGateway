from app.db.session import engine
from app.db.base import Base

# IMPORT ALL MODELS
from app.models.user import User
from app.models.api_key import APIKey
from app.models.usage_log import UsageLog

Base.metadata.create_all(bind=engine)
print("Tables created successfully")
