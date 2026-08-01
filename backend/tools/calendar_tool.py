from datetime import datetime, timedelta

from googleapiclient.discovery import build

from services.google_auth import get_credentials


def create_event(summary):
    creds = get_credentials()

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    start = datetime.utcnow() + timedelta(minutes=5)
    end = start + timedelta(hours=1)

    event = {
        "summary": summary,
        "start": {
            "dateTime": start.isoformat() + "Z",
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": end.isoformat() + "Z",
            "timeZone": "Asia/Kolkata",
        },
    }

    event = service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    return {
        "status": "success",
        "message": f"Calendar event created.\n{event['htmlLink']}"
    }