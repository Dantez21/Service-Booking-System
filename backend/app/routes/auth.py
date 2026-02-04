from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import LoginSchema
from app.auth.hashing import Hash
from app.auth.jwt import create_access_token

router = APIRouter(
    prefix="/api/admin",
    tags=["Authentication"]
)

@router.post("/login")
def login(request: LoginSchema, db: Session = Depends(get_db)):
    # 1. Fetch user from PostgreSQL
    user = db.query(User).filter(User.email == request.email).first()
    
    # 2. Check if user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid Credentials"
        )
    
    # 3. Verify the hashed password
    # We use the 'Hash' utility from your app.auth.hashing file
    if not Hash.verify(user.hashed_password, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect Password"
        )

    # 4. Generate the JWT Access Token
    access_token = create_access_token(data={"sub": user.email})
    
    # 5. Return the token to the frontend
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }