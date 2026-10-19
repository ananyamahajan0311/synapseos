import re

from googleapiclient.discovery import build
from services.google_auth import get_credentials


def preview_spreadsheet(spreadsheet_id):
    if not isinstance(spreadsheet_id, str) or not spreadsheet_id.strip():
        return {
            "status": "error",
            "message": "A Google Sheets URL or spreadsheet ID is required."
        }

    value = spreadsheet_id.strip()
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9_-]+)", value)
    spreadsheet_id = match.group(1) if match else value

    if not re.fullmatch(r"[a-zA-Z0-9_-]+", spreadsheet_id):
        return {
            "status": "error",
            "message": "Please provide a valid Google Sheets URL or spreadsheet ID."
        }

    try:
        service = build("sheets", "v4", credentials=get_credentials())

        spreadsheet = service.spreadsheets().get(
            spreadsheetId=spreadsheet_id,
            fields="spreadsheetId,properties(title),sheets(properties(title))"
        ).execute()

        previews = []

        for sheet in spreadsheet.get("sheets", []):
            title = sheet.get("properties", {}).get("title", "Sheet")
            escaped_title = title.replace("'", "''")

            values = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=f"'{escaped_title}'!A1:Z50"
            ).execute().get("values", [])

            previews.append({
                "sheet_name": title,
                "values": values
            })

        title = spreadsheet.get("properties", {}).get(
            "title", "Untitled spreadsheet"
        )
        url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"

        preview_text = []

        for sheet in previews:
            preview_text.append(f"Sheet: {sheet['sheet_name']}")
            preview_text.extend(
                " | ".join(str(cell) for cell in row)
                for row in sheet["values"]
            )

        content = "\n".join(preview_text) or "This spreadsheet has no readable cell data."

        return {
            "status": "success",
            "title": title,
            "spreadsheet_id": spreadsheet_id,
            "sheets": previews,
            "url": url,
            "message": (
                f"Preview: {title}\n\n{content}\n\n"
                f"Open spreadsheet: {url}"
            )
        }

    except Exception:
        return {
            "status": "error",
            "message": "Could not preview the spreadsheet. Check its URL or ID and Google access permissions."
        }