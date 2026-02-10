from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.message import ContactMessage
from pydantic import BaseModel, EmailStr
from typing import List

router = APIRouter()

class MessageCreate(BaseModel):
    full_name: str
    email: EmailStr
    message: str

@router.post("/send")
async def send_message(msg: MessageCreate, db: Session = Depends(get_db)):
    new_msg = ContactMessage(**msg.dict())
    db.add(new_msg)
    db.commit()
    return {"message": "Message sent successfully!"}

@router.get("/all")
async def get_all_messages(db: Session = Depends(get_db)):
    return db.query(ContactMessage).order_by(ContactMessage.timestamp.desc()).all()

@router.delete("/delete/{msg_id}")
async def delete_message(msg_id: int, db: Session = Depends(get_db)):
    msg = db.query(ContactMessage).filter(ContactMessage.id == msg_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(msg)
    db.commit()
    return {"message": "Message deleted"}

# Add these to your messages.py
@router.patch("/{msg_id}/read")
async def toggle_read(msg_id: int, db: Session = Depends(get_db)):
    msg = db.query(ContactMessage).filter(ContactMessage.id == msg_id).first()
    msg.is_read = not msg.is_read
    db.commit()
    return {"status": "updated", "is_read": msg.is_read}

@router.patch("/{msg_id}/trash")
async def move_to_bin(msg_id: int, db: Session = Depends(get_db)):
    msg = db.query(ContactMessage).filter(ContactMessage.id == msg_id).first()
    msg.is_deleted = True # Hide from inbox, show in bin
    db.commit()
    return {"status": "moved to bin"}

@router.post("/delete-multiple")
async def delete_multiple(msg_ids: list[int], db: Session = Depends(get_db)):
    db.query(ContactMessage).filter(ContactMessage.id.in_(msg_ids)).update({"is_deleted": True}, synchronize_session=False)
    db.commit()
    return {"message": "Selected messages moved to bin"}

@router.patch("/{msg_id}/restore")
async def restore_message(msg_id: int, db: Session = Depends(get_db)):
    msg = db.query(ContactMessage).filter(ContactMessage.id == msg_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    
    msg.is_deleted = False  # Set back to active
    db.commit()
    return {"status": "success", "message": "Message restored to inbox"}