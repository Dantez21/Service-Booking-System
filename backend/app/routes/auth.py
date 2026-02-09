from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Import from your specific project structure
from app.database import get_db
from app.models.user import User
from app.schemas.user import LoginSchema
from app.auth.hashing import Hash
from app.auth.jwt import create_access_token

router = APIRouter()

@router.post("/login")
def login(request: LoginSchema, db: Session = Depends(get_db)):
    # 1. Check if the user exists in the PostgreSQL 'users' table
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 2. Verify the plain password against the hashed password in the DB
    # UPDATED: Changed 'user.hashed_password' to 'user.password'
    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 3. Generate a JWT Access Token
    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }