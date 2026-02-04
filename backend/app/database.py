import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. SETUP PATH TO .env
# This looks at this file (database.py), goes up to 'app', 
# up to 'backend', then up to 'portfolio-system' to find .env
base_dir = Path(__file__).resolve().parent.parent.parent
env_path = base_dir / '.env'

# 2. LOAD .env
load_dotenv(dotenv_path=env_path)

# 3. GET DATABASE URL FROM ENVIRONMENT
# The fallback is helpful for local development if the .env isn't found
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:password@localhost:5432/portfolio_db"
)

# 4. SQLALCHEMY SETUP
# 'check_same_thread' is only needed for SQLite. For PostgreSQL, we just need the URL.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 5. DATABASE DEPENDENCY
# This opens a connection for each request and closes it when done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()