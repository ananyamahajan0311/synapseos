from googleapiclient.discovery import build

from services.google_auth import get_credentials
from tools.docs_write import write_document
from tools.docs_parser import parse_document_request
from agents.llm import generate_content


def create_document(prompt):
    creds = get_credentials()

    # Parse the user's request
    title, content = parse_document_request(prompt)

    # Generate document content using Gemini
    if content.strip():
        generated_content = generate_content(
            f"""Write the content requested below for a Google Document.

Request:
{content}

Write clear, well-structured content suitable for a document.
Do not explain what you are doing. Return only the content."""
        )
    else:
        generated_content = f"{title}\n\nCreated by SynapseOS."

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

    # Write generated content into the document
    write_document(document_id, generated_content)

    return {
        "status": "success",
        "message": (
            f"Google Document created successfully.\n"
            f"https://docs.google.com/document/d/{document_id}/edit"
        ),
        "document_id": document_id
    }