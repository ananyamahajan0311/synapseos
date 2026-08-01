import base64

from googleapiclient.discovery import build

from services.google_auth import get_credentials


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
                id=message["id"]
            )
            .execute()
        )

        headers = msg["payload"]["headers"]

        subject = ""
        sender = ""

        for header in headers:
            if header["name"] == "Subject":
                subject = header["value"]

            if header["name"] == "From":
                sender = header["value"]

        output += f"From: {sender}\n"
        output += f"Subject: {subject}\n\n"

    return {
        "status": "success",
        "message": output
    }