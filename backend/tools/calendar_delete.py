from googleapiclient.discovery import build

from services.google_auth import get_credentials


def delete_event(event_name):
    creds = get_credentials()

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    events = (
        service.events()
        .list(
            calendarId="primary",
            maxResults=20,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    items = events.get("items", [])

    for event in items:
        summary = event.get("summary", "")

        if event_name.lower() in summary.lower():
            service.events().delete(
                calendarId="primary",
                eventId=event["id"]
            ).execute()

            return {
                "status": "success",
                "message": f"✅ Deleted calendar event: {summary}"
            }

    return {
        "status": "error",
        "message": "No matching event found."
    }