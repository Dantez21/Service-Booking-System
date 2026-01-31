import os
import uuid
import shutil
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form, Header, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.project import Project
from app.schemas.project import ProjectOut

router = APIRouter(tags=["Projects"])

# Match the directory to your main.py mount
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- SECURITY CONFIG ---
# Fallback to 'supersecretkey' if .env SECRET_KEY is missing
ADMIN_SECRET_TOKEN = os.getenv("SECRET_KEY", "supersecretkey")

async def verify_admin(x_admin_token: str = Header(None)):
    if not x_admin_token or x_admin_token != ADMIN_SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Unauthorized: Invalid Admin Token"
        )
    return x_admin_token

# --- ROUTES ---

# 1. CREATE (Protected)
@router.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
async def create_project(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    github_link: Optional[str] = Form(None),
    live_demo: Optional[str] = Form(None),
    file: UploadFile = File(...),
    admin_check: str = Depends(verify_admin),
    db: Session = Depends(get_db)
):
    # Save the file with a unique name
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")

    # Construct dynamic URL
    base_url = str(request.base_url).rstrip('/')
    image_url = f"{base_url}/static/uploads/{unique_filename}"

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
    # Returns projects ordered by newest first
    return db.query(Project).order_by(Project.id.desc()).all()

# 3. UPDATE (Protected)
@router.put("/{project_id}", response_model=ProjectOut)
async def update_project(
    request: Request,
    project_id: int,
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    github_link: Optional[str] = Form(None),
    live_demo: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    admin_check: str = Depends(verify_admin),
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

    # If a new file is uploaded, replace the old one
    if file:
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        base_url = str(request.base_url).rstrip('/')
        project.image_url = f"{base_url}/static/uploads/{unique_filename}"

    db.commit()
    db.refresh(project)
    return project

# 4. DELETE (Protected)
@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int, 
    admin_check: str = Depends(verify_admin),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Clean up the image file from storage
    if project.image_url:
        filename = project.image_url.split("/")[-1]
        old_file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.exists(old_file_path):
            try:
                os.remove(old_file_path)
            except Exception as e:
                print(f"Error deleting file: {e}")

    db.delete(project)
    db.commit()
    return None