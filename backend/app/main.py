from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from app.routes import chatbot, messages
from app.routes import auth, projects, services
from app.database import engine, Base
from app.models import chat  # Import your chat model specifically

# This line creates all tables that don't exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Service Booking System API")

# 1. Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Path Configuration
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_PATH = BASE_DIR / "frontend" / "public"
UPLOAD_PATH = BASE_DIR / "backend" / "static" / "uploads"

# Verify Paths
print(f"\n🚀 FRONTEND PATH: {FRONTEND_PATH}")
if FRONTEND_PATH.exists():
    print("✅ Frontend Folder Found!")
    app.mount("/static", StaticFiles(directory=str(FRONTEND_PATH)), name="static")
else:
    print("❌ FRONTEND FOLDER NOT FOUND")

# Ensure upload directory exists
UPLOAD_PATH.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_PATH)), name="uploads")

# 3. Include Routers
# This connects your logic in auth.py, projects.py, etc., to the app
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(services.router, prefix="/api/services", tags=["Services"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["AI Assistant"])
app.include_router(messages.router, prefix="/api/messages", tags=["Messages"]) 

# 4. Root Route (Fixes the 404 on http://127.0.0.1:8000)
@app.get("/")
async def root():
    return {
        "message": "Service Booking System API is running",
        "docs": "/docs",
        "status": "online"
    }