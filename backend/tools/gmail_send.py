import base64
from email.mime.text import MIMEText

from googleapiclient.discovery import build

from services.google_auth import get_credentials


def send_email(to, subject, body):
    print("\n========== GMAIL SEND ==========")
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")

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

    response = service.users().messages().send(
        userId="me",
        body={
            "raw": raw
        }
    ).execute()

    message_id = response.get("id")

    print(f"Gmail message ID: {message_id}")
    print("========== GMAIL SUCCESS ==========\n")

    return {
        "status": "success",
        "message": f"Email sent successfully to {to}",
        "message_id": message_id
    }