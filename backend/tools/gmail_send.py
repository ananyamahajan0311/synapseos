import base64
from email.mime.text import MIMEText

from googleapiclient.discovery import build

from services.google_auth import get_credentials


def send_email(to, subject, body):
    creds = get_credentials()

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    message = MIMEText(body)

    message["to"] = to
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    service.users().messages().send(
        userId="me",
        body={
            "raw": raw
        }
    ).execute()

    return {
        "status": "success",
        "message": f"Email sent successfully to {to}"
    }