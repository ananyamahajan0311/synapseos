
from datetime import datetime, timedelta, timezone
import re
import secrets

from sqlalchemy import update

from database import SessionLocal
from models import EmailDraft
from tools.gmail_send import send_email
from services.email_validation import validate_email_address

DRAFT_TTL_MINUTES = 15


def _now():
    return datetime.now(timezone.utc)


def _utc(value):
    # SQLite may return naive datetimes even when timezone=True.
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _public_draft(draft):
    valid_format = validate_email_address(draft.recipient)

    warnings = [
        "Email format validation does not verify the recipient's identity."
    ]

    if not valid_format:
        warnings.append("The recipient email format appears invalid.")
    if not (draft.subject or "").strip():
        warnings.append("The subject is empty.")
    if not (draft.body or "").strip():
        warnings.append("The email body is empty.")

    return {
        "draft_id": draft.draft_id,
        "to_email": draft.recipient,
        "subject": draft.subject,
        "body": draft.body,
        "status": draft.status,
        "expires_at": _utc(draft.expires_at).isoformat(),
        "validation": {
            "recipient_format_valid": valid_format,
            "warnings": warnings,
        },
    }


def create_draft(to_email, subject, body):
    to_email = (to_email or "").strip()
    if not validate_email_address(to_email):
        return {
        "status": "error",
        "message": "Enter a valid email address.",
    }
    subject = subject or ""
    body = body or ""
    now = _now()

    draft = EmailDraft(
        draft_id=secrets.token_urlsafe(32),
        recipient=to_email,
        subject=subject,
        body=body,
        status="pending",
        created_at=now,
        expires_at=now + timedelta(minutes=DRAFT_TTL_MINUTES),
        updated_at=now,
    )

    db = SessionLocal()
    try:
        db.add(draft)
        db.commit()
        db.refresh(draft)
        return _public_draft(draft)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def update_draft(draft_id, to_email, subject, body):
    to_email = (to_email or "").strip()
    subject = subject or ""
    body = body or ""

    if not validate_email_address(to_email):
        return {"status": "error", "message": "Enter a valid email address."}

    if not subject.strip():
        return {"status": "error", "message": "The email subject cannot be empty."}

    if not body.strip():
        return {"status": "error", "message": "The email body cannot be empty."}

    db = SessionLocal()
    try:
        now = _now()

        result = db.execute(
            update(EmailDraft)
            .where(
                EmailDraft.draft_id == draft_id,
                EmailDraft.status == "pending",
                EmailDraft.expires_at > now,
            )
            .values(
                recipient=to_email,
                subject=subject,
                body=body,
                updated_at=now,
            )
        )

        if result.rowcount != 1:
            db.rollback()

            draft = (
                db.query(EmailDraft)
                .filter(EmailDraft.draft_id == draft_id)
                .first()
            )

            if not draft:
                return {"status": "error", "message": "Draft not found."}

            if draft.status == "pending" and now >= _utc(draft.expires_at):
                draft.status = "expired"
                draft.updated_at = now
                db.commit()
                return {
                    "status": "error",
                    "message": "Draft expired. Generate a new email.",
                }

            return {
                "status": "error",
                "message": f"Draft cannot be edited: {draft.status}.",
            }

        db.commit()

        draft = (
            db.query(EmailDraft)
            .filter(EmailDraft.draft_id == draft_id)
            .first()
        )

        return {
            "status": "success",
            "draft": _public_draft(draft),
            "message": "Draft updated. Review it before approving.",
        }

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def cancel_draft(draft_id):
    db = SessionLocal()
    try:
        draft = (
            db.query(EmailDraft)
            .filter(EmailDraft.draft_id == draft_id)
            .with_for_update()
            .first()
        )

        if not draft:
            return {"status": "error", "message": "Draft not found."}

        if _now() >= _utc(draft.expires_at):
            if draft.status == "pending":
                draft.status = "expired"
                draft.updated_at = _now()
                db.commit()
            return {
                "status": "error",
                "message": "Draft expired. Generate a new email.",
            }

        if draft.status != "pending":
            return {
                "status": "error",
                "message": f"Draft cannot be cancelled: {draft.status}.",
            }

        draft.status = "cancelled"
        draft.updated_at = _now()
        db.commit()

        return {
            "status": "success",
            "message": "Email draft cancelled. No email was sent.",
        }
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()



def send_approved_draft(draft_id, to_email, subject, body):
    to_email = (to_email or "").strip()
    subject = subject or ""
    body = body or ""

    if not validate_email_address(to_email):
        return {"status": "error", "message": "Enter a valid email address."}

    if not subject.strip():
        return {"status": "error", "message": "The email subject cannot be empty."}

    if not body.strip():
        return {"status": "error", "message": "The email body cannot be empty."}

    db = SessionLocal()
    try:
        now = _now()

        # Claim only if the submitted content exactly matches the saved draft.
        claim = db.execute(
            update(EmailDraft)
            .where(
                EmailDraft.draft_id == draft_id,
                EmailDraft.status == "pending",
                EmailDraft.expires_at > now,
                EmailDraft.recipient == to_email,
                EmailDraft.subject == subject,
                EmailDraft.body == body,
            )
            .values(
                status="sending",
                approved_at=now,
                updated_at=now,
                last_error=None,
            )
        )

        if claim.rowcount != 1:
            db.rollback()
            draft = (
                db.query(EmailDraft)
                .filter(EmailDraft.draft_id == draft_id)
                .first()
            )

            if not draft:
                return {"status": "error", "message": "Draft not found."}

            if draft.status == "pending" and now >= _utc(draft.expires_at):
                draft.status = "expired"
                draft.updated_at = now
                db.commit()
                return {
                    "status": "error",
                    "message": "Draft expired. Generate a new email.",
                }

            if draft.status == "pending":
                return {
                    "status": "error",
                    "message": (
                        "The approved email does not match the saved draft. "
                        "Save and approve the updated draft before sending."
                    ),
                }

            return {
                "status": "error",
                "message": f"This draft cannot be sent: {draft.status}.",
            }

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    
    # Never hold a database transaction open during the Gmail request.
    try:
        result = send_email(to_email, subject, body)
       
    except Exception as exc:
        print("EMAIL SEND EXCEPTION TYPE:", type(exc).__name__)
        failure_status = _classify_gmail_error(exc)
        error_message = (
            "Gmail rejected the request. Check the error details before "
            "creating a new draft."
            if failure_status == "failed"
            else "The send outcome could not be confirmed. "
                 "Check Gmail before attempting another send."
        )
        _set_send_result(
            draft_id,
            failure_status,
            error=error_message,
        )
        return {
            "status": "error",
            "message": error_message,
        }


        

    
    if (
        isinstance(result, dict)
        and result.get("status") == "success"
        and result.get("message_id")
    ):
        status_saved = _set_send_result(
            draft_id,
            "sent",
            message_id=result["message_id"],
        )

        if not status_saved:
            return {
                **result,
                "status_persisted": False,
                "message": (
                    "Gmail accepted the email, but SynapseOS could not "
                    "save the final status. Do not resend the email. "
                    "Check your Gmail Sent folder."
                ),
            }

        return {
            **result,
            "status_persisted": True,
        }

    _set_send_result(
        draft_id,
        "send_uncertain",
        error="Gmail returned an unexpected result.",
    )
    return {
        "status": "error",
        "message": (
            "Gmail returned an unexpected result. "
            "Check your Sent folder before retrying."
        ),
    }




def _set_send_result(draft_id, status, message_id=None, error=None):
    db = SessionLocal()
    try:
        draft = (
            db.query(EmailDraft)
            .filter(EmailDraft.draft_id == draft_id)
            .first()
        )

        if not draft:
            return False

        draft.status = status
        draft.message_id = message_id
        draft.last_error = error
        draft.updated_at = _now()
        db.commit()
        return True

    except Exception:
        db.rollback()
        import traceback
        traceback.print_exc()
        return False

    finally:
        db.close()



def recover_incomplete_sends():
    """Mark sends interrupted by a restart as uncertain, never resend them."""
    db = SessionLocal()
    try:
        drafts = (
            db.query(EmailDraft)
            .filter(EmailDraft.status == "sending")
            .all()
        )
        now = _now()
        for draft in drafts:
            draft.status = "send_uncertain"
            draft.last_error = (
                "Backend restarted while this send was in progress. "
                "Check Gmail before taking further action."
            )
            draft.updated_at = now

        db.commit()
        return len(drafts)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def _classify_gmail_error(exc):
    """Conservatively classify Gmail API errors."""
    from googleapiclient.errors import HttpError

    if isinstance(exc, HttpError):
        status_code = getattr(exc.resp, "status", None)

        if status_code == 400:
            return "failed"

    return "send_uncertain"
 