from googleapiclient.discovery import build

from services.google_auth import get_credentials
from tools.calendar_parser import parse_event


def create_event(user_input):
    creds = get_credentials()

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    title, start, end = parse_event(user_input)

    event = {
        "summary": title,
        "start": {
            "dateTime": start.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": end.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
    }

    event = service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    return {
        "status": "success",
        "message": (
            f"✅ Calendar event created successfully!\n\n"
            f"📌 Title: {title}\n"
            f"🕒 Start: {start.strftime('%d %b %Y %I:%M %p')}\n"
            f"🔗 {event['htmlLink']}"
        )
    }