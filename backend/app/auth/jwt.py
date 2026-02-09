# File: backend/app/auth/jwt.py
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "YOUR_SUPER_SECRET_KEY" # Ideally move this to your .env
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)