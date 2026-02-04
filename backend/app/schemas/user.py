# File: backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True

# This is what our Login Route uses
class LoginSchema(BaseModel):
    email: EmailStr
    password: str