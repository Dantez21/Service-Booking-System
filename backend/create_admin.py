# File: backend/create_admin.py
import sys
import os

# Ensure Python can find the 'app' folder
sys.path.append(os.getcwd())

from app.database import SessionLocal
from app.models.user import User
from app.auth.hashing import Hash

def create_initial_admin():
    db = SessionLocal()
    email = "admin@daniel.com"
    password = "admin123"

    try:
        # Check if user already exists so we don't create duplicates
        user = db.query(User).filter(User.email == email).first()
        
        if user:
            print(f"User {email} already exists. No changes made.")
        else:
            new_user = User(
                email=email,
                hashed_password=Hash.bcrypt(password)
            )
            db.add(new_user)
            db.commit()
            print("--------------------------------------")
            print("ADMIN CREATED SUCCESSFULLY")
            print(f"Email: {email}")
            print(f"Password: {password}")
            print("--------------------------------------")
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_admin()