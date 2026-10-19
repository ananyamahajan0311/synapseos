import re

from googleapiclient.discovery import build
from services.google_auth import get_credentials


def preview_document(document_id):
    if not isinstance(document_id, str) or not document_id.strip():
        return {"status": "error", "message": "A Google Docs URL or document ID is required."}

    value = document_id.strip()
    match = re.search(r"/document/d/([a-zA-Z0-9_-]+)", value)
    document_id = match.group(1) if match else value

    if not re.fullmatch(r"[a-zA-Z0-9_-]+", document_id):
        return {"status": "error", "message": "Please provide a valid Google Docs URL or document ID."}

    try:
        service = build("docs", "v1", credentials=get_credentials())
        document = service.documents().get(documentId=document_id).execute()
        content = []

        def extract_text(elements):
            for element in elements or []:
                if "paragraph" in element:
                    for item in element["paragraph"].get("elements", []):
                        text_run = item.get("textRun", {})
                        if text_run.get("content"):
                            content.append(text_run["content"])
                elif "table" in element:
                    for row in element["table"].get("tableRows", []):
                        for cell in row.get("tableCells", []):
                            extract_text(cell.get("content", []))
                elif "tableOfContents" in element:
                    extract_text(element["tableOfContents"].get("content", []))

        extract_text(document.get("body", {}).get("content", []))
        text = "".join(content).strip()
        url = f"https://docs.google.com/document/d/{document_id}/edit"

        return {
            "status": "success",
            "document_id": document_id,
            "title": document.get("title", "Untitled document"),
            "content": text,
            "url": url,
            "message": (
                f"Preview: {document.get('title', 'Untitled document')}\n\n"
                f"{text or 'This document has no readable text content.'}\n\n"
                f"Open document: {url}"
            )
        }
    except Exception:
        return {
            "status": "error",
            "message": "Could not preview the document. Check its URL or ID and Google access permissions."
        }