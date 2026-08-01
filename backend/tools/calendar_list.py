from datetime import datetime

from googleapiclient.discovery import build

from services.google_auth import get_credentials


def list_events():
    creds = get_credentials()

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    now = datetime.utcnow().isoformat() + "Z"

    events = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    items = events.get("items", [])

    if not items:
        return {
            "status": "success",
            "message": "No upcoming events found."
        }

    message = "📅 Upcoming Events\n\n"

    for event in items:
        start = event["start"].get(
            "dateTime",
            event["start"].get("date")
        )

        message += f"• {event['summary']}\n"
        message += f"  {start}\n\n"

    return {
        "status": "success",
        "message": message
    }