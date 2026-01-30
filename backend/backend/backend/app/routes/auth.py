from fastapi import APIRouter, Depends
from app.auth.hashing import hash_password

router = APIRouter()

@router.post("/register")
def register():
    return {"message": "User registered"}

@router.post("/login")
def login():
    return {"message": "User logged in"}
