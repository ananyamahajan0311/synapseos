import base64

from bs4 import BeautifulSoup
from googleapiclient.discovery import build

from services.google_auth import get_credentials


def decode_body(data):
    """Decode Gmail's base64 encoded email body."""
    if not data:
        return ""

    try:
        return base64.urlsafe_b64decode(data).decode(
            "utf-8",
            errors="ignore"
        )
    except Exception:
        return ""


def clean_html(html):
    """Convert HTML email content into clean readable text."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove elements that don't contain useful email text
    for element in soup(["script", "style"]):
        element.decompose()

    return soup.get_text(
        separator="\n",
        strip=True
    )


def get_email_body(payload):
    """
    Extract the best available email body.

    Preference:
    1. text/plain
    2. text/html converted to clean text
    3. nested multipart content
    """

    plain_text = ""
    html_text = ""

    # Check the current payload
    body = payload.get("body", {})
    data = body.get("data")

    if data:
        decoded = decode_body(data)

        mime_type = payload.get("mimeType", "")

        if mime_type == "text/plain":
            plain_text = decoded

        elif mime_type == "text/html":
            html_text = clean_html(decoded)

    # Check multipart sections
    parts = payload.get("parts", [])

    for part in parts:

        mime_type = part.get("mimeType", "")

        part_body = part.get("body", {})
        data = part_body.get("data")

        if data:

            decoded = decode_body(data)

            if mime_type == "text/plain":
                plain_text = decoded

            elif mime_type == "text/html":
                html_text = clean_html(decoded)

        # Recursively check nested multipart sections
        if part.get("parts"):

            nested_body = get_email_body(part)

            if nested_body:
                return nested_body

    # Prefer plain text
    if plain_text.strip():
        return plain_text.strip()

    # Otherwise use cleaned HTML
    if html_text.strip():
        return html_text.strip()

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
            "headers",
            []
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
            f"Body:\n{body}\n\n"
            "-------------------------\n\n"
        )

    return {
        "status": "success",
        "message": output
    }