from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_projects():
    return {"projects": []}

@router.post("/")
async def create_project():
    return {"message": "Project created"}
