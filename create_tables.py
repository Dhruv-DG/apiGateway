from app.db.session import engine
from app.db.base import Base
from app.models.user import User  # import all models here
from app.models.api_key import APIKey

Base.metadata.create_all(bind=engine)
print("Tables created successfully")