from app.db.session import SessionLocal
from app.models.user import User

db = SessionLocal()
user = db.query(User).filter(User.email == "dhruv@example.com").first()
user.role = "admin"
db.commit()
db.close()

print("Admin created")
