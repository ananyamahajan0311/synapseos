import dateparser


def parse_meeting_from_email(email_text):

    title = "Meeting"

    # Try to extract a useful title
    lines = email_text.splitlines()

    for line in lines:
        line = line.strip()

        if line.lower().startswith("subject:"):
            subject = line.split(":", 1)[1].strip()

            if subject:
                title = subject

    # Extract date/time from the entire email
    dt = dateparser.parse(
        email_text,
        settings={
            "PREFER_DATES_FROM": "future"
        }
    )

    if dt is None:
        return {
            "status": "error",
            "message": "Could not detect a meeting date or time."
        }

    return {
        "status": "success",
        "title": title,
        "start": dt,
    }