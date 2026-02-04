from sqlalchemy import Column, Integer, String, Float, Text
from ..database import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=True)