import re


def parse_document_request(prompt):
    prompt = prompt.strip()

    title = "Untitled Document"

    # Look for an explicitly requested title.
    title_match = re.search(
        r"(?:called|named)\s+(.+?)(?=\s+(?:containing|with|and\s+write|and\s+add)\b|$)",
        prompt,
        re.IGNORECASE,
    )

    if title_match:
        title = title_match.group(1).strip()

    else:
        # If there is no explicit title, create a useful title
        # from the user's request.
        topic_match = re.search(
            r"(?:on|about)\s+(.+?)(?:\s+(?:with|containing)\b|$)",
            prompt,
            re.IGNORECASE,
        )

        if topic_match:
            title = topic_match.group(1).strip().title()
        else:
            title = "SynapseOS Document"

    # IMPORTANT:
    # Preserve the COMPLETE user request.
    # Gemini should understand the request, not the regex parser.
    content = prompt

    return title, content