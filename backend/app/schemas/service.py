from pydantic import BaseModel

class ServiceBase(BaseModel):
    title: str
    icon_class: str
    description: str

class ServiceCreate(ServiceBase):
    pass

class ServiceOut(ServiceBase):
    id: int
    class Config:
        from_attributes = True