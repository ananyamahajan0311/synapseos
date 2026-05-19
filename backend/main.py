from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import os
import smtplib
from email.mime.text import MIMEText

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

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

@app.get("/")
def home():
    return {"message": "SynapseOS Backend Running"}

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

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    server.login(sender_email, sender_password)

    server.sendmail(
        sender_email,
        data.to_email,
        msg.as_string()
    )

    server.quit()

    return {
        "message": "Email sent successfully"
    }