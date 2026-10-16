from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.schemas import PromptRequest
from services.ai_service import AIService
from database import SessionLocal
from models import EmailHistory

from services.email_drafts import (
    send_approved_draft,
    cancel_draft,
    update_draft,
)

router = APIRouter(tags=["Email"])

ai_service = AIService()


class ApproveDraftRequest(BaseModel):
    to_email: str
    subject: str
    message: str
class UpdateDraftRequest(BaseModel):
    to_email: str
    subject: str
    message: str

@router.post("/generate-email")
def generate_email(data: PromptRequest):
    email = ai_service.generate_email(data.prompt)
    return {"email": email}

@router.put("/email-drafts/{draft_id}")
def edit_email_draft(
    draft_id: str,
    data: UpdateDraftRequest,
):
    result = update_draft(
        draft_id,
        data.to_email,
        data.subject,
        data.message,
    )

    if result.get("status") != "success":
        raise HTTPException(
            status_code=409,
            detail=result.get("message", "Draft could not be updated."),
        )

    return result


@router.post("/email-drafts/{draft_id}/send")
def approve_and_send_email(
    draft_id: str,
    data: ApproveDraftRequest
):
    result = send_approved_draft(
        draft_id,
        data.to_email,
        data.subject,
        data.message,
    )

    if result.get("status") != "success":
        raise HTTPException(
            status_code=409,
            detail=result.get(
                "message",
                "Email could not be sent."
            ),
        )

    return result


@router.post("/email-drafts/{draft_id}/cancel")
def cancel_email_draft(draft_id: str):
    result = cancel_draft(draft_id)

    if result.get("status") != "success":
        raise HTTPException(
            status_code=409,
            detail=result["message"],
        )

    return result


@router.post("/send-email")
def direct_send_disabled():
    raise HTTPException(
        status_code=403,
        detail=(
            "Direct email sending is disabled. "
            "Create a draft and approve it before sending."
        ),
    )


@router.get("/email-history")
def get_email_history():
    db = SessionLocal()

    try:
        return db.query(EmailHistory).all()
    finally:
        db.close()