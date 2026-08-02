from googleapiclient.discovery import build

from services.google_auth import get_credentials


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

    return {
        "status": "success",
        "message": (
            "Google Document created successfully.\n"
            f"https://docs.google.com/document/d/{document['documentId']}/edit"
        ),
        "document_id": document["documentId"]
    }