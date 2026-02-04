from fastapi import APIRouter

router = APIRouter()

@router.post("/ask")
async def ask_bot(question: str):
    # Placeholder response
    return {"question": question, "answer": "This is a dummy response"}
