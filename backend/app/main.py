from fastapi import FastAPI
from app.routes import auth, projects, services, hire, payments, contact, chatbot, admin

app = FastAPI(title="AI Portfolio System")

app.include_router(auth.router, prefix="/auth")
app.include_router(projects.router, prefix="/projects")
app.include_router(services.router, prefix="/services")
app.include_router(hire.router, prefix="/hire")
app.include_router(payments.router, prefix="/payments")
app.include_router(contact.router, prefix="/contact")
app.include_router(chatbot.router, prefix="/chatbot")
app.include_router(admin.router, prefix="/admin")

@app.get("/")
def root():
    return {"status": "Portfolio API running"}
