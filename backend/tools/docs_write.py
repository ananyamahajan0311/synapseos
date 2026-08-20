from googleapiclient.discovery import build

from services.google_auth import get_credentials


def write_document(document_id, content):
    creds = get_credentials()

    service = build(
        "docs",
        "v1",
        credentials=creds
    )

    # Insert the complete content first
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

    # Find heading lines and format them
    formatting_requests = []

    lines = content.splitlines()
    current_index = 1

    for line in lines:
        line_length = len(line) + 1

        if line.startswith("# "):
            heading_text = line[2:]

            formatting_requests.append({
                "updateParagraphStyle": {
                    "range": {
                        "startIndex": current_index,
                        "endIndex": current_index + len(line)
                    },
                    "paragraphStyle": {
                        "namedStyleType": "HEADING_1"
                    },
                    "fields": "namedStyleType"
                }
            })

        current_index += line_length

    if formatting_requests:
        service.documents().batchUpdate(
            documentId=document_id,
            body={"requests": formatting_requests}
        ).execute()

    return {
        "status": "success",
        "message": "Content written successfully."
    }