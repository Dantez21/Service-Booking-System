from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_payments():
    return {"payments": []}

@router.post("/")
async def make_payment():
    return {"message": "Payment processed"}
