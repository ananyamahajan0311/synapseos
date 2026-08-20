from googleapiclient.discovery import build

from services.google_auth import get_credentials
from tools.docs_write import write_document
from tools.docs_parser import parse_document_request


def create_document(prompt):
    creds = get_credentials()

    # Parse title and requested content
    title, content = parse_document_request(prompt)

    # Do NOT call Gemini for now.
    # Use the user's requested content directly.
    if content.strip():
        document_content = content
    else:
        document_content = f"{title}\n\nCreated by SynapseOS."

    service = build(
        "docs",
        "v1",
        credentials=creds
    )

    # Create Google Document
    document = service.documents().create(
        body={
            "title": title
        }
    ).execute()

    document_id = document["documentId"]

    # Write content into the document
    write_document(
        document_id,
        document_content
    )

    document_url = (
        f"https://docs.google.com/document/d/{document_id}/edit"
    )

    return {
        "status": "success",
        "message": (
            "Google Document created successfully.\n"
            f"{document_url}"
        ),
        "document_id": document_id,
        "url": document_url
    }