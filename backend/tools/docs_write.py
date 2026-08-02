from googleapiclient.discovery import build

from services.google_auth import get_credentials


def write_document(document_id, content):
    creds = get_credentials()

    service = build(
        "docs",
        "v1",
        credentials=creds
    )

    requests = [
        {
            "insertText": {
                "location": {
                    "index": 1
                },
                "text": content
            }
        }
    ]

    service.documents().batchUpdate(
        documentId=document_id,
        body={"requests": requests}
    ).execute()

    return {
        "status": "success",
        "message": "Content written successfully."
    }