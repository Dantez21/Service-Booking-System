import os
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

router = APIRouter()

# --- EMAIL CONFIGURATION ---
# IMPORTANT: For Gmail, you must use an "App Password," not your regular password.
conf = ConnectionConfig(
    MAIL_USERNAME = "wambuadaniel21@gmail.com",
    MAIL_PASSWORD = "jmjb odbz byuh qfio",
    MAIL_FROM = "wambuadaniel21@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

class HireRequest(BaseModel):
    id: Optional[int] = None
    full_name: str
    email: str
    service_type: str
    budget: str
    details: str
    status: str = "Under Review"
    timestamp: datetime = datetime.now()

hire_db: List[HireRequest] = []

# --- THE REAL EMAIL LOGIC ---
async def send_real_email(email: str, name: str, status: str, service: str):
    subject = f"Update on your {service} request"
    
    # HTML content for a professional look
    html = f"""
    <h3>Hi {name},</h3>
    <p>We have an update regarding your hire request for <strong>{service}</strong>.</p>
    <p>Current Status: <span style="color: blue; font-weight: bold;">{status}</span></p>
    <p>Thank you for choosing our services!</p>
    """

    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)

# --- ROUTES ---

@router.get("/all", response_model=List[HireRequest])
async def get_all_hires():
    return hire_db

@router.post("/")
async def create_hire(request: HireRequest):
    new_id = len(hire_db) + 1
    request.id = new_id
    request.timestamp = datetime.now()
    hire_db.append(request)
    return {"message": "Success", "id": new_id}

@router.patch("/{hire_id}/status")
async def update_status(hire_id: int, status_update: dict, background_tasks: BackgroundTasks):
    for hire in hire_db:
        if hire.id == hire_id:
            new_status = status_update.get("status")
            hire.status = new_status
            
            # This now triggers a REAL email in the background
            background_tasks.add_task(
                send_real_email, 
                hire.email, 
                hire.full_name, 
                new_status, 
                hire.service_type
            )
            return hire
    raise HTTPException(status_code=404, detail="Request not found")