from googleapiclient.discovery import build

from services.google_auth import get_credentials
from tools.docs_write import write_document
from tools.docs_parser import parse_document_request


def create_document(prompt):
    creds = get_credentials()

    # Parse the user's request
    title, content = parse_document_request(prompt)

    service = build(
        "docs",
        "v1",
        credentials=creds
    )

    document = service.documents().create(
        body={
            "title": title
        }
    ).execute()

    document_id = document["documentId"]

    # Write content if provided
    if content.strip():
        write_document(document_id, content)
    else:
        write_document(
            document_id,
            f"{title}\n\nCreated by SynapseOS."
        )

    return {
        "status": "success",
        "message": (
            f"Google Document created successfully.\n"
            f"https://docs.google.com/document/d/{document_id}/edit"
        ),
        "document_id": document_id
    }