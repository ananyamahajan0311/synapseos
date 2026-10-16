
import base64
from email.mime.text import MIMEText

from googleapiclient.discovery import build

from services.google_auth import get_credentials


def send_email(to, subject, body):
    creds = get_credentials()

    service = build(
        "gmail",
        "v1",
        credentials=creds,
    )

    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    response = service.users().messages().send(
        userId="me",
        body={"raw": raw},
    ).execute()

    message_id = response.get("id")

    if not message_id:
        return {
            "status": "error",
            "message": (
                "Gmail returned no message ID. "
                "Check the Sent folder before retrying."
            ),
        }

    return {
        "status": "success",
        "message": "Gmail accepted the email for sending.",
        "message_id": message_id,
    }
