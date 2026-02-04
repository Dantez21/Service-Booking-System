from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectBase(BaseModel):
    title: str
    description: str
    image_url: Optional[str] = None
    category: str
    github_link: Optional[str] = None
    live_demo: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True