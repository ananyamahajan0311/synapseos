
from datetime import datetime, timedelta, timezone
from threading import Lock
import re
import secrets

from tools.gmail_send import send_email


_drafts = {}
_drafts_lock = Lock()
DRAFT_TTL_MINUTES = 15


def _now():
    return datetime.now(timezone.utc)


def _public_draft(draft):
    return {
        "draft_id": draft["draft_id"],
        "to_email": draft["to_email"],
        "subject": draft["subject"],
        "body": draft["body"],
        "status": draft["status"],
        "expires_at": draft["expires_at"].isoformat(),
        "validation": draft["validation"],
    }


def create_draft(to_email, subject, body):
    to_email = (to_email or "").strip()

    valid_format = bool(
        re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", to_email)
    )

    warnings = [
        "Email format validation does not verify the recipient's identity."
    ]

    if not valid_format:
        warnings.append("The recipient email format appears invalid.")

    if not (subject or "").strip():
        warnings.append("The subject is empty.")

    if not (body or "").strip():
        warnings.append("The email body is empty.")

    now = _now()

    draft = {
        "draft_id": secrets.token_urlsafe(32),
        "to_email": to_email,
        "subject": subject or "",
        "body": body or "",
        "status": "pending",
        "created_at": now,
        "expires_at": now + timedelta(minutes=DRAFT_TTL_MINUTES),
        "validation": {
            "recipient_format_valid": valid_format,
            "warnings": warnings,
        },
    }

    with _drafts_lock:
        _drafts[draft["draft_id"]] = draft

    return _public_draft(draft)


def cancel_draft(draft_id):
    with _drafts_lock:
        draft = _drafts.get(draft_id)

        if not draft:
            return {
                "status": "error",
                "message": "Draft not found.",
            }

        if _now() >= draft["expires_at"]:
            draft["status"] = "expired"
            return {
                "status": "error",
                "message": "Draft expired. Generate a new email.",
            }

        if draft["status"] != "pending":
            return {
                "status": "error",
                "message": f"Draft cannot be cancelled: {draft['status']}.",
            }

        draft["status"] = "cancelled"

    return {
        "status": "success",
        "message": "Email draft cancelled. No email was sent.",
    }


def send_approved_draft(draft_id, to_email, subject, body):
    # Validate and reserve the draft before calling Gmail.
    with _drafts_lock:
        draft = _drafts.get(draft_id)

        if not draft:
            return {
                "status": "error",
                "message": "Draft not found or server restarted.",
            }

        if _now() >= draft["expires_at"]:
            draft["status"] = "expired"
            return {
                "status": "error",
                "message": "Draft expired. Generate a new email.",
            }

        if draft["status"] != "pending":
            return {
                "status": "error",
                "message": f"This draft cannot be sent: {draft['status']}.",
            }

        to_email = (to_email or "").strip()
        subject = subject or ""
        body = body or ""

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", to_email):
            return {
                "status": "error",
                "message": "Enter a valid email address.",
            }

        if not subject.strip():
            return {
                "status": "error",
                "message": "The email subject cannot be empty.",
            }

        if not body.strip():
            return {
                "status": "error",
                "message": "The email body cannot be empty.",
            }

        # Reserve the draft so concurrent requests cannot send it twice.
        draft["status"] = "sending"
        draft["to_email"] = to_email
        draft["subject"] = subject
        draft["body"] = body

    # Keep network requests outside the lock.
    try:
        result = send_email(to_email, subject, body)
    except Exception as exc:
        print("EMAIL SEND EXCEPTION:", repr(exc))

        with _drafts_lock:
            draft["status"] = "send_uncertain"

        return {
            "status": "error",
            "message": (
                "The send result could not be confirmed. "
                "Check Gmail before attempting another send."
            ),
        }

    print("GMAIL RESULT:", repr(result))

    with _drafts_lock:
        if isinstance(result, dict) and result.get("status") == "success":
            draft["status"] = "sent"
            draft["message_id"] = result.get("message_id")
        else:
            draft["status"] = "send_uncertain"

            return {
                "status": "error",
                "message": (
                    "Gmail returned an unexpected result. "
                    "Check your Sent folder before retrying."
                ),
            }

    return result
