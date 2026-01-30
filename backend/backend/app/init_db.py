import sys
import os

# Ensures Python can see the 'app' folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base
# IMPORTANT: You must import your models so SQLAlchemy sees them
from app.models.project import Project
from app.models.user import User
from app.models.service import Service

def create_tables():
    print("Connecting to PostgreSQL at 127.0.0.1...")
    try:
        # This command creates the tables in the DB defined in your .env
        Base.metadata.create_all(bind=engine)
        print("✅ Success! Tables 'projects', 'users', and 'services' created.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_tables()