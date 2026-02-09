import sys
import os
sys.path.append(os.getcwd())

from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.auth.hashing import Hash

def reset_db():
    print("Connecting to database...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Clear existing
        db.query(User).filter(User.email == "admin@daniel.com").delete()
        db.commit()

        # Create new - UPDATED KEYWORD HERE
        new_user = User(
            email="admin@daniel.com",
            password=Hash.bcrypt("admin123") 
        )
        db.add(new_user)
        db.commit()
        print("SUCCESS: Admin user created!")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_db()