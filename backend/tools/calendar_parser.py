from datetime import timedelta
import dateparser


# ============================================================
# PARSE NORMAL CALENDAR REQUEST
# ============================================================

def parse_event(user_input):

    title = "Meeting"
    text = user_input.lower()

    # --------------------------------------------------------
    # Extract title
    # --------------------------------------------------------

    if "called" in text:
        title = user_input.split("called", 1)[1].strip()

    # --------------------------------------------------------
    # Extract date/time portion
    # --------------------------------------------------------

    date_text = text

    # Remove task/instruction words
    prefixes = [
        "schedule a meeting",
        "schedule meeting",
        "create a meeting",
        "create meeting",
        "schedule an event",
        "create an event",
        "schedule",
        "create"
    ]

    for prefix in prefixes:
        if date_text.startswith(prefix):
            date_text = date_text[len(prefix):].strip()
            break

    # Remove title portion
    if " called " in date_text:
        date_text = date_text.split(" called ", 1)[0].strip()

    # --------------------------------------------------------
    # Parse date/time
    # --------------------------------------------------------

    dt = dateparser.parse(
        date_text,
        settings={
            "PREFER_DATES_FROM": "future",
            "RETURN_AS_TIMEZONE_AWARE": False
        }
    )

    if dt is None:
        return (
            title,
            dateparser.parse("5 minutes from now"),
            dateparser.parse("1 hour 5 minutes from now")
        )

    # --------------------------------------------------------
    # Create one-hour event
    # --------------------------------------------------------

    end = dt + timedelta(hours=1)

    return title, dt, end


# ============================================================
# PARSE MEETING FROM EMAIL
# ============================================================

def parse_meeting_from_email(email_text):

    title = "Meeting"

    # Extract subject
    for line in email_text.splitlines():

        line = line.strip()

        if line.lower().startswith("subject:"):

            subject = line.split(":", 1)[1].strip()

            if subject:
                title = subject

            break

    # Extract date and time
    dt = dateparser.parse(
        email_text,
        settings={
            "PREFER_DATES_FROM": "future"
        }
    )

    if dt is None:
        return {
            "status": "error",
            "message": (
                "Could not detect a meeting date or time "
                "from the email."
            )
        }

    return {
        "status": "success",
        "title": title,
        "start": dt
    }