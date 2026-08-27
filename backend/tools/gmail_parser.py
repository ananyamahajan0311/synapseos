import re


def parse_email_command(command):
    result = {
        "to": "",
        "subject": "",
        "body": ""
    }

    # ============================================================
    # RECIPIENT
    # Supports:
    # "to abc@gmail.com"
    # "mail abc@gmail.com"
    # "email abc@gmail.com"
    # ============================================================

    match = re.search(
        r"(?:to|mail|email)\s+(?:my\s+friend\s+)?([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})",
        command,
        re.IGNORECASE
    )

    if match:
        result["to"] = match.group(1)

    else:
        # Fallback: find any email address in the command
        match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            command
        )

        if match:
            result["to"] = match.group(0)

    # ============================================================
    # SUBJECT
    # ============================================================

    match = re.search(
        r"subject\s+(.*?)\s+body",
        command,
        re.IGNORECASE
    )

    if match:
        result["subject"] = match.group(1).strip()

    # ============================================================
    # BODY
    # ============================================================

    match = re.search(
        r"body\s+(.*)",
        command,
        re.IGNORECASE
    )

    if match:
        result["body"] = match.group(1).strip()

    return result