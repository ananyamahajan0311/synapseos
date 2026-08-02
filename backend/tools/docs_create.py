from googleapiclient.discovery import build

from services.google_auth import get_credentials
from tools.docs_write import write_document


def create_document(title):
    creds = get_credentials()

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

    # Write initial content
    write_document(
        document_id,
        f"{title}\n\nCreated by SynapseOS.\n"
    )

    return {
        "status": "success",
        "message": (
            f"Google Document created successfully.\n"
            f"https://docs.google.com/document/d/{document_id}/edit"
        ),
        "document_id": document_id
    }