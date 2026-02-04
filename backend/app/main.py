from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.routes import projects, auth, services

app = FastAPI(title="Portfolio API")

# 1. FINALIZED CORS SETTINGS
# Using ["*"] for allow_origins is best for local Wi-Fi testing 
# because it allows your phone (IP 192.168.0.61) and laptop (127.0.0.1) 
# to talk to the backend without restriction.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    # Explicitly allow the custom header you created for admin access
    allow_headers=["Content-Type", "x-admin-token", "Authorization"], 
)

# 2. MOUNT STATIC FILES
# Ensure the "static" folder exists in your backend root.
# This serves your uploaded project images.
if not os.path.exists("static"):
    os.makedirs("static")
    
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. ROUTES
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(services.router, prefix="/api/services", tags=["Services"])

@app.get("/")
def root():
    return {
        "message": "API is online",
        "status": "Ready for cross-device connections"
    }