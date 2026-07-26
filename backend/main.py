from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google import genai
import os
from database import engine, SessionLocal
from models import EmailHistory
from database import Base
from agents.planner import Planner
from agents.executor import Executor
from services.ai_service import AIService
from services.email_service import EmailService
from api.health_routes import router as health_router
from api.auth_routes import router as auth_router
from api.schemas import PromptRequest, SendEmailRequest

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

app = FastAPI()
app.include_router(health_router)
app.include_router(auth_router)
planner = Planner()
executor = Executor()
ai_service = AIService()
email_service = EmailService()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-email")
def generate_email(data: PromptRequest):

    email = ai_service.generate_email(data.prompt)

    return {
        "email": email
    }
@app.post("/send-email")
def send_email(data: SendEmailRequest):

    return email_service.send_email(
        data.to_email,
        data.subject,
        data.message
    )

@app.get("/email-history")
def get_email_history():

    db = SessionLocal()

    emails = db.query(EmailHistory).all()

    db.close()

    return emails
@app.post("/chat")
def chat(data: PromptRequest):

    plan = planner.plan(data.prompt)

    result = executor.execute(plan)

    return {
        "message": data.prompt,
        "plan": plan,
        "result": result
    }