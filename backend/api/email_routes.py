from fastapi import APIRouter

from api.schemas import PromptRequest, SendEmailRequest
from services.ai_service import AIService
from services.email_service import EmailService
from database import SessionLocal
from models import EmailHistory

router = APIRouter(tags=["Email"])

ai_service = AIService()
email_service = EmailService()


@router.post("/generate-email")
def generate_email(data: PromptRequest):

    email = ai_service.generate_email(data.prompt)

    return {
        "email": email
    }


@router.post("/send-email")
def send_email(data: SendEmailRequest):

    return email_service.send_email(
        data.to_email,
        data.subject,
        data.message
    )


@router.get("/email-history")
def get_email_history():

    db = SessionLocal()

    emails = db.query(EmailHistory).all()

    db.close()

    return emails