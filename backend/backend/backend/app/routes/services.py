from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_services():
    return {"services": []}

@router.post("/")
async def create_service():
    return {"message": "Service created"}
