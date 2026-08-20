import base64

from googleapiclient.discovery import build

from services.google_auth import get_credentials


def get_email_body(payload):

    # Simple email
    if "body" in payload:
        data = payload["body"].get("data")

        if data:
            return base64.urlsafe_b64decode(
                data
            ).decode(
                "utf-8",
                errors="ignore"
            )

    # Multipart email
    parts = payload.get("parts", [])

    for part in parts:

        if part.get("mimeType") == "text/plain":

            data = part.get("body", {}).get("data")

            if data:
                return base64.urlsafe_b64decode(
                    data
                ).decode(
                    "utf-8",
                    errors="ignore"
                )

        # Nested multipart
        if part.get("parts"):

            body = get_email_body(part)

            if body:
                return body

    return ""


def search_emails(query, max_results=5):

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
            q=query,
            maxResults=max_results,
        )
        .execute()
    )

    messages = results.get("messages", [])

    if not messages:

        return {
            "status": "success",
            "message": "No matching emails found."
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

        subject = ""
        sender = ""

        for header in msg["payload"].get(
            "headers", []
        ):

            if header["name"].lower() == "subject":
                subject = header["value"]

            elif header["name"].lower() == "from":
                sender = header["value"]

        body = get_email_body(
            msg["payload"]
        )

        output += (
            f"From: {sender}\n"
            f"Subject: {subject}\n"
            f"Body: {body}\n\n"
            "-------------------------\n\n"
        )

    return {
        "status": "success",
        "message": output
    }