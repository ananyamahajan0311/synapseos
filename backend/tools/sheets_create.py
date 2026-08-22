import json
import re

from googleapiclient.discovery import build

from services.google_auth import get_credentials
from agents.llm import generate_content


def create_sheet(prompt):
    creds = get_credentials()

    # Ask Gemini to convert the user's request into structured
    # spreadsheet data.
    ai_prompt = f"""
You are the spreadsheet-generation engine for SynapseOS.

The user wants to create a Google Spreadsheet.

USER REQUEST:
{prompt}

Understand the user's request and generate the ACTUAL spreadsheet
content they requested.

Return ONLY valid JSON.

The JSON must have exactly this structure:

{{
  "title": "Spreadsheet title",
  "rows": [
    ["Column 1", "Column 2", "Column 3"],
    ["Value 1", "Value 2", "Value 3"]
  ]
}}

Rules:
- The first row must contain column headers.
- Every following row must contain the actual requested data.
- If the user requests a specific number of items, generate exactly
  that number.
- Use as many columns as necessary.
- Do not add Markdown.
- Do not use ```json.
- Do not explain anything.
- Return only the JSON object.
"""

    generated = generate_content(ai_prompt)

    # Remove accidental Markdown code fences if Gemini adds them.
    generated = re.sub(r"```json|```", "", generated).strip()

    try:
        spreadsheet_data = json.loads(generated)

        title = spreadsheet_data.get(
            "title",
            "SynapseOS Spreadsheet"
        )

        data = spreadsheet_data.get(
            "rows",
            []
        )

        if not data:
            return {
                "status": "error",
                "message": "Gemini generated no spreadsheet data."
            }

    except json.JSONDecodeError as e:
        return {
            "status": "error",
            "message": (
                "Could not parse AI-generated spreadsheet data.\n"
                f"Error: {str(e)}"
            )
        }

    # Create Google Sheets service
    service = build(
        "sheets",
        "v4",
        credentials=creds
    )

    # Create spreadsheet
    spreadsheet = {
        "properties": {
            "title": title
        }
    }

    sheet = service.spreadsheets().create(
        body=spreadsheet
    ).execute()

    spreadsheet_id = sheet["spreadsheetId"]

    # Write AI-generated rows
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range="Sheet1!A1",
        valueInputOption="USER_ENTERED",
        body={
            "values": data
        }
    ).execute()

    spreadsheet_url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{spreadsheet_id}/edit"
    )

    return {
        "status": "success",
        "message": (
            "Google Spreadsheet created successfully.\n"
            f"{spreadsheet_url}"
        ),
        "spreadsheet_id": spreadsheet_id,
        "url": spreadsheet_url
    }