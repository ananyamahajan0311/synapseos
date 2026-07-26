from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import os
import smtplib
from email.mime.text import MIMEText
from database import engine, SessionLocal
from models import User, EmailHistory
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

SECRET_KEY = "synapseos_secret_key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI()
app.include_router(health_router)
app.include_router(auth_router)
planner = Planner()
executor = Executor()
ai_service = AIService()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


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
    email_service = EmailService()