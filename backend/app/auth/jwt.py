from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from app import config # This assumes you have SECRET_KEY in your config.py

# Fallback values if config.py isn't set up yet
SECRET_KEY = "SUPER_SECRET_KEY_123" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt