import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. SETUP PATH TO .env (Correctly points to portfolio-system/.env)
base_dir = Path(__file__).resolve().parent.parent.parent
env_path = base_dir / '.env'
load_dotenv(dotenv_path=env_path)

# 2. GET DATABASE URL
# IMPORTANT: This will prioritize the URL in your .env file.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback check: If .env is missing or DATABASE_URL is empty, 
# use a default (but you should replace 'your_password' with your real one here too)
if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:your_actual_password@localhost:5432/portfolio_db"

# 3. SQLALCHEMY SETUP
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 4. DATABASE DEPENDENCY
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()