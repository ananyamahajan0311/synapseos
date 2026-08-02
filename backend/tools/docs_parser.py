import re


def parse_document_request(prompt):
    title = "Untitled Document"
    content = ""

    # Extract title
    title_match = re.search(
        r"(?:called|named)\s+(.*?)(?:\s+containing|\s+with|\s*$)",
        prompt,
        re.IGNORECASE,
    )

    if title_match:
        title = title_match.group(1).strip()

    # Extract content
    content_match = re.search(
        r"(?:containing|with)\s+(.*)",
        prompt,
        re.IGNORECASE,
    )

    if content_match:
        content = content_match.group(1).strip()

    return title, content