from googleapiclient.discovery import build

from services.google_auth import get_credentials


def list_documents():
    creds = get_credentials()

    service = build(
        "drive",
        "v3",
        credentials=creds
    )

    results = service.files().list(
        q="mimeType='application/vnd.google-apps.document'",
        pageSize=10,
        fields="files(id,name)"
    ).execute()

    files = results.get("files", [])

    if not files:
        return {
            "status": "success",
            "message": "No Google Docs found."
        }

    message = "Your Google Documents:\n\n"

    for file in files:
        message += (
            f"{file['name']}\n"
            f"https://docs.google.com/document/d/{file['id']}/edit\n\n"
        )

    return {
        "status": "success",
        "message": message
    }