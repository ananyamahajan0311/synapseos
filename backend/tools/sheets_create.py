from googleapiclient.discovery import build

from services.google_auth import get_credentials


def create_sheet(title, data=None):
    creds = get_credentials()

    service = build(
        "sheets",
        "v4",
        credentials=creds
    )

    spreadsheet = {
        "properties": {
            "title": title
        }
    }

    sheet = service.spreadsheets().create(
        body=spreadsheet
    ).execute()

    spreadsheet_id = sheet["spreadsheetId"]

    # Add data if provided
    if data:
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range="Sheet1!A1",
            valueInputOption="USER_ENTERED",
            body={
                "values": data
            }
        ).execute()

    return {
        "status": "success",
        "message": (
            "Google Spreadsheet created successfully.\n"
            f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
        ),
        "spreadsheet_id": spreadsheet_id
    }