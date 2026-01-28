from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.routes import projects, auth, services

app = FastAPI()

# 1. UPDATED CORS SETTINGS
# Using allow_origin_regex or a broader list helps when Live Server 
# switches ports (like 5500 to 5501).
# In main.py
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Keeping this for now since we know it works
    allow_credentials=True,
    allow_methods=["*"],
    # ADD 'x-admin-token' TO THIS LIST:
    allow_headers=["Content-Type", "x-admin-token", "Authorization"], 
)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,  # You can use ["*"] temporarily to test if this is the issue
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# 2. MOUNT STATIC FILES
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. ROUTES
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(services.router, prefix="/api/services", tags=["Services"])

@app.get("/")
def root():
    return {"message": "API is online"}