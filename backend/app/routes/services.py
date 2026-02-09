from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceOut

router = APIRouter(
    prefix="/api/services",   # NO trailing slash
    tags=["Services"]
)

@router.get("", response_model=List[ServiceOut])
def get_services(db: Session = Depends(get_db)):
    return db.query(Service).all()

@router.post("", response_model=ServiceOut)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    new_service = Service(**service.model_dump())
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service

@router.delete("/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    db.delete(service)
    db.commit()
    return {"message": "Service deleted"}
