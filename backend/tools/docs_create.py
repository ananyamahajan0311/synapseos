from googleapiclient.discovery import build

from services.google_auth import get_credentials
from tools.docs_write import write_document
from tools.docs_parser import parse_document_request
from agents.llm import generate_content


def create_document(prompt):
    creds = get_credentials()

    # Parse title and preserve the user's full request
    title, content = parse_document_request(prompt)

    # Generate the actual document content using Gemini
    if content.strip():
        generated_content = generate_content(
            f"""
You are the document-generation engine for SynapseOS.

The user wants to create a Google Document.

USER REQUEST:
{content}

Your task is to fulfill the user's request exactly.

Understand the user's intent and generate the ACTUAL content
they requested.

Do not merely repeat or describe the request.

Examples:
- If the user asks for questions, generate the actual questions.
- If the user asks for answers, provide the actual answers.
- If the user asks for notes, generate the actual notes.
- If the user asks for a report, write the actual report.
- If the user asks for a list, provide the actual list.
- If the user asks for code, provide the requested code.
- If the user asks for explanations, provide the explanations.
- If the user asks for a specific number of items, generate exactly
  that number.

Follow ALL requirements in the user's request, including:
- topic
- quantity
- format
- difficulty
- structure
- language
- answers
- examples
- length
- any other constraints

Use clear headings, numbering, and formatting where appropriate.

Return ONLY the final content that should appear in the
Google Document.

Do not explain your process.
"""
        )
    else:
        generated_content = f"{title}\n\nCreated by SynapseOS."

    # Create Google Document
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

    # Write AI-generated content into the document
    write_document(
        document_id,
        generated_content
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