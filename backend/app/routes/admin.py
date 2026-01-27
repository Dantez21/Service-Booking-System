from fastapi import APIRouter

router = APIRouter()

@router.get("/stats")
async def get_stats():
    return {"users": 0, "projects": 0, "payments": 0}

@router.post("/create-user")
async def create_user():
    return {"message": "Admin user created"}
