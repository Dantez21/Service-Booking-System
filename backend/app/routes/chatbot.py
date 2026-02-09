import csv
from io import StringIO
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.chat import ChatLog
from pydantic import BaseModel
from sqlalchemy import delete
from typing import List
from rapidfuzz import process, fuzz

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

# --- LOCAL KNOWLEDGE BASE ---
KNOWLEDGE_BASE = {
    "who are you": "I am Daniel Wambua's AI Assistant. I help answer questions about his work in Software Engineering and XR Development.",
    "pricing": "Web apps start at KES 50k, while XR/VR projects start at KES 80k. Prices vary based on complexity!",
    "tech stack": "Daniel specializes in Python (FastAPI), PostgreSQL, Unity, and XR Development.",
    "contact": "You can reach Daniel via the contact form on this website or find him on LinkedIn.",
    "services": "We offer Custom Web Development, VR/AR (XR) solutions, and Backend Architecture design.",
    "location": "Daniel is based in Nairobi, Kenya, but works with clients globally.",
}

@router.post("/chat")
async def chat_with_ai(req: ChatRequest, request: Request, db: Session = Depends(get_db)):
    user_msg = req.message.lower().strip()
    
    # Fuzzy match (60% threshold)
    match = process.extractOne(user_msg, KNOWLEDGE_BASE.keys(), scorer=fuzz.WRatio)
    
    if match and match[1] > 60:
        bot_response = KNOWLEDGE_BASE[match[0]]
    else:
        bot_response = "I'm not sure about that. Try asking about Daniel's pricing, tech stack, or contact info!"

    # Log to Database
    new_log = ChatLog(
        user_ip=request.client.host,
        message=req.message,
        response=bot_response
        # Note: 'timestamp' is filled automatically by the database server_default
    )
    db.add(new_log)
    db.commit()

    return {"response": bot_response}

@router.get("/logs")
async def get_logs(db: Session = Depends(get_db)):
    # Returns logs ordered by newest first
    return db.query(ChatLog).order_by(ChatLog.id.desc()).all()

@router.delete("/clear")
async def clear_logs(db: Session = Depends(get_db)):
    """Deletes all chat logs from the database."""
    try:
        db.execute(delete(ChatLog))
        db.commit()
        return {"message": "All chat logs have been cleared successfully!"}
    except Exception as e:
        db.rollback()
        print(f"Delete Error: {e}")
        return {"error": "Could not clear logs."}, 500

@router.get("/export")
async def export_logs(db: Session = Depends(get_db)):
    """Exports chat history to a CSV file."""
    logs = db.query(ChatLog).all()
    
    output = StringIO()
    writer = csv.writer(output)
    # Headers
    writer.writerow(["ID", "Timestamp", "IP Address", "User Message", "AI Response"])
    
    for log in logs:
        # Changed log.created_at to log.timestamp to match your DB
        writer.writerow([log.id, log.timestamp, log.user_ip, log.message, log.response])
    
    output.seek(0)
    return StreamingResponse(
        output, 
        media_type="text/csv", 
        headers={"Content-Disposition": "attachment; filename=chat_logs_export.csv"}
    )

@router.post("/delete-multiple")
async def delete_multiple(log_ids: List[int], db: Session = Depends(get_db)):
    """Deletes specific logs based on a list of IDs."""
    try:
        db.execute(delete(ChatLog).where(ChatLog.id.in_(log_ids)))
        db.commit()
        return {"message": f"Successfully deleted {len(log_ids)} logs."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))