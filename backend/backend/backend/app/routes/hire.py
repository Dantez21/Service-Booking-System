from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_hires():
    return {"hires": []}

@router.post("/")
async def create_hire():
    return {"message": "Hire request created"}
