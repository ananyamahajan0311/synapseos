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
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from agents.planner import Planner
from agents.executor import Executor
from services.ai_service import AIService
from services.email_service import EmailService

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET_KEY = "synapseos_secret_key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI()
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

class PromptRequest(BaseModel):
    prompt: str

class SendEmailRequest(BaseModel):
    to_email: str
    subject: str
    message: str

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

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

@app.get("/")
def home():

    return {
        "message": "SynapseOS Backend Running"
    }

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
@app.post("/signup")
def signup(data: SignupRequest):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_user:

        return {
            "message": "User already exists"
        }

    hashed_password = pwd_context.hash(
        data.password
    )

    new_user = User(
        username=data.username,
        email=data.email,
        password=hashed_password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    db.close()

    return {
        "message": "User created successfully"
    }

@app.post("/login")
def login(data: LoginRequest):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:

        return {
            "message": "User not found"
        }

    if not pwd_context.verify(
        data.password,
        user.password
    ):

        return {
            "message": "Incorrect password"
        }

    access_token = create_access_token(
        data={
            "sub": user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

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