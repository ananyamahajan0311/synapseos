import re
from datetime import datetime, timedelta

from agents.llm import generate_meeting_details


def parse_meeting_from_email(email_text):

    # Ask Gemini to understand the meeting details
    generated = generate_meeting_details(email_text)

    print("\n========== AI MEETING DETAILS ==========")
    print(generated)

    # Extract values returned by Gemini
    title_match = re.search(
        r"TITLE:\s*(.*)",
        generated,
        re.IGNORECASE
    )

    date_match = re.search(
        r"DATE:\s*(.*)",
        generated,
        re.IGNORECASE
    )

    time_match = re.search(
        r"TIME:\s*(.*)",
        generated,
        re.IGNORECASE
    )

    duration_match = re.search(
        r"DURATION:\s*(\d+)",
        generated,
        re.IGNORECASE
    )

    title = (
        title_match.group(1).strip()
        if title_match
        else "Meeting"
    )

    date_text = (
        date_match.group(1).strip()
        if date_match
        else ""
    )

    time_text = (
        time_match.group(1).strip()
        if time_match
        else ""
    )

    duration = (
        int(duration_match.group(1))
        if duration_match
        else 60
    )

    # Make sure Gemini found the required information
    if (
        not date_text
        or date_text.upper() == "UNKNOWN"
        or not time_text
        or time_text.upper() == "UNKNOWN"
    ):
        return {
            "status": "error",
            "message": (
                "Could not determine the meeting "
                "date and time from the email."
            )
        }

    # Convert Gemini's date/time into a Python datetime
    try:
        import dateparser

        dt = dateparser.parse(
            f"{date_text} {time_text}",
            settings={
                "PREFER_DATES_FROM": "future"
            }
        )

    except Exception:
        dt = None

    if dt is None:
        return {
            "status": "error",
            "message": (
                "The meeting date and time "
                "could not be understood."
            )
        }

    return {
        "status": "success",
        "title": title,
        "start": dt,
        "duration": duration
    }