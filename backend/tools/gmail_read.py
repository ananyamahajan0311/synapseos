import base64

from googleapiclient.discovery import build
from services.google_auth import get_credentials


def get_email_body(payload):
    """
    Extract plain-text body from Gmail message payload.
    """

    # Simple email with body directly available
    if payload.get("body", {}).get("data"):
        data = payload["body"]["data"]
        return base64.urlsafe_b64decode(data).decode("utf-8")

    # Multipart email
    for part in payload.get("parts", []):
        if part["mimeType"] == "text/plain":
            data = part.get("body", {}).get("data")

            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8")

        # Check nested parts
        if part.get("parts"):
            body = get_email_body(part)

            if body:
                return body

    return ""


def read_emails(max_results=5):

    creds = get_credentials()

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    results = (
        service.users()
        .messages()
        .list(
            userId="me",
            maxResults=max_results,
        )
        .execute()
    )

    messages = results.get("messages", [])

    if not messages:
        return {
            "status": "success",
            "message": "No emails found."
        }

    output = ""

    for message in messages:

        msg = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=message["id"],
                format="full"
            )
            .execute()
        )

        headers = msg["payload"]["headers"]

        subject = ""
        sender = ""

        for header in headers:

            if header["name"].lower() == "subject":
                subject = header["value"]

            elif header["name"].lower() == "from":
                sender = header["value"]

        body = get_email_body(msg["payload"])

        output += f"From: {sender}\n"
        output += f"Subject: {subject}\n"
        output += f"Body: {body}\n"
        output += "\n-------------------------\n\n"

    return {
        "status": "success",
        "message": output
    }