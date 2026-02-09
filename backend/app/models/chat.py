from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class ChatLog(Base):
    __tablename__ = "chat_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_ip = Column(String)
    message = Column(String)
    response = Column(String)
    # Change 'created_at' to 'timestamp' to match your DB
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
