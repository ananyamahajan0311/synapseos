from datetime import timedelta

from googleapiclient.discovery import build

from services.google_auth import get_credentials
from tools.calendar_parser import parse_event
from tools.email_meeting_parser import parse_meeting_from_email


# ============================================================
# CREATE EVENT FROM NORMAL USER REQUEST
# ============================================================

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

    created_event = (
        service.events()
        .insert(
            calendarId="primary",
            body=event
        )
        .execute()
    )

    return {
        "status": "success",
        "message": (
            "✅ Calendar event created successfully!\n\n"
            f"📌 Title: {title}\n"
            f"🕒 Start: "
            f"{start.strftime('%d %b %Y %I:%M %p')}\n"
            f"🔗 {created_event['htmlLink']}"
        ),
        "calendar_url": created_event["htmlLink"]
    }


# ============================================================
# CREATE EVENT FROM EMAIL
# ============================================================

def create_event_from_email(email_text):

    creds = get_credentials()

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    # Parse meeting information from the email
    parsed = parse_meeting_from_email(email_text)

    if parsed["status"] != "success":
        return parsed

    title = parsed["title"]
    start = parsed["start"]

    # Use AI-detected duration, default to 1 hour
    duration = parsed.get("duration", 60)

    end = start + timedelta(minutes=duration)

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

    created_event = (
        service.events()
        .insert(
            calendarId="primary",
            body=event
        )
        .execute()
    )

    return {
        "status": "success",
        "message": (
            "✅ Calendar event created from email!\n\n"
            f"📌 Title: {title}\n"
            f"🕒 Start: "
            f"{start.strftime('%d %b %Y %I:%M %p')}\n"
            f"🔗 {created_event['htmlLink']}"
        ),
        "calendar_url": created_event["htmlLink"]
    }