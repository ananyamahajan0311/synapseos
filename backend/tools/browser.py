import webbrowser
import urllib.parse


def open_google(query=""):
    query = query.strip()

    # Open a specific URL if provided
    if query.startswith("http://") or query.startswith("https://"):
        webbrowser.open(query)

        return {
            "status": "success",
            "message": f"Opened {query}"
        }

    # Default to Google homepage
    if query == "" or query.lower() == "google":
        webbrowser.open("https://www.google.com")

        return {
            "status": "success",
            "message": "Opened Google."
        }

    # Otherwise perform a Google search
    encoded = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded}"

    webbrowser.open(url)

    return {
        "status": "success",
        "message": f"Searching Google for '{query}'."
    }