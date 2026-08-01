from datetime import timedelta
import dateparser


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