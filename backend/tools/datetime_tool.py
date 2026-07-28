from datetime import datetime


def get_datetime():
    return {
        "status": "success",
        "message": datetime.now().strftime("%d %B %Y %I:%M %p")
    }