from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from ..database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=True) # Link to your images
    category = Column(String(100), index=True)      # e.g., AI, Data Science
    github_link = Column(String(500), nullable=True)
    live_demo = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)