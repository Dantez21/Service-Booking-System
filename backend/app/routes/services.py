from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Schema for the Service
class ServiceSchema(BaseModel):
    title: str
    icon: str
    description: str

# Mock Database for testing (Replace with SQL logic if using a DB)
services_db = []

ADMIN_TOKEN = "supersecretkey"

def verify_admin(x_admin_token: str = Header(None)):
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid Admin Token")
    return x_admin_token

@router.get("/")
async def get_all_services():
    return services_db

@router.post("/")
async def add_service(service: ServiceSchema, token: str = Depends(verify_admin)):
    new_service = {
        "id": len(services_db) + 1,
        **service.model_dump()
    }
    services_db.append(new_service)
    return new_service

@router.delete("/{service_id}")
async def delete_service(service_id: int, token: str = Depends(verify_admin)):
    global services_db
    services_db = [s for s in services_db if s.get("id") != service_id]
    return {"message": "Deleted"}