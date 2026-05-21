from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import os
import smtplib
from email.mime.text import MIMEText
from database import engine, SessionLocal
from models import User
from database import Base
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

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

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Write a professional email:\n{data.prompt}"
    )

    return {
        "email": response.text
    }

@app.post("/send-email")
def send_email(data: SendEmailRequest):

    sender_email = os.getenv("EMAIL_ADDRESS")

    sender_password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText(data.message)

    msg["Subject"] = data.subject

    msg["From"] = sender_email

    msg["To"] = data.to_email

    server = smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    )

    server.login(
        sender_email,
        sender_password
    )

    server.sendmail(
        sender_email,
        data.to_email,
        msg.as_string()
    )

    server.quit()

    return {
        "message": "Email sent successfully"
    }

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