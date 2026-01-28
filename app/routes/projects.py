from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form, Header
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import os
import uuid

from app.database import get_db
from app.models.project import Project
from app.schemas.project import ProjectOut

router = APIRouter(tags=["Projects"])

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- SECURITY CONFIG ---
# In a production app, move this to an environment variable (.env)
ADMIN_SECRET_TOKEN = "your_super_secret_token_123"

async def verify_admin(x_admin_token: str = Header(None)):
    if x_admin_token != ADMIN_SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Unauthorized: Invalid Admin Token"
        )
    return x_admin_token

# --- ROUTES ---

# 1. CREATE (Protected)
@router.post("/", response_model=ProjectOut)
async def create_project(
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    github_link: Optional[str] = Form(None),
    live_demo: Optional[str] = Form(None),
    file: UploadFile = File(...),
    admin_check: str = Depends(verify_admin), # Security Check
    db: Session = Depends(get_db)
):
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_url = f"http://127.0.0.1:8000/static/uploads/{unique_filename}"

    new_project = Project(
        title=title,
        description=description,
        category=category,
        github_link=github_link,
        live_demo=live_demo,
        image_url=image_url
    )
    
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

# 2. GET ALL (Public)
@router.get("/", response_model=List[ProjectOut])
def get_all_projects(db: Session = Depends(get_db)):
    return db.query(Project).order_by(Project.created_at.desc()).all()

# 3. UPDATE (Protected)
@router.put("/{project_id}", response_model=ProjectOut)
async def update_project(
    project_id: int,
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    github_link: Optional[str] = Form(None),
    live_demo: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    admin_check: str = Depends(verify_admin), # Security Check
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.title = title
    project.description = description
    project.category = category
    project.github_link = github_link
    project.live_demo = live_demo

    if file:
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        project.image_url = f"http://127.0.0.1:8000/static/uploads/{unique_filename}"

    db.commit()
    db.refresh(project)
    return project

# 4. DELETE (Protected)
@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int, 
    admin_check: str = Depends(verify_admin), # Security Check
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Optional: Delete file from local storage too
    if project.image_url:
        filename = project.image_url.split("/")[-1]
        old_file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.exists(old_file_path):
            os.remove(old_file_path)

    db.delete(project)
    db.commit()
    return None