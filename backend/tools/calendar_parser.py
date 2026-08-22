from datetime import timedelta
import dateparser


# ============================================================
# PARSE NORMAL CALENDAR REQUEST
# ============================================================

def parse_event(user_input):

    title = "Meeting"

    text = user_input.lower()

    if "called" in text:
        title = user_input.split("called")[-1].strip()

    elif "meeting" in text:
        title = "Meeting"

    dt = dateparser.parse(
        user_input,
        settings={
            "PREFER_DATES_FROM": "future"
        }
    )

    if dt is None:
        dt = dateparser.parse("5 minutes from now")

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