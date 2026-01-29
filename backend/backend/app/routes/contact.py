from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_contacts():
    return {"contacts": []}

@router.post("/")
async def create_contact():
    return {"message": "Contact request sent"}
