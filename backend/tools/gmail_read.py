import base64
import re
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from services.google_auth import get_credentials


def decode_body(data):
    """Decode Gmail base64 encoded content."""
    if not data:
        return ""

    try:
        return base64.urlsafe_b64decode(data).decode(
            "utf-8",
            errors="ignore"
        )
    except Exception:
        return ""


def clean_text(text):
    """Clean unnecessary URLs and email formatting."""

    if not text:
        return ""

    # Convert HTML to readable text if HTML is present
    if "<html" in text.lower() or "<body" in text.lower():
        soup = BeautifulSoup(text, "html.parser")

        for element in soup(["script", "style", "a"]):
            element.decompose()

        text = soup.get_text(
            separator="\n",
            strip=True
        )

    # Remove long URLs
    text = re.sub(
        r'https?://\S+',
        '',
        text
    )

    # Remove excessive blank lines
    text = re.sub(
        r'\n\s*\n+',
        '\n\n',
        text
    )

    # Remove excessive spaces
    text = re.sub(
        r'[ \t]+',
        ' ',
        text
    )

    return text.strip()


def get_email_body(payload):
    """
    Extract the best available email body.

    Priority:
    1. text/plain
    2. text/html
    3. nested multipart sections
    """

    plain_text = ""
    html_text = ""

    body = payload.get("body", {})
    data = body.get("data")

    if data:

        decoded = decode_body(data)

        mime_type = payload.get("mimeType", "")

        if mime_type == "text/plain":
            plain_text = decoded

        elif mime_type == "text/html":
            html_text = decoded

    for part in payload.get("parts", []):

        mime_type = part.get("mimeType", "")
        part_body = part.get("body", {})
        data = part_body.get("data")

        if data:

            decoded = decode_body(data)

            if mime_type == "text/plain":
                plain_text = decoded

            elif mime_type == "text/html":
                html_text = decoded

        if part.get("parts"):

            nested = get_email_body(part)

            if nested:
                return nested

    if plain_text.strip():
        return clean_text(plain_text)

    if html_text.strip():
        return clean_text(html_text)

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

        headers = msg["payload"].get("headers", [])

        subject = ""
        sender = ""

        for header in headers:

            if header["name"].lower() == "subject":
                subject = header["value"]

            elif header["name"].lower() == "from":
                sender = header["value"]

        body = get_email_body(msg["payload"])

        output += (
            f"From: {sender}\n"
            f"Subject: {subject}\n"
            f"Body:\n{body}\n"
            "\n-------------------------\n\n"
        )

    return {
        "status": "success",
        "message": output
    }