from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import os
import uuid
from app.database import get_db
from app.models.project import Project # Ensure this model exists

router = APIRouter(tags=["Projects"])

UPLOAD_DIR = "static/uploads"

@router.post("")
async def create_project(
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    github_link: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Handle File Upload
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Save to DB
    # Note: we save the path relative to the backend root
    image_url = f"static/uploads/{unique_filename}"
    
    new_project = Project(
        title=title,
        description=description,
        category=category,
        github_link=github_link,
        image_url=image_url
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("", response_model=List[dict]) # Replace dict with your Schema
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()