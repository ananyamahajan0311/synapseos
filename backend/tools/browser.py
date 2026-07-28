import webbrowser


def open_google():

    webbrowser.open("https://www.google.com")

    return {
        "status": "success",
        "message": "Opened Google."
    }